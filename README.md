# personal-homepage

此專案已重構為以 `Streamlit` 驅動的個人品牌網站，定位為：

- 個人首頁
- 作品展示入口
- 技術筆記與知識內容平台
- 從 Obsidian 發布資料夾同步內容的網站骨架

## 目前功能

- 中英雙語首頁內容切換
- `Home / Projects / Notes / About` 頂部 navigation
- Hero / Services / Featured Projects / Latest Notes / About 區塊
- 筆記列表、搜尋、標籤篩選與文章詳頁
- Markdown + frontmatter 筆記格式
- 支援 Obsidian 常見 `[[wikilink]]` 與 `![[image.png]]`
- Obsidian 發布資料夾同步腳本
- Railway 可用的 Python + Docker 部署流程

## Tech Stack

- Python 3.12
- Streamlit
- Markdown/frontmatter content workflow
- Docker
- Railway

## 本機啟動

```bash
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\streamlit run app.py
```

若你還沒有虛擬環境：

```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\streamlit run app.py
```

## 主要可編輯位置

### 1. 首頁與作品文案

```bash
content/site_content.py
```

適合修改：

- 個人介紹
- 服務內容
- 作品展示
- About 文案
- 外部連結

### 2. 筆記內容

```bash
content/notes/
```

每篇筆記使用 Markdown，支援 frontmatter：

```md
---
title: Example note
summary: 這篇文章的摘要
date: 2026-04-01
slug: example-note
lang: zh
tags:
  - api
  - automation
draft: false
---
```

必要欄位建議至少包含：

- `title`
- `summary`
- `date`

可選欄位：

- `slug`
- `lang`
- `tags`
- `draft`

## Obsidian 同步方式

建議你在 Obsidian vault 中準備一個專門的發布資料夾，例如：

```bash
publish/
```

然後執行：

```bash
.venv\Scripts\python.exe scripts\sync_obsidian_notes.py "C:\path\to\your\vault\publish" --clean
```

這會把：

- Markdown 筆記複製到 `content/notes/`
- 圖片與附件複製到 `static/notes/`

### 發布建議

- 只同步你整理過、確定可公開的內容
- 草稿請保留在 vault 的非發布資料夾
- 若文章不想上站，可加 `draft: true`

## Railway 部署

這個專案現在使用 Python Docker image 啟動 `Streamlit`：

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

部署步驟：

1. Push 到 GitHub。
2. 在 Railway 建立新專案。
3. 選擇從 GitHub repo 部署。
4. Railway 會使用 repo 內的 `Dockerfile` 建置。
5. 建立公開網域後即可瀏覽。

## 專案結構

```bash
personal-homepage/
├─ app.py
├─ content/
│  ├─ site_content.py
│  └─ notes/
├─ homepage/
│  ├─ content_loader.py
│  ├─ note_loader.py
│  └─ ui.py
├─ public/
│  └─ profile.jpg
├─ scripts/
│  └─ sync_obsidian_notes.py
├─ static/
│  └─ notes/
├─ .streamlit/
│  └─ config.toml
├─ Dockerfile
├─ requirements.txt
└─ README.md
```

## Notes

- 目前正式入口為 `app.py`。
- 若未來更重視 SEO、複雜路由與更高程度的品牌客製前端，可再評估改為 Astro 或 Next.js。
