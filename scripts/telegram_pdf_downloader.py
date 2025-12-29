import argparse
import asyncio
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.custom.message import Message
from tqdm import tqdm


@dataclass(frozen=True)
class DownloadResult:
    message_id: int
    file_path: str


def _env_int(name: str) -> int:
    val = os.getenv(name)
    if not val or not val.strip():
        raise SystemExit(f"Missing required env var: {name}")
    try:
        return int(val)
    except ValueError as e:
        raise SystemExit(f"Env var {name} must be an int") from e


def _env_str(name: str) -> str:
    val = os.getenv(name)
    if not val or not val.strip():
        raise SystemExit(f"Missing required env var: {name}")
    return val.strip()


def _is_pdf_message(msg: Message) -> bool:
    if not msg or not msg.file:
        return False
    mime = (msg.file.mime_type or "").lower()
    if mime == "application/pdf":
        return True
    # Some channels have weird/blank mime types; fall back to extension.
    name = (msg.file.name or "").lower()
    return name.endswith(".pdf")


def _safe_name(name: str) -> str:
    name = name.strip().replace("\n", " ")
    for ch in ["/", "\\", ":", "*", "?", "\"", "<", ">", "|"]:
        name = name.replace(ch, "_")
    return name[:180] if len(name) > 180 else name


def _load_state(state_file: Path) -> dict[str, Any]:
    if not state_file.exists():
        return {"downloaded_message_ids": [], "files": {}}
    return json.loads(state_file.read_text(encoding="utf-8"))


def _save_state(state_file: Path, state: dict[str, Any]) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


async def _download_one_pdf(
    client: TelegramClient,
    msg: Message,
    out_dir: Path,
) -> Optional[DownloadResult]:
    if not _is_pdf_message(msg):
        return None

    filename = msg.file.name or f"telegram_{msg.id}.pdf"
    filename = _safe_name(filename)

    # Organize by year-month to keep directories reasonable
    ym = "unknown-date"
    if msg.date:
        ym = f"{msg.date.year:04d}-{msg.date.month:02d}"

    target_dir = out_dir / ym
    target_dir.mkdir(parents=True, exist_ok=True)

    # Avoid clobbering if duplicates exist in channel
    target = target_dir / filename
    if target.exists():
        stem = target.stem
        suffix = target.suffix
        i = 2
        while True:
            candidate = target_dir / f"{stem} ({i}){suffix}"
            if not candidate.exists():
                target = candidate
                break
            i += 1

    await client.download_media(msg, file=str(target))
    return DownloadResult(message_id=msg.id, file_path=str(target))


async def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download PDFs from a Telegram channel (attachments only) into a local folder."
    )
    parser.add_argument(
        "--channel",
        required=True,
        help="Channel username (e.g. @mychannel) or t.me link.",
    )
    parser.add_argument(
        "--out-dir",
        default="downloads/telegram_pdfs",
        help="Output directory for downloaded PDFs.",
    )
    parser.add_argument(
        "--state-file",
        default="state/telegram_downloader_state.json",
        help="State file to support resume and avoid duplicates.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Optional max messages to scan (0 = no limit).",
    )
    parser.add_argument(
        "--min-message-id",
        type=int,
        default=0,
        help="Only scan messages with id > this value (useful for incremental runs).",
    )
    args = parser.parse_args()

    load_dotenv()
    api_id = _env_int("TELEGRAM_API_ID")
    api_hash = _env_str("TELEGRAM_API_HASH")
    session_string = os.getenv("TELEGRAM_SESSION_STRING", "").strip()

    out_dir = Path(args.out_dir).expanduser().resolve()
    state_file = Path(args.state_file).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    state = _load_state(state_file)
    downloaded_ids = set(int(x) for x in state.get("downloaded_message_ids", []))

    session = StringSession(session_string) if session_string else None
    client = TelegramClient(session or "telegram_session", api_id, api_hash)

    await client.start()  # interactive the first time unless TELEGRAM_SESSION_STRING is set

    # Handle numeric channel IDs
    entity = args.channel
    try:
        entity = int(args.channel)
    except ValueError:
        pass  # Keep as string (username)
    total_scanned = 0
    new_downloads: list[DownloadResult] = []

    # Telethon iter_messages returns newest -> oldest by default
    pbar = tqdm(total=args.limit if args.limit and args.limit > 0 else None, unit="msg")
    try:
        async for msg in client.iter_messages(entity, limit=args.limit or None):
            total_scanned += 1
            pbar.update(1)

            if msg.id <= args.min_message_id:
                continue
            if msg.id in downloaded_ids:
                continue

            res = await _download_one_pdf(client, msg, out_dir)
            if not res:
                continue

            new_downloads.append(res)
            downloaded_ids.add(res.message_id)
            state.setdefault("files", {})[str(res.message_id)] = res.file_path
            state["downloaded_message_ids"] = sorted(downloaded_ids)
            _save_state(state_file, state)
    finally:
        pbar.close()
        await client.disconnect()

    print(f"Scanned messages: {total_scanned}")
    print(f"New PDFs downloaded: {len(new_downloads)}")
    if new_downloads:
        print("Latest downloads:")
        for r in new_downloads[-10:]:
            print(f"- {r.message_id}: {r.file_path}")


if __name__ == "__main__":
    asyncio.run(main())


