from __future__ import annotations

from pathlib import Path

import streamlit as st

from homepage.content_loader import get_text
from homepage.note_loader import Note


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Manrope:wght@400;500;600;700;800&family=Noto+Sans+TC:wght@400;500;700;800&display=swap');

        .stApp {
          background:
            radial-gradient(circle at top left, rgba(255, 255, 255, 0.96) 0%, rgba(239, 244, 250, 0.92) 35%, rgba(227, 235, 246, 0.95) 100%),
            linear-gradient(180deg, #f8fbff 0%, #eef3f9 100%);
          color: #102033;
          font-family: "Manrope", "Noto Sans TC", "Segoe UI", sans-serif;
        }
        .block-container {
          max-width: 1180px;
          padding-top: 1.1rem;
          padding-bottom: 4.8rem;
        }
        .site-header {
          display: flex;
          justify-content: space-between;
          align-items: end;
          gap: 1rem;
          margin-bottom: 0.35rem;
        }
        .site-title {
          font-size: 1.08rem;
          font-weight: 800;
          letter-spacing: 0.08em;
          text-transform: uppercase;
        }
        .site-subtitle {
          color: #5e6e84;
          margin-top: 0.15rem;
          font-size: 0.9rem;
        }
        .section-shell {
          margin-top: 1.7rem;
          margin-bottom: 1rem;
        }
        .feature-card,
        .project-card,
        .note-card,
        .link-card,
        .article-shell {
          background: rgba(255, 255, 255, 0.88);
          border: 1px solid rgba(214, 223, 236, 0.95);
          border-radius: 24px;
          box-shadow: 0 16px 42px rgba(16, 32, 51, 0.07);
        }
        .feature-card,
        .project-card,
        .note-card,
        .link-card {
          padding: 1.3rem;
          min-height: 100%;
        }
        .project-card,
        .note-card,
        .link-card {
          display: flex;
          flex-direction: column;
          gap: 0.65rem;
        }
        .article-shell {
          padding: 1.7rem;
        }
        .hero-shell {
          padding: 1.85rem;
          border-radius: 30px;
          border: 1px solid rgba(214, 223, 236, 0.95);
          box-shadow: 0 16px 42px rgba(16, 32, 51, 0.07);
          background:
            radial-gradient(circle at top right, rgba(38, 86, 156, 0.12) 0%, rgba(38, 86, 156, 0.02) 36%, rgba(255, 255, 255, 0.9) 72%),
            linear-gradient(180deg, rgba(255, 255, 255, 0.96) 0%, rgba(245, 249, 255, 0.96) 100%);
        }
        .eyebrow,
        .card-label {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          border-radius: 999px;
          background: #e9f1ff;
          color: #1e4ea7;
          font-size: 0.78rem;
          font-weight: 800;
          letter-spacing: 0.03em;
          padding: 0.42rem 0.8rem;
        }
        .hero-name {
          font-size: 0.94rem;
          color: #5d6c82;
          font-weight: 700;
          letter-spacing: 0.05em;
          text-transform: uppercase;
          margin-top: 0.8rem;
        }
        .hero-lead {
          color: #36598f;
          font-size: 0.96rem;
          font-weight: 700;
          line-height: 1.65;
          margin-top: 1rem;
          max-width: 58ch;
        }
        .hero-title {
          font-size: clamp(2rem, 2.8vw, 3.05rem);
          font-family: "Fraunces", "Noto Sans TC", serif;
          font-weight: 700;
          line-height: 1.04;
          margin-top: 0.35rem;
          letter-spacing: -0.03em;
        }
        .section-title {
          font-size: clamp(1.55rem, 2.1vw, 2.25rem);
          font-family: "Fraunces", "Noto Sans TC", serif;
          font-weight: 700;
          line-height: 1.14;
          margin-top: 0.55rem;
          letter-spacing: -0.02em;
        }
        .section-subtitle,
        .muted,
        .hero-summary,
        .article-summary {
          color: #5a677b;
          line-height: 1.72;
        }
        .hero-summary {
          max-width: 60ch;
          font-size: 1rem;
          margin-top: 0.9rem;
        }
        .feature-title,
        .project-title,
        .note-title,
        .about-title {
          font-size: 1.08rem;
          font-weight: 800;
          margin: 0.75rem 0 0.45rem;
        }
        .project-title,
        .note-title {
          font-size: 1.14rem;
        }
        .card-summary {
          color: #5a677b;
          line-height: 1.72;
          min-height: 5.4rem;
        }
        .project-card .card-summary,
        .note-card .card-summary,
        .link-card .card-summary {
          min-height: 0;
        }
        .card-role {
          color: #526177;
          font-size: 0.9rem;
          line-height: 1.65;
          padding-top: 0.15rem;
        }
        .card-meta-label {
          color: #6b7790;
          font-size: 0.76rem;
          font-weight: 800;
          letter-spacing: 0.08em;
          text-transform: uppercase;
        }
        .tag-row,
        .stack-row,
        .meta-row {
          display: flex;
          flex-wrap: wrap;
          gap: 0.55rem;
          margin-top: 0.95rem;
        }
        .skill-grid {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 0.85rem;
          margin-top: 1.15rem;
        }
        .skill-card {
          border-radius: 20px;
          border: 1px solid rgba(214, 223, 236, 0.95);
          background: rgba(255, 255, 255, 0.82);
          padding: 1rem 1rem 1.05rem;
        }
        .skill-card-kicker {
          color: #6b7790;
          font-size: 0.74rem;
          font-weight: 800;
          letter-spacing: 0.08em;
          text-transform: uppercase;
        }
        .skill-card-title {
          color: #102033;
          font-size: 0.98rem;
          font-weight: 800;
          line-height: 1.5;
          margin-top: 0.3rem;
        }
        .skill-card-description {
          color: #5a677b;
          font-size: 0.88rem;
          line-height: 1.6;
          margin-top: 0.45rem;
        }
        .tag-chip,
        .stack-badge,
        .meta-pill {
          display: inline-flex;
          align-items: center;
          border-radius: 999px;
          border: 1px solid rgba(214, 223, 236, 0.95);
          background: rgba(255, 255, 255, 0.9);
          padding: 0.42rem 0.76rem;
          font-size: 0.84rem;
        }
        .proof-grid {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 0.8rem;
          margin-top: 1rem;
        }
        .proof-card {
          border-radius: 16px;
          border: 1px solid rgba(214, 223, 236, 0.95);
          background: rgba(255, 255, 255, 0.72);
          padding: 0.8rem 0.95rem 0.82rem;
        }
        .proof-label {
          color: #6b7790;
          font-size: 0.72rem;
          font-weight: 800;
          letter-spacing: 0.06em;
          text-transform: uppercase;
        }
        .proof-value {
          color: #102033;
          font-size: 1.18rem;
          font-weight: 800;
          margin-top: 0.18rem;
        }
        .proof-note {
          color: #5a677b;
          font-size: 0.8rem;
          margin-top: 0.18rem;
          line-height: 1.5;
        }
        .cta-shell {
          margin-top: 1rem;
          border-radius: 24px;
          border: 1px solid rgba(214, 223, 236, 0.95);
          background: rgba(255, 255, 255, 0.78);
          padding: 1rem 1rem 0.8rem;
        }
        .cta-title {
          color: #102033;
          font-size: 0.95rem;
          font-weight: 800;
          margin-bottom: 0.1rem;
        }
        .cta-note {
          color: #5a677b;
          font-size: 0.85rem;
          line-height: 1.55;
          margin-bottom: 0.7rem;
        }
        .page-intro-card {
          margin: 1rem 0 1.4rem;
          padding: 1.2rem 1.3rem;
          border-radius: 24px;
          border: 1px solid rgba(214, 223, 236, 0.95);
          background: rgba(255, 255, 255, 0.82);
          box-shadow: 0 12px 30px rgba(16, 32, 51, 0.05);
        }
        .page-intro-title {
          color: #102033;
          font-size: 1.04rem;
          font-weight: 800;
          margin-bottom: 0.28rem;
        }
        .page-intro-copy {
          color: #5a677b;
          line-height: 1.72;
        }
        .page-strip {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 0.8rem;
          margin: 0.2rem 0 1.2rem;
        }
        .page-strip-card {
          padding: 0.95rem 1rem;
          border-radius: 20px;
          border: 1px solid rgba(214, 223, 236, 0.95);
          background: rgba(255, 255, 255, 0.76);
          box-shadow: 0 10px 24px rgba(16, 32, 51, 0.04);
        }
        .page-strip-label {
          color: #6b7790;
          font-size: 0.73rem;
          font-weight: 800;
          letter-spacing: 0.08em;
          text-transform: uppercase;
        }
        .page-strip-value {
          color: #102033;
          font-size: 1rem;
          font-weight: 800;
          line-height: 1.35;
          margin-top: 0.28rem;
        }
        .page-strip-note {
          color: #5a677b;
          font-size: 0.82rem;
          line-height: 1.55;
          margin-top: 0.2rem;
        }
        .action-panel {
          padding: 1.1rem 1.1rem 0.9rem;
          border-radius: 22px;
          border: 1px solid rgba(214, 223, 236, 0.95);
          background: rgba(255, 255, 255, 0.82);
          box-shadow: 0 12px 30px rgba(16, 32, 51, 0.05);
        }
        .action-panel-title {
          color: #102033;
          font-size: 0.95rem;
          font-weight: 800;
          margin-bottom: 0.18rem;
        }
        .action-panel-copy {
          color: #5a677b;
          font-size: 0.85rem;
          line-height: 1.6;
          margin-bottom: 0.7rem;
        }
        .about-shell {
          padding: 1.45rem;
        }
        .about-paragraph {
          color: #5a677b;
          line-height: 1.8;
          margin: 0 0 1rem;
        }
        .about-paragraph:last-child {
          margin-bottom: 0;
        }
        .focus-card {
          margin-bottom: 0.9rem;
        }
        .contact-link-copy {
          color: #5a677b;
          font-size: 0.88rem;
          line-height: 1.6;
          margin-top: -0.15rem;
        }
        .hero-footnote {
          color: #647288;
          font-size: 0.84rem;
          line-height: 1.6;
          margin-top: 0.95rem;
        }
        .note-meta {
          color: #6c778b;
          font-size: 0.85rem;
          margin-top: 0.45rem;
        }
        .link-card-stat {
          color: #102033;
          font-size: 1.55rem;
          font-weight: 800;
          line-height: 1;
          margin-top: 0.2rem;
        }
        .article-title {
          font-size: clamp(1.9rem, 2.5vw, 2.65rem);
          font-weight: 800;
          line-height: 1.1;
          margin-top: 0.7rem;
        }
        .article-divider {
          height: 1px;
          background: rgba(221, 229, 240, 1);
          margin: 1.1rem 0 1.3rem;
        }
        .empty-state {
          padding: 1.15rem;
          border-radius: 20px;
          border: 1px dashed rgba(176, 188, 205, 1);
          background: rgba(255, 255, 255, 0.68);
          color: #5d6c82;
        }
        .soft-divider {
          height: 1px;
          background: rgba(221, 229, 240, 0.92);
          margin: 1.2rem 0 1.45rem;
        }
        .note-inline-image {
          width: 100%;
          border-radius: 18px;
          border: 1px solid rgba(214, 223, 236, 0.95);
        }
        .note-image-shell {
          margin: 1rem 0;
        }
        div[data-testid="stVerticalBlock"] div[data-testid="stButton"] > button {
          border-radius: 999px;
          min-height: 2.9rem;
          font-weight: 700;
          border: 1px solid rgba(214, 223, 236, 0.95);
        }
        div[data-testid="stLinkButton"] a {
          border-radius: 999px !important;
          font-weight: 700 !important;
        }
        div[data-testid="stImage"] img {
          border-radius: 24px;
          min-height: 100%;
          object-fit: cover;
          border: 1px solid rgba(214, 223, 236, 0.95);
          box-shadow: 0 20px 50px rgba(16, 32, 51, 0.1);
          background: rgba(255, 255, 255, 0.95);
        }
        @media (max-width: 900px) {
          .page-strip,
          .skill-grid,
          .proof-grid {
            grid-template-columns: 1fr;
          }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_heading(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="section-shell">
          <div class="eyebrow">{eyebrow}</div>
          <div class="section-title">{title}</div>
          <div class="section-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_site_header(name: str, role: str) -> None:
    st.markdown(
        f"""
        <div class="site-header">
          <div>
            <div class="site-title">{name}</div>
            <div class="site-subtitle">{role}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_intro(title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="page-intro-card">
          <div class="page-intro-title">{title}</div>
          <div class="page-intro-copy">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_strip(items: list[tuple[str, str, str]]) -> None:
    st.markdown(
        "<div class='page-strip'>"
        + "".join(
            f"""
            <div class="page-strip-card">
              <div class="page-strip-label">{label}</div>
              <div class="page-strip-value">{value}</div>
              <div class="page-strip-note">{note}</div>
            </div>
            """
            for label, value, note in items
        )
        + "</div>",
        unsafe_allow_html=True,
    )


def render_home_page(
    site_content: dict,
    notes: list[Note],
    language: str,
    profile_image: Path,
    open_note,
) -> None:
    profile = site_content["profile"]
    services = site_content["services"]
    hero_stats = [
        (
            "Featured Work",
            f"{len(site_content['projects']):02d}",
            "精選案例" if language == "zh" else "featured case studies",
        ),
        (
            "Published Notes",
            f"{len(notes):02d}",
            "公開技術筆記" if language == "zh" else "published notes",
        ),
        (
            "Primary Focus",
            "API + Auto",
            "串接與流程整理" if language == "zh" else "integration and workflow cleanup",
        ),
    ]
    left, right = st.columns([1.12, 0.88], gap="large")

    with left:
        st.markdown(
            f"""
            <div class="hero-shell">
              <div class="eyebrow">{get_text(profile["badge"], language)}</div>
              <div class="hero-name">{profile["name"]}</div>
              <div class="hero-lead">{get_text(profile["heroLead"], language)}</div>
              <div class="hero-title">{get_text(profile["role"], language)}</div>
              <div class="hero-summary">{get_text(profile["summary"], language)}</div>
              <div class="skill-grid">
                {"".join(
                    f'''
                    <div class="skill-card">
                      <div class="skill-card-kicker">{item["title"]["en"].upper()}</div>
                      <div class="skill-card-title">{get_text(item["title"], language)}</div>
                      <div class="skill-card-description">{get_text(item["description"], language)}</div>
                    </div>
                    '''
                    for item in profile["focusCards"]
                )}
              </div>
              <div class="meta-row">
                <span class="meta-pill">{get_text(profile["locationLabel"], language)}: {profile["location"]}</span>
                <span class="meta-pill">{get_text(profile["workType"], language)}</span>
              </div>
              <div class="stack-row">
                {"".join(f"<span class='stack-badge'>{badge}</span>" for badge in profile["heroBadges"])}
              </div>
              <p class="muted">{get_text(profile["availability"], language)}</p>
              <div class="hero-footnote">{"適合需要先做出可用版本，再逐步擴充的 API integration 與 automation 類型需求。" if language == "zh" else "A strong fit for API integration and automation projects that need a usable first version with room to expand."}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='proof-grid'>"
            + "".join(
                f"""
                <div class="proof-card">
                  <div class="proof-label">{label}</div>
                  <div class="proof-value">{value}</div>
                  <div class="proof-note">{note}</div>
                </div>
                """
                for label, value, note in hero_stats
            )
            + "</div>",
            unsafe_allow_html=True,
        )
        cta_left, cta_right = st.columns(2, gap="medium")
        with cta_left:
            st.markdown(
                f"""
                <div class="cta-shell">
                  <div class="cta-title">{get_text(profile["profileLinksTitle"], language)}</div>
                  <div class="cta-note">{"先從背景、公開程式碼與合作定位快速了解我。" if language == "zh" else "Start with background, public code, and delivery context for a quick overview."}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            for item in profile["profileLinks"]:
                st.link_button(
                    get_text(item["label"], language),
                    item["href"],
                    use_container_width=True,
                    type="primary" if item.get("primary") else "secondary",
                )
        with cta_right:
            st.markdown(
                f"""
                <div class="cta-shell">
                  <div class="cta-title">{get_text(profile["demoLinksTitle"], language)}</div>
                  <div class="cta-note">{"如果你想先看已完成的實作成果，可以直接從這裡進入。" if language == "zh" else "If you prefer to review working examples first, start here."}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            for item in profile["demoLinks"]:
                st.link_button(
                    get_text(item["label"], language),
                    item["href"],
                    use_container_width=True,
                    type="primary" if item.get("primary") else "secondary",
                )
    with right:
        st.image(str(profile_image), use_container_width=True)

    section_heading(
        services["eyebrow"][language],
        services["title"][language],
        services["subtitle"][language],
    )
    service_columns = st.columns(3, gap="medium")
    for column, item in zip(service_columns, services["items"], strict=False):
        with column:
            st.markdown(
                f"""
                <div class="feature-card">
                  <div class="card-label">{item["number"]}</div>
                  <div class="feature-title">{get_text(item["title"], language)}</div>
                  <div class="muted">{get_text(item["description"], language)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    section_heading(
        "信任線索" if language == "zh" else "Signals of trust",
        "作品與內容一起建立可驗證的可信度" if language == "zh" else "Projects and writing build credibility together",
        "讓訪客快速看到你的做法、思路與交付方式，而不是只看到一串技術名詞。"
        if language == "zh"
        else "Let visitors see your implementation style, reasoning, and delivery mindset instead of just a list of technologies.",
    )
    highlight_columns = st.columns(3, gap="medium")
    for column, highlight in zip(highlight_columns, site_content["highlights"], strict=False):
        with column:
            st.markdown(
                f"""
                <div class="feature-card">
                  <div class="card-label">{'Why it matters' if language == 'en' else 'Why it matters'}</div>
                  <div class="feature-title">{get_text(highlight["title"], language)}</div>
                  <div class="muted">{get_text(highlight["description"], language)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

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
            st.markdown(
                f"""
                <div class="project-card">
                  <div class="card-label">{get_text(project["tag"], language)}</div>
                  <div class="project-title">{get_text(project["title"], language)}</div>
                  <div class="card-summary">{get_text(project["description"], language)}</div>
                  <div class="card-meta-label">{'你的角色' if language == 'zh' else 'Role'}</div>
                  <div class="card-role">{get_text(project["role"], language)}</div>
                  <div class="stack-row">
                    {"".join(f"<span class='stack-badge'>{item}</span>" for item in project["stack"])}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            for link in project["links"]:
                st.link_button(get_text(link["label"], language), link["href"], use_container_width=True)

    section_heading(
        "知識內容" if language == "zh" else "Knowledge",
        "最新發布筆記" if language == "zh" else "Latest published notes",
        "把實作經驗拆解成可閱讀、可分享的內容，讓合作方更快理解你的技術判斷。"
        if language == "zh"
        else "Turn implementation experience into readable notes that make your technical judgment easier to trust.",
    )
    if not notes:
        st.markdown(
            f'<div class="empty-state">{"目前還沒有公開筆記，可先執行同步腳本匯入 Obsidian 內容。" if language == "zh" else "No published notes yet. Run the sync script to import your curated Obsidian content."}</div>',
            unsafe_allow_html=True,
        )
    else:
        note_columns = st.columns(min(3, len(notes)), gap="medium")
        for column, note in zip(note_columns, notes, strict=False):
            with column:
                st.markdown(
                    f"""
                    <div class="note-card">
                      <div class="card-label">{note.lang.upper()}</div>
                      <div class="note-title">{note.title}</div>
                      <div class="note-meta">{note.date.isoformat()}</div>
                      <div class="card-summary">{note.summary}</div>
                      <div class="stack-row">
                        {"".join(f"<span class='tag-chip'>{tag}</span>" for tag in note.tags)}
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("閱讀文章" if language == "zh" else "Read note", key=f"home-note-{note.slug}"):
                    open_note(note.slug)

    contact = site_content["contact"]
    section_heading(
        get_text(contact["title"], language),
        get_text(contact["heading"], language),
        get_text(contact["description"], language),
    )
    contact_columns = st.columns(2, gap="medium")
    for column, group in zip(contact_columns, contact["groups"], strict=False):
        with column:
            st.markdown(
                f"""
                <div class="link-card">
                  <div class="card-meta-label">{'Link Group' if language == 'en' else 'Link Group'}</div>
                  <div class="about-title">{get_text(group["title"], language)}</div>
                  <div class="link-card-stat">{len(group["items"]):02d}</div>
                  <div class="muted">{len(group["items"])} {"個入口" if language == "zh" else "entry points"}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            for item in group["items"]:
                st.link_button(
                    f'{get_text(item["label"], language)} | {get_text(item["description"], language)}',
                    item["href"],
                    use_container_width=True,
                )


def render_projects_page(site_content: dict, language: str) -> None:
    section_heading(
        "作品集" if language == "zh" else "Portfolio",
        "案例與可交付成果" if language == "zh" else "Case studies and deliverable work",
        "用案例說明你做了什麼、怎麼做，以及成果能如何延伸。"
        if language == "zh"
        else "Use projects to show what you built, how you approached it, and how the result can extend further.",
    )
    render_page_intro(
        "這裡收錄目前公開展示的代表案例。" if language == "zh" else "This page collects the public projects that best represent my delivery style.",
        "重點不是只列出技術棧，而是讓合作方快速理解需求拆解、角色分工與可延伸方向。"
        if language == "zh"
        else "The goal is not just to list the stack, but to make the scoping, role, and extension path easy to evaluate.",
    )
    render_page_strip(
        [
            (
                "Projects",
                f"{len(site_content['projects']):02d}",
                "目前公開展示的案例數" if language == "zh" else "public case studies currently shown",
            ),
            (
                "Delivery Lens",
                "API + Automation",
                "以可交付與可維護為主" if language == "zh" else "delivery and maintainability first",
            ),
            (
                "Review Mode",
                "Code / Demo",
                "可以同時看原始碼與成果" if language == "zh" else "review both source code and live output",
            ),
        ]
    )
    projects = site_content["projects"]
    for index, project in enumerate(projects):
        left, right = st.columns([0.72, 0.28], gap="large")
        with left:
            st.markdown(
                f"""
                <div class="project-card">
                  <div class="card-label">{get_text(project["tag"], language)}</div>
                  <div class="project-title">{get_text(project["title"], language)}</div>
                  <div class="card-summary">{get_text(project["description"], language)}</div>
                  <div class="card-meta-label">{'我的角色' if language == 'zh' else 'My role'}</div>
                  <div class="card-role">{get_text(project["role"], language)}</div>
                  <div class="stack-row">
                    {"".join(f"<span class='stack-badge'>{item}</span>" for item in project["stack"])}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with right:
            st.markdown(
                f"""
                <div class="action-panel">
                  <div class="action-panel-title">{'專案入口' if language == 'zh' else 'Project links'}</div>
                  <div class="action-panel-copy">{"可直接查看原始碼與線上展示。" if language == "zh" else "Jump straight into the source code or live demo."}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            for item in project["links"]:
                st.link_button(get_text(item["label"], language), item["href"], use_container_width=True)
        if index != len(projects) - 1:
            st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)


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
        st.markdown(
            f"""
            <div class="article-shell">
              <div class="eyebrow">{selected_note.lang.upper()}</div>
              <div class="article-title">{selected_note.title}</div>
              <div class="note-meta">{selected_note.date.isoformat()}</div>
              <div class="article-summary">{selected_note.summary}</div>
              <div class="stack-row">
                {"".join(f"<span class='tag-chip'>{tag}</span>" for tag in selected_note.tags)}
              </div>
              <div class="article-divider"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        action_left, action_right, _ = st.columns([0.2, 0.2, 0.6])
        with action_left:
            if st.button("返回列表" if language == "zh" else "Back to list", use_container_width=True):
                clear_note()
        with action_right:
            st.page_link("app.py", label="Home", icon=":material/home:")
        st.markdown(selected_note.rendered_body, unsafe_allow_html=True)
        return

    section_heading(
        "知識內容" if language == "zh" else "Knowledge",
        "筆記與文章" if language == "zh" else "Notes and articles",
        "整理來自 Obsidian 發布資料夾的內容，將實作經驗、工具流程與案例拆成可閱讀的文章。"
        if language == "zh"
        else "Published notes from your Obsidian workflow, covering implementation insights, tooling, and case-driven writeups.",
    )
    render_page_intro(
        "這裡會顯示從 Obsidian 發布流程整理過的技術筆記。" if language == "zh" else "This page surfaces technical notes curated from the Obsidian publishing workflow.",
        "你可以用關鍵字、標籤與日期快速篩選，讓筆記頁更像知識入口而不是單純的文章堆疊。"
        if language == "zh"
        else "Use keywords, tags, and sort order to turn the note archive into a navigable knowledge hub instead of a flat list.",
    )
    render_page_strip(
        [
            (
                "Published Notes",
                f"{len(notes):02d}",
                "目前可瀏覽的文章數量" if language == "zh" else "articles currently available",
            ),
            (
                "Topics",
                f"{len(tags):02d}",
                "可用標籤數量" if language == "zh" else "available tag filters",
            ),
            (
                "Source",
                "Obsidian",
                "由發布流程同步進網站" if language == "zh" else "synced in through the publishing workflow",
            ),
        ]
    )

    if not notes:
        st.markdown(
            f'<div class="empty-state">{"目前沒有可顯示的筆記，請先把整理好的內容同步到 content/notes。" if language == "zh" else "No notes are available yet. Sync your curated content into content/notes first."}</div>',
            unsafe_allow_html=True,
        )
        return

    st.caption("用搜尋、標籤與排序快速縮小你想看的內容。" if language == "zh" else "Use search, tags, and sorting to narrow down the content you want.")
    filter_left, filter_center, filter_right = st.columns([0.42, 0.26, 0.32])
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
        st.markdown(
            f'<div class="empty-state">{"沒有符合條件的筆記，請調整搜尋字詞或標籤。" if language == "zh" else "No notes matched the current filters. Try adjusting the keyword or tag."}</div>',
            unsafe_allow_html=True,
        )
        return

    for note in filtered_notes:
        left, right = st.columns([0.78, 0.22], gap="medium")
        with left:
            st.markdown(
                f"""
                <div class="note-card">
                  <div class="card-label">{note.lang.upper()}</div>
                  <div class="note-title">{note.title}</div>
                  <div class="note-meta">{note.date.isoformat()}</div>
                  <div class="card-summary">{note.summary}</div>
                  <div class="stack-row">
                    {"".join(f"<span class='tag-chip'>{tag_name}</span>" for tag_name in note.tags)}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with right:
            st.markdown(
                f"""
                <div class="action-panel">
                  <div class="action-panel-title">{'閱讀入口' if language == 'zh' else 'Read note'}</div>
                  <div class="action-panel-copy">{"進入單篇頁面查看完整內容與附圖。" if language == "zh" else "Open the full post with the complete article body and assets."}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("閱讀全文" if language == "zh" else "Read full note", key=f"note-{note.slug}", use_container_width=True):
                open_note(note.slug)


def render_about_page(site_content: dict, language: str) -> None:
    about = site_content["about"]
    contact = site_content["contact"]
    section_heading(
        get_text(about["sectionLabel"], language),
        get_text(about["title"], language),
        get_text(about["subtitle"], language),
    )
    render_page_intro(
        "合作偏好是先把需求整理成可交付的第一版，再逐步擴充。" if language == "zh" else "I prefer shaping work into a usable first delivery, then expanding from there.",
        "這頁集中整理合作方式、適合案型與維護觀點，讓訪客快速判斷是否適合一起合作。"
        if language == "zh"
        else "This page summarizes collaboration style, project fit, and maintenance priorities so visitors can quickly gauge fit.",
    )
    left, right = st.columns([1.1, 0.9], gap="large")
    with left:
        st.markdown(
            """
            <div class="article-shell about-shell">
            """
            + "".join(
                f'<p class="about-paragraph">{get_text(paragraph, language)}</p>' for paragraph in about["paragraphs"]
            )
            + """
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        for focus in about["focuses"]:
            st.markdown(
                f"""
                <div class="feature-card focus-card">
                  <div class="card-meta-label">{'Good fit' if language == 'en' else '適合案型'}</div>
                  <div class="about-title">{get_text(focus, language)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown(
            f"""
            <div class="link-card">
              <div class="card-meta-label">{'Contact' if language == 'en' else '聯絡入口'}</div>
              <div class="about-title">{'快速查看背景與作品' if language == 'zh' else 'Quick links for profile and demos'}</div>
              <div class="contact-link-copy">{"如果你想快速確認合作背景或直接看案例，下面這些入口會最直接。" if language == "zh" else "If you want to review background or jump straight into examples, these are the fastest entry points."}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for group in contact["groups"]:
            for item in group["items"]:
                st.link_button(
                    f'{get_text(item["label"], language)} | {get_text(item["description"], language)}',
                    item["href"],
                    use_container_width=True,
                )
