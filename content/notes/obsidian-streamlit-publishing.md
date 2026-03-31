---
title: Obsidian publishing flow for a Streamlit portfolio
summary: 說明如何把 Obsidian 中整理好的發布資料夾同步到 Streamlit 網站，並控制公開範圍、圖片資產與內部連結。
date: 2026-03-28
slug: obsidian-streamlit-publishing
lang: zh
tags:
  - obsidian
  - streamlit
  - publishing
---

# Obsidian publishing flow

這個網站的筆記內容不是直接讀整個 vault，而是只讀你整理過的發布資料夾。這樣做有幾個好處：

- 不會把草稿或私人筆記直接暴露出去。
- 可以保留 Obsidian 當成日常工作區，再把可公開內容同步進 repo。
- 正式部署時只依賴 repo 內的內容，不依賴你本機的 vault 結構。

同步後，網站端會處理 Obsidian 常見語法，例如：

- `[[api-integration-checklist]]` 這種 wikilink 會轉成站內筆記連結。
- `![[automation-workflow.svg]]` 這種嵌入圖片會轉成可顯示的內嵌圖。

![[automation-workflow.svg]]

這種流程很適合內容型個人品牌網站，因為你可以先在 Obsidian 中整理思路，再選擇哪些內容要正式發布。
