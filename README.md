# Personal Homepage

以 Streamlit 建立的個人作品集網站，包含 Home、Projects、Notes 與 About 四個頁面，支援中文及英文介面。網站內容集中在 Python 資料檔與 Markdown 筆記，方便直接維護。

## 本機啟動

建議使用 Python 3.12，與專案 Dockerfile 的版本一致。請先進入專案根目錄，再於 PowerShell 執行：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

啟動後開啟終端顯示的網址；預設為 `http://localhost:8501`。按 `Ctrl+C` 停止服務。

上述指令直接使用虛擬環境內的 Python，不需要另外啟用 PowerShell 的環境啟動腳本。本機執行不需要雲端主機帳號。

目前唯一列出的第三方依賴為 `streamlit>=1.41,<2.0`，以 `requirements.txt` 為準。

## 專案結構

```text
app.py                         網站入口、語言狀態、頁面與筆記導覽
content/site_content.py         個人介紹、作品及中英文網站文字
content/notes/                 Markdown 筆記
homepage/content_loader.py     網站內容與語言文字讀取
homepage/note_loader.py        筆記中繼資料、排序、連結與圖片處理
homepage/ui.py                 各頁面的畫面與樣式
public/profile.jpg             個人照片
static/notes/                  筆記附圖與素材
scripts/sync_obsidian_notes.py 公開筆記同步工具
.streamlit/config.toml         主題與導覽設定
Dockerfile                    容器建置與啟動設定
```

## 修改網站內容

- 個人介紹、作品與介面文字：修改 `content/site_content.py` 中的 `SITE_CONTENT`。
- 中英文文字：沿用既有 `zh`、`en` 欄位。文字讀取會優先使用選定語言，再依序回退至中文、英文。
- 個人照片：替換 `public/profile.jpg`。
- 版面與樣式：修改 `homepage/ui.py`；主題設定位於 `.streamlit/config.toml`。
- 外部作品連結：在 `content/site_content.py` 維護。連結目標是否仍可使用，需另外確認。

## 新增筆記

在 `content/notes/` 建立 UTF-8 編碼的 `.md` 檔案，例如 `my-note.md`：

```markdown
---
title: 我的筆記
summary: 這篇筆記的簡短介紹。
date: 2026-10-26
slug: my-note
tags: [Python, 自動化]
lang: zh
draft: false
---

# 我的筆記

在這裡撰寫內容。
```

筆記讀取器支援上述單層欄位、布林值與簡單清單，並非完整的 YAML 解析器。Front matter 需以獨立一行的 `---` 開始及結束。

- `draft: true` 的筆記不會顯示。
- 未提供 `date` 或日期無法解析時，會使用檔案修改日期。
- 未提供 `slug` 時，會從檔名產生；請讓不同筆記使用不同的 slug。
- 筆記按日期及標題反向排序，首頁取排序後的前三篇。
- `lang` 記錄筆記語言，不會自動翻譯內文。

筆記連結可使用 `[[另一篇筆記]]` 或 `[[另一篇筆記|顯示文字]]`。圖片可使用 Markdown 圖片語法或 Obsidian 的 `![[圖片檔名]]`，素材放在筆記旁或 `static/notes/`。

## 從 Obsidian 匯入公開筆記

先準備一個只含可公開內容的資料夾，再將以下來源參數替換為該資料夾路徑：

```powershell
.\.venv\Scripts\python.exe scripts/sync_obsidian_notes.py "<公開筆記資料夾>"
```

預設將 Markdown 複製到 `content/notes/`，其他檔案複製到 `static/notes/`，並保留來源的相對目錄。可用 `--target-notes` 與 `--target-assets` 指定其他目的地。

同步時，同一路徑的既有檔案會被覆寫；來源已移除的檔案不會自動從目的地移除。`--clean` 會先刪除兩個目的資料夾的既有內容，再執行複製，使用前應先確認路徑並完成備份。

工具會複製來源資料夾內的檔案，並不會自動檢查敏感內容或依 `draft` 篩選同步項目。請勿將整個私人 Obsidian Vault 作為來源；送出版本控制前，應自行檢查同步結果。

## 使用 Docker 在本機執行

安裝並啟動 Docker 後，在專案根目錄執行：

```powershell
docker build -t personal-homepage .
docker run --rm -p 8501:8501 personal-homepage
```

預設使用 `http://localhost:8501`。Dockerfile 以 Python 3.12 為基底，容器內的 `PORT` 預設為 `8501`；若調整該值，也需同步調整連接埠對應。

## 手動檢查

目前 Repository 未附自動化測試套件或 GitHub Actions 流程。修改後可依序確認：

1. Home、Projects、Notes、About 均可開啟。
2. 切換中文與英文後，導覽及主要文字正常顯示。
3. 筆記能開啟，圖片與站內連結正常。
4. 草稿筆記不會顯示；沒有筆記時，Notes 頁仍可操作。
5. 作品連結符合目前要展示的內容。

## 公開資料與本機設定

網站會讀取 `SITE_CONTENT`、筆記與素材，加入前請確認內容可公開。`.gitignore` 已排除 `.venv/`、`.env` 與 `.env.*`；已被 Git 追蹤的檔案不會因新增忽略規則而自動停止追蹤。

目前 Docker 建置排除 `.streamlit/secrets.toml`，但 Git 忽略規則未明確排除該檔案。若未來需要新增敏感設定，應先補妥忽略規則並確認不會納入 Git 或建置內容。
