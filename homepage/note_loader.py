from __future__ import annotations

import base64
import mimetypes
import re
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class Note:
    title: str
    summary: str
    date: date
    slug: str
    tags: list[str]
    lang: str
    draft: bool
    path: Path
    body: str
    rendered_body: str = ""
    sort_key: str = field(default="")


def slugify(value: str) -> str:
    normalized = value.strip().lower()
    normalized = re.sub(r"[^\w\s-]", "", normalized, flags=re.UNICODE)
    normalized = re.sub(r"[-\s]+", "-", normalized, flags=re.UNICODE)
    return normalized.strip("-") or "note"


def parse_scalar(value: str) -> Any:
    cleaned = value.strip()
    if not cleaned:
        return ""
    if cleaned.startswith(("'", '"')) and cleaned.endswith(("'", '"')) and len(cleaned) >= 2:
        return cleaned[1:-1]
    lowered = cleaned.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if cleaned.startswith("[") and cleaned.endswith("]"):
        inner = cleaned[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(item.strip()) for item in inner.split(",")]
    return cleaned


def parse_frontmatter(raw_text: str) -> tuple[dict[str, Any], str]:
    if not raw_text.startswith("---\n"):
        return {}, raw_text

    closing_marker = "\n---\n"
    closing_index = raw_text.find(closing_marker, 4)
    if closing_index == -1:
        return {}, raw_text

    metadata_block = raw_text[4:closing_index]
    body = raw_text[closing_index + len(closing_marker) :]
    metadata: dict[str, Any] = {}

    lines = metadata_block.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped or stripped.startswith("#") or ":" not in line:
            index += 1
            continue

        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()

        if value:
            metadata[key] = parse_scalar(value)
            index += 1
            continue

        items: list[Any] = []
        index += 1
        while index < len(lines):
            nested_line = lines[index]
            nested_stripped = nested_line.strip()
            if not nested_stripped:
                index += 1
                continue
            if not nested_line.startswith((" ", "\t", "-")):
                break
            if nested_stripped.startswith("-"):
                items.append(parse_scalar(nested_stripped[1:].strip()))
            index += 1

        metadata[key] = items

    return metadata, body.lstrip()


def parse_note_date(raw_value: Any, path: Path) -> date:
    if isinstance(raw_value, date):
        return raw_value

    if isinstance(raw_value, str):
        normalized = raw_value.strip()
        try:
            return date.fromisoformat(normalized)
        except ValueError:
            try:
                return datetime.fromisoformat(normalized).date()
            except ValueError:
                pass

    return datetime.fromtimestamp(path.stat().st_mtime).date()


def summarize_body(body: str) -> str:
    for chunk in body.split("\n\n"):
        cleaned = chunk.strip()
        if not cleaned or cleaned.startswith("#") or cleaned.startswith("![["):
            continue
        return cleaned.replace("\n", " ")[:160].strip()
    return "No summary available."


def resolve_asset_path(reference: str, note_path: Path, assets_dir: Path) -> Path | None:
    target_name = reference.split("|", 1)[0].strip()
    if not target_name:
        return None

    direct_candidates = [note_path.parent / target_name, assets_dir / target_name]
    for candidate in direct_candidates:
        if candidate.exists() and candidate.is_file():
            return candidate

    basename = Path(target_name).name
    for candidate in assets_dir.rglob("*"):
        if candidate.is_file() and candidate.name == basename:
            return candidate

    return None


def file_to_data_uri(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(path.name)
    mime = mime_type or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def render_markdown(note: Note, slug_lookup: dict[str, str], assets_dir: Path) -> str:
    content = note.body

    def replace_embed(match: re.Match[str]) -> str:
        asset_reference = match.group(1).strip()
        asset_path = resolve_asset_path(asset_reference, note.path, assets_dir)
        if not asset_path:
            return f"`Missing asset: {asset_reference}`"

        alt = Path(asset_reference.split("|", 1)[0].strip()).stem.replace("-", " ")
        return (
            "<figure class='note-image-shell'>"
            f"<img class='note-inline-image' src='{file_to_data_uri(asset_path)}' alt='{alt}' />"
            "</figure>"
        )

    content = re.sub(r"!\[\[(.+?)\]\]", replace_embed, content)

    def replace_markdown_image(match: re.Match[str]) -> str:
        alt_text = match.group(1).strip() or "note image"
        target = match.group(2).strip()
        if target.startswith(("http://", "https://", "data:")):
            return match.group(0)

        asset_path = resolve_asset_path(target, note.path, assets_dir)
        if not asset_path:
            return f"`Missing asset: {target}`"

        return (
            "<figure class='note-image-shell'>"
            f"<img class='note-inline-image' src='{file_to_data_uri(asset_path)}' alt='{alt_text}' />"
            "</figure>"
        )

    content = re.sub(r"!\[(.*?)\]\((.*?)\)", replace_markdown_image, content)

    def replace_link(match: re.Match[str]) -> str:
        target = match.group(1).strip()
        label = match.group(2).strip() if match.group(2) else target
        note_slug = slug_lookup.get(slugify(target))
        if not note_slug:
            return label
        return f"[{label}](?note={note_slug})"

    content = re.sub(r"(?<!\!)\[\[(.*?)(?:\|(.*?))?\]\]", replace_link, content)
    return content


def load_notes(notes_dir: Path, assets_dir: Path) -> list[Note]:
    if not notes_dir.exists():
        return []

    notes: list[Note] = []
    for path in sorted(notes_dir.rglob("*.md")):
        metadata, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        note = Note(
            title=str(metadata.get("title") or path.stem.replace("-", " ").title()),
            summary=str(metadata.get("summary") or summarize_body(body)),
            date=parse_note_date(metadata.get("date"), path),
            slug=slugify(str(metadata.get("slug") or path.stem)),
            tags=[str(tag).strip() for tag in metadata.get("tags", []) if str(tag).strip()],
            lang=str(metadata.get("lang") or "zh"),
            draft=bool(metadata.get("draft", False)),
            path=path,
            body=body.strip(),
        )
        note.sort_key = note.date.isoformat()
        if not note.draft:
            notes.append(note)

    notes.sort(key=lambda item: (item.sort_key, item.title.lower()), reverse=True)
    slug_lookup = {note.slug: note.slug for note in notes}
    for note in notes:
        slug_lookup[slugify(note.title)] = note.slug
        slug_lookup[slugify(note.path.stem)] = note.slug

    for note in notes:
        note.rendered_body = render_markdown(note, slug_lookup, assets_dir)

    return notes


def get_note_tags(notes: list[Note]) -> list[str]:
    return sorted({tag for note in notes for tag in note.tags})


def get_featured_notes(notes: list[Note], limit: int = 3) -> list[Note]:
    return notes[:limit]


def find_note_by_slug(notes: list[Note], slug: str | None) -> Note | None:
    if not slug:
        return None
    return next((note for note in notes if note.slug == slug), None)
