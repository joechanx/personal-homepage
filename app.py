from pathlib import Path

import streamlit as st

from homepage.content_loader import get_site_content, get_text
from homepage.note_loader import find_note_by_slug, get_featured_notes, get_note_tags, load_notes
from homepage.ui import (
    inject_global_styles,
    render_about_page,
    render_home_page,
    render_notes_page,
    render_projects_page,
    render_site_header,
)

BASE_DIR = Path(__file__).resolve().parent
NOTES_DIR = BASE_DIR / "content" / "notes"
NOTE_ASSETS_DIR = BASE_DIR / "static" / "notes"
PROFILE_IMAGE = BASE_DIR / "public" / "profile.jpg"
DEFAULT_LANGUAGE = "zh"
LANGUAGES = ("zh", "en")


def get_language() -> str:
    current = st.session_state.get("language", DEFAULT_LANGUAGE)
    if current not in LANGUAGES:
        current = DEFAULT_LANGUAGE
    return current


def set_language(language: str) -> None:
    if language in LANGUAGES:
        st.session_state.language = language


def get_selected_note_slug() -> str | None:
    slug = st.query_params.get("note")
    return str(slug) if slug else None


def open_note(note_slug: str) -> None:
    st.query_params["note"] = note_slug
    st.rerun()


def clear_note() -> None:
    if "note" in st.query_params:
        del st.query_params["note"]
    st.rerun()


st.set_page_config(
    page_title="Dexter Chang | Editorial Portfolio",
    page_icon="DC",
    layout="wide",
    initial_sidebar_state="collapsed",
)

site_content = get_site_content()
notes = load_notes(NOTES_DIR, NOTE_ASSETS_DIR)
language = get_language()
selected_note = find_note_by_slug(notes, get_selected_note_slug())

inject_global_styles()
render_site_header(site_content["profile"]["name"], get_text(site_content["profile"]["role"], language))

header_left, header_right = st.columns([0.75, 0.25])
with header_left:
    st.caption(get_text(site_content["seo"]["description"], language))
with header_right:
    selected_language = st.segmented_control(
        "Language",
        options=list(LANGUAGES),
        default=language,
        format_func=lambda value: "中文 / EN" if value == "zh" else "EN / 中文",
        label_visibility="collapsed",
    )
    set_language(selected_language or language)
    language = get_language()


def home_page() -> None:
    render_home_page(
        site_content=site_content,
        notes=get_featured_notes(notes, limit=3),
        language=language,
        profile_image=PROFILE_IMAGE,
        open_note=open_note,
    )


def projects_page() -> None:
    render_projects_page(site_content=site_content, language=language)


def notes_page() -> None:
    render_notes_page(
        site_content=site_content,
        notes=notes,
        selected_note=selected_note,
        language=language,
        tags=get_note_tags(notes),
        open_note=open_note,
        clear_note=clear_note,
    )


def about_page() -> None:
    render_about_page(site_content=site_content, language=language)


navigation = st.navigation(
    [
        st.Page(home_page, title="Home", icon=":material/home:"),
        st.Page(projects_page, title="Projects", icon=":material/rocket_launch:"),
        st.Page(notes_page, title="Notes", icon=":material/menu_book:"),
        st.Page(about_page, title="About", icon=":material/person:"),
    ],
    position="top",
)

navigation.run()
