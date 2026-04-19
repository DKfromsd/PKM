---
title: "Gobi Homepage 101: A Beginner's Guide to Digital Brains"
tags: [Gobi, SDK, Tutorial, PKM, Debugging]
description: "How to transform your Gobi vault into a premium interactive dashboard."
thumbnail: ./Attachments/thumb.jpg
---

# 🎓 Gobi Homepage 101: Building Your Digital Brain

Welcome to the world of **Gobi Space**! If you've seen beautiful, interactive vaults like [Mickey's Kitchen](https://gobispace.com/@mickeyfromsd) or [@jyk](https://gobispace.com/@jyk) and wondered how to start, this guide is for you.

This document synthesizes our hours of debugging and development into a simple 5-step roadmap for new users.

---

## 🛠️ Step 1: Initialize Your Vault

Before you build a homepage, you need a vault.

1.  **Local Folder**: Create a folder on your Mac (e.g., `Documents/My_Gobi_Vault`).
2.  **Gobi CLI**: Open your terminal and run:
    ```bash
    cd [Your-Folder-Path]
    gobi init
    ```
3.  **Sync**: Start syncing your files to the cloud:
    ```bash
    gobi sync
    ```

---

## 🖼️ Step 2: Activating the "Homepage Skill"

Gobi allows you to replace the default file list with a custom HTML page.

1.  **Create the App Folder**: Inside your vault root, create an `app/` folder.
2.  **Create index.html**: Place your HTML/JS code inside `app/index.html`.
3.  **Link in BRAIN.md**: Open (or create) `BRAIN.md` in your vault root and add this frontmatter:
    ```yaml
    ---
    homepage: ./app/index.html?nav=false
    ---
    ```
    *   `?nav=false`: Hides the Gobi sidebar for a clean, full-screen look.

---

## 🧩 Step 3: Understanding the Gobi SDK

Your `index.html` can talk to your vault using the **Gobi SDK**. Here are the most essential functions we discovered:

- `gobi.listBrainUpdates()`: Fetches recent posts and updates.
- `gobi.listFiles(path)`: Scans your folder structure for files.
- `gobi.renderMarkdown(content)`: Converts your `.md` files into beautiful HTML.
- `gobi.sendMessage(prompt)`: Connects your page to Gobi's AI agent for chat features.

---

## 🔍 Step 4: The Debugging Masterclass (Pro Tips)

This is where most beginners get stuck. Here are the "Aha!" moments from our development:

### 1. The Sandbox Prison 🧱
Your `index.html` is executed inside the `app/` folder. For security, Gobi blocks you from listing the root directory (`/`).
*   **The Fix**: You cannot see the parent, but you can "shout" to a sibling! Use **Relative Sibling Paths** like `../Stock` or `../Music` to access your content.

### 2. The `?nav=false` Paradox 🔄
Applying `nav=false` changes the way the Gobi server perceives your "Root Path".
*   **The Fix**: Use a **Multi-Path Probe** strategy. Have your code try multiple paths in order:
    1. `../FolderName`
    2. `./FolderName`
    3. `/FolderName`
    *   *If one fails, try the next until the data flows!*

### 3. The "Self-Healing" Vault ID 🩹
Sometimes the SDK loses track of which vault it belongs to (returns `undefined`).
*   **The Fix**: Extract the ID directly from the URL slug (e.g., the `@mickeyfromsd` part) and manually inject it into your requests.

---

## 🎨 Step 5: Aesthetics & Polishing

To get that premium "@jyk style" or "Mickey's Kitchen" look:

1.  **Typography**: Use Google Fonts like `Playfair Display` for titles and `Montserrat` for a modern feel.
2.  **Card Layout**: Use CSS Flexbox or Grid. Add a `transition` and a `box-shadow` to your cards to make them "pop" when hovered.
3.  **One-Page Flow**: Instead of many buttons, let the user scroll through sections (Stock -> Music -> Thoughts).

---

## ✅ Final Success Checklist

- [ ] Does your `index.html` wait for the SDK? (Use a 6-second retry loop).
- [ ] Are your file paths using the `../` prefix to escape the `app/` folder?
- [ ] Have you run `gobi sync` and `gobi brain publish` to see changes online?
- [ ] Did you include a **Disclaimer** for any financial or specialized advice?

> "Sandbox restrictions are not walls, but puzzles." — *Mickey's Kitchen Dev Team*

---
## 📚 References
For more details, see our internal technical logs:
- `![[Study/Homepage_cli_skill/홈페이지 구축 - 101 gobispace cli v2.md]]`
- `![[Study/Homepage_cli_skill/gobi-homepage-history-en-v2.md]]`

🚀 **Happy Cooking (Developing)!**
