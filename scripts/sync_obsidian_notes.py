from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy curated Obsidian notes into the Streamlit portfolio content folders."
    )
    parser.add_argument("source", help="Path to the Obsidian publish folder.")
    parser.add_argument(
        "--target-notes",
        default="content/notes",
        help="Destination for markdown notes. Default: content/notes",
    )
    parser.add_argument(
        "--target-assets",
        default="static/notes",
        help="Destination for note assets. Default: static/notes",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove existing synced notes and assets before copying.",
    )
    return parser.parse_args()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_publish_content(source_dir: Path, notes_dir: Path, assets_dir: Path) -> tuple[int, int]:
    note_count = 0
    asset_count = 0

    for source_path in sorted(source_dir.rglob("*")):
        if not source_path.is_file():
            continue

        relative_path = source_path.relative_to(source_dir)
        if source_path.suffix.lower() == ".md":
            target_path = notes_dir / relative_path
            ensure_dir(target_path.parent)
            shutil.copy2(source_path, target_path)
            note_count += 1
            continue

        target_path = assets_dir / relative_path
        ensure_dir(target_path.parent)
        shutil.copy2(source_path, target_path)
        asset_count += 1

    return note_count, asset_count


def main() -> None:
    args = parse_args()
    base_dir = Path(__file__).resolve().parents[1]
    source_dir = Path(args.source).expanduser().resolve()
    notes_dir = (base_dir / args.target_notes).resolve()
    assets_dir = (base_dir / args.target_assets).resolve()

    if not source_dir.exists() or not source_dir.is_dir():
        raise SystemExit(f"Source folder does not exist: {source_dir}")

    if args.clean:
        reset_dir(notes_dir)
        reset_dir(assets_dir)
    else:
        ensure_dir(notes_dir)
        ensure_dir(assets_dir)

    note_count, asset_count = copy_publish_content(source_dir, notes_dir, assets_dir)

    print(f"Synced {note_count} note files to {notes_dir}")
    print(f"Synced {asset_count} asset files to {assets_dir}")
    print("Tip: keep unpublished or private content outside the selected publish folder.")


if __name__ == "__main__":
    main()
