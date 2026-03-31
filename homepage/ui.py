from __future__ import annotations

from pathlib import Path

import streamlit as st

from homepage.content_loader import get_text
from homepage.note_loader import Note


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        .note-inline-image {
          max-width: 100%;
          height: auto;
        }
        .note-image-shell {
          margin: 1rem 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_heading(eyebrow: str, title: str, subtitle: str) -> None:
    st.caption(eyebrow)
    st.subheader(title)
    st.write(subtitle)


def render_site_header(name: str, role: str) -> None:
    st.title(name)
    st.caption(role)


def render_page_intro(title: str, description: str) -> None:
    st.write(f"**{title}**")
    st.write(description)


def render_page_strip(items: list[tuple[str, str, str]]) -> None:
    columns = st.columns(len(items))
    for column, (label, value, note) in zip(columns, items, strict=False):
        with column:
            with st.container(border=True):
                st.caption(label)
                st.write(f"**{value}**")
                st.caption(note)


def render_home_page(
    site_content: dict,
    notes: list[Note],
    language: str,
    profile_image: Path,
    open_note,
) -> None:
    profile = site_content["profile"]
    services = site_content["services"]

    left, right = st.columns([2, 1], gap="large")
    with left:
        st.subheader(get_text(profile["role"], language))
        st.write(get_text(profile["heroLead"], language))
        st.write(get_text(profile["summary"], language))
        st.write(get_text(profile["availability"], language))
        st.caption(
            f"{get_text(profile['locationLabel'], language)}: {profile['location']} | {get_text(profile['workType'], language)}"
        )
        st.caption(" / ".join(profile["heroBadges"]))

        st.write("**核心方向**" if language == "zh" else "**Focus**")
        for item in profile["focusCards"]:
            st.write(f"- {get_text(item['title'], language)}: {get_text(item['description'], language)}")

        link_left, link_right = st.columns(2)
        with link_left:
            st.write(f"**{get_text(profile['profileLinksTitle'], language)}**")
            for item in profile["profileLinks"]:
                st.link_button(get_text(item["label"], language), item["href"], use_container_width=True)
        with link_right:
            st.write(f"**{get_text(profile['demoLinksTitle'], language)}**")
            for item in profile["demoLinks"]:
                st.link_button(get_text(item["label"], language), item["href"], use_container_width=True)

    with right:
        st.image(str(profile_image), use_container_width=True)

    st.divider()

    section_heading(
        services["eyebrow"][language],
        services["title"][language],
        services["subtitle"][language],
    )
    service_columns = st.columns(3, gap="medium")
    for column, item in zip(service_columns, services["items"], strict=False):
        with column:
            with st.container(border=True):
                st.caption(item["number"])
                st.write(f"**{get_text(item['title'], language)}**")
                st.write(get_text(item["description"], language))

    st.divider()

    section_heading(
        "作品集" if language == "zh" else "Portfolio",
        "精選展示專案" if language == "zh" else "Featured Projects",
        "展示可交付、可擴充與可說明的實作能力"
        if language == "zh"
        else "Projects that show deliverable, explainable, and expandable implementation work.",
    )
    project_columns = st.columns(2, gap="medium")
    for column, project in zip(project_columns, site_content["projects"], strict=False):
        with column:
            with st.container(border=True):
                st.caption(get_text(project["tag"], language))
                st.write(f"**{get_text(project['title'], language)}**")
                st.write(get_text(project["description"], language))
                st.write(f"**{'你的角色' if language == 'zh' else 'Role'}**")
                st.write(get_text(project["role"], language))
                st.caption(" / ".join(project["stack"]))
                for link in project["links"]:
                    st.link_button(get_text(link["label"], language), link["href"], use_container_width=True)

    st.divider()

    section_heading(
        "知識內容" if language == "zh" else "Knowledge",
        "最新發布筆記" if language == "zh" else "Latest notes",
        "把實作經驗拆解成可閱讀、可分享的內容。"
        if language == "zh"
        else "Turn implementation experience into readable, shareable notes.",
    )
    if not notes:
        st.info(
            "目前還沒有公開筆記，可先執行同步腳本匯入 Obsidian 內容。"
            if language == "zh"
            else "No notes yet. Run the sync script to import curated Obsidian content."
        )
    else:
        note_columns = st.columns(min(3, len(notes)), gap="medium")
        for column, note in zip(note_columns, notes, strict=False):
            with column:
                with st.container(border=True):
                    st.caption(f"{note.lang.upper()} | {note.date.isoformat()}")
                    st.write(f"**{note.title}**")
                    st.write(note.summary)
                    if note.tags:
                        st.caption(f"Tags: {', '.join(note.tags)}")
                    if st.button("閱讀文章" if language == "zh" else "Read note", key=f"home-note-{note.slug}"):
                        open_note(note.slug)

    st.divider()

    contact = site_content["contact"]
    section_heading(
        get_text(contact["title"], language),
        get_text(contact["heading"], language),
        get_text(contact["description"], language),
    )
    contact_columns = st.columns(2, gap="medium")
    for column, group in zip(contact_columns, contact["groups"], strict=False):
        with column:
            with st.container(border=True):
                st.write(f"**{get_text(group['title'], language)}**")
                for item in group["items"]:
                    st.link_button(
                        f"{get_text(item['label'], language)} | {get_text(item['description'], language)}",
                        item["href"],
                        use_container_width=True,
                    )


def render_projects_page(site_content: dict, language: str) -> None:
    section_heading(
        "作品集" if language == "zh" else "Portfolio",
        "案例與可交付成果" if language == "zh" else "Projects",
        "用案例說明你做了什麼、怎麼做，以及成果能如何延伸。"
        if language == "zh"
        else "Use projects to show what you built, how you approached it, and how the result can extend further.",
    )
    for project in site_content["projects"]:
        with st.container(border=True):
            left, right = st.columns([3, 1], gap="large")
            with left:
                st.caption(get_text(project["tag"], language))
                st.write(f"**{get_text(project['title'], language)}**")
                st.write(get_text(project["description"], language))
                st.write(f"**{'我的角色' if language == 'zh' else 'My role'}**")
                st.write(get_text(project["role"], language))
                st.caption(" / ".join(project["stack"]))
            with right:
                for item in project["links"]:
                    st.link_button(get_text(item["label"], language), item["href"], use_container_width=True)
        st.write("")


def render_notes_page(
    site_content: dict,
    notes: list[Note],
    selected_note: Note | None,
    language: str,
    tags: list[str],
    open_note,
    clear_note,
) -> None:
    if selected_note:
        st.subheader(selected_note.title)
        st.caption(f"{selected_note.lang.upper()} | {selected_note.date.isoformat()}")
        st.write(selected_note.summary)
        if selected_note.tags:
            st.caption(f"Tags: {', '.join(selected_note.tags)}")

        action_left, action_right = st.columns([1, 1])
        with action_left:
            if st.button("返回列表" if language == "zh" else "Back to list", use_container_width=True):
                clear_note()
        with action_right:
            st.page_link("app.py", label="Home", icon=":material/home:")
        st.divider()
        st.markdown(selected_note.rendered_body, unsafe_allow_html=True)
        return

    section_heading(
        "知識內容" if language == "zh" else "Knowledge",
        "筆記與文章" if language == "zh" else "Notes",
        "整理來自 Obsidian 發布資料夾的內容。"
        if language == "zh"
        else "Published notes synced from the Obsidian publishing workflow.",
    )

    if not notes:
        st.info(
            "目前沒有可顯示的筆記，請先把整理好的內容同步到 content/notes。"
            if language == "zh"
            else "No notes are available yet. Sync curated content into content/notes first."
        )
        return

    filter_left, filter_center, filter_right = st.columns([2, 1, 1])
    with filter_left:
        keyword = st.text_input("搜尋筆記" if language == "zh" else "Search notes", placeholder="API / automation / workflow")
    with filter_center:
        tag_label = "全部" if language == "zh" else "All"
        selected_tag = st.selectbox("標籤" if language == "zh" else "Tag", options=[tag_label, *tags])
    with filter_right:
        order = st.selectbox(
            "排序" if language == "zh" else "Sort",
            options=["最新優先" if language == "zh" else "Newest first", "最舊優先" if language == "zh" else "Oldest first"],
        )

    filtered_notes = []
    keyword_value = keyword.strip().lower()
    tag_filter = "" if selected_tag == tag_label else selected_tag
    for note in notes:
        haystack = f"{note.title} {note.summary} {' '.join(note.tags)}".lower()
        if keyword_value and keyword_value not in haystack:
            continue
        if tag_filter and tag_filter not in note.tags:
            continue
        filtered_notes.append(note)

    filtered_notes.sort(key=lambda item: item.sort_key, reverse=order in {"最新優先", "Newest first"})

    if not filtered_notes:
        st.info(
            "沒有符合條件的筆記，請調整搜尋字詞或標籤。"
            if language == "zh"
            else "No notes matched the current filters. Try adjusting the keyword or tag."
        )
        return

    for note in filtered_notes:
        with st.container(border=True):
            left, right = st.columns([4, 1], gap="medium")
            with left:
                st.caption(f"{note.lang.upper()} | {note.date.isoformat()}")
                st.write(f"**{note.title}**")
                st.write(note.summary)
                if note.tags:
                    st.caption(f"Tags: {', '.join(note.tags)}")
            with right:
                if st.button("閱讀全文" if language == "zh" else "Read full note", key=f"note-{note.slug}", use_container_width=True):
                    open_note(note.slug)
        st.write("")


def render_about_page(site_content: dict, language: str) -> None:
    about = site_content["about"]
    contact = site_content["contact"]
    section_heading(
        get_text(about["sectionLabel"], language),
        get_text(about["title"], language),
        get_text(about["subtitle"], language),
    )
    left, right = st.columns([2, 1], gap="large")
    with left:
        with st.container(border=True):
            for paragraph in about["paragraphs"]:
                st.write(get_text(paragraph, language))
    with right:
        with st.container(border=True):
            st.write("**適合案型**" if language == "zh" else "**Good fit**")
            for focus in about["focuses"]:
                st.write(f"- {get_text(focus, language)}")

            st.write("")
            st.write("**聯絡入口**" if language == "zh" else "**Links**")
            for group in contact["groups"]:
                st.caption(get_text(group["title"], language))
                for item in group["items"]:
                    st.link_button(
                        f"{get_text(item['label'], language)} | {get_text(item['description'], language)}",
                        item["href"],
                        use_container_width=True,
                    )
