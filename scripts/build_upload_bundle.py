import argparse
import csv
import hashlib
import json
from pathlib import Path


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare an upload bundle from downloaded PDFs (dedupe + manifest)."
    )
    parser.add_argument(
        "--in-dir",
        default="downloads/telegram_pdfs",
        help="Input directory containing PDFs (possibly nested).",
    )
    parser.add_argument(
        "--out-dir",
        default="upload_bundle",
        help="Output directory for upload bundle.",
    )
    args = parser.parse_args()

    in_dir = Path(args.in_dir).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_pdfs = out_dir / "pdfs"
    out_pdfs.mkdir(parents=True, exist_ok=True)

    pdfs = sorted([p for p in in_dir.rglob("*.pdf") if p.is_file()])
    seen_hashes: dict[str, Path] = {}
    manifest = []

    for src in pdfs:
        digest = _sha256(src)
        if digest in seen_hashes:
            continue

        # Keep stable, hash-prefixed filenames to avoid collisions
        safe_name = src.name.replace("/", "_").replace("\\", "_")
        dst = out_pdfs / f"{digest[:12]}__{safe_name}"
        dst.write_bytes(src.read_bytes())

        seen_hashes[digest] = src
        manifest.append(
            {
                "sha256": digest,
                "original_path": str(src),
                "bundle_path": str(dst),
                "filename": src.name,
            }
        )

    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    with (out_dir / "manifest.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["sha256", "filename", "original_path", "bundle_path"])
        w.writeheader()
        for row in manifest:
            w.writerow(row)

    print(f"Input PDFs found: {len(pdfs)}")
    print(f"Unique PDFs bundled: {len(manifest)}")
    print(f"Bundle folder: {out_dir}")


if __name__ == "__main__":
    main()


