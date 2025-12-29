import asyncio
import os

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession


def _env_int(name: str) -> int:
    val = os.getenv(name)
    if not val or not val.strip():
        raise SystemExit(f"Missing required env var: {name}")
    return int(val)


def _env_str(name: str) -> str:
    val = os.getenv(name)
    if not val or not val.strip():
        raise SystemExit(f"Missing required env var: {name}")
    return val.strip()


async def main() -> None:
    load_dotenv()
    api_id = _env_int("TELEGRAM_API_ID")
    api_hash = _env_str("TELEGRAM_API_HASH")

    client = TelegramClient(StringSession(), api_id, api_hash)
    await client.start()  # interactive: asks for phone + code (and 2FA password if enabled)
    try:
        print("\nPaste this into TELEGRAM_SESSION_STRING in your .env:\n")
        print(client.session.save())
        print()
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())


