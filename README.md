# personal-homepage

A bilingual React personal homepage for **Dexter Chang**, prepared for:

- GitHub source control
- Railway deployment
- future expansion into a fuller freelance portfolio site

此專案是為 **Dexter Chang** 製作的中英雙語 React 個人首頁，已整理成適合：

- 放到 GitHub 管理版本
- 部署到 Railway
- 後續持續擴充成完整接案型作品網站

## Current Features / 目前內容

- bilingual Chinese / English toggle
- personal photo hero section
- profile intro and service focus
- featured GitHub + live demo links
- reusable component structure
- content stored in a single data file for easy editing
- Dockerfile + Caddyfile ready for Railway

## Tech Stack

- React
- Vite
- plain CSS
- Caddy (for production static serving in Railway)
- Docker multi-stage build

## Project Name

This repo is set to:

```bash
personal-homepage
```

## Local Development

```bash
npm install
npm run dev
```

## Production Build

```bash
npm run build
npm run preview
```

## Deploy to Railway from GitHub

1. Push this project to a GitHub repository.
2. In Railway, create a new project.
3. Choose **Deploy from GitHub repo**.
4. Select this repository.
5. Wait for the build and deployment to finish.
6. In the Railway service settings, generate a public domain.

This project already includes:

- `Dockerfile`
- `Caddyfile`
- `.dockerignore`
- `.gitignore`

so the deployment setup is already prepared.

## Recommended Files to Edit First

### 1. Main content / 主要文案

```bash
src/data/siteContent.js
```

Edit here when you want to update:

- intro text
- project cards
- links
- service descriptions
- navigation labels

### 2. Photo / 照片

```bash
public/profile.jpg
```

### 3. Metadata / 網頁標題與描述

```bash
index.html
```

## Project Structure

```bash
personal-homepage/
├─ public/
│  ├─ favicon.svg
│  └─ profile.jpg
├─ src/
│  ├─ components/
│  ├─ data/
│  │  └─ siteContent.js
│  ├─ App.jsx
│  ├─ main.jsx
│  └─ styles.css
├─ Caddyfile
├─ Dockerfile
├─ .dockerignore
├─ .gitignore
├─ index.html
├─ package.json
└─ vite.config.js
```

## Suggested Next Sections

You can extend this site later with:

- services page
- resume download section
- contact form
- testimonials
- case studies
- FAQ
- pricing or engagement flow

## Notes

- No license file is included by default.
- If you want to open-source this repo later, add a license intentionally.
- If you want to use a custom domain on Railway, connect the domain after deployment.
