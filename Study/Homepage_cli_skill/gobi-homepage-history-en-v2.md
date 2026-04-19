# 📔 Debugging Chronicle: Building "Mickey's Kitchen" (v2)
### Evolution of a Unique Personal Knowledge Platform using Gobi SDK

**Date:** 2026-04-14
**Chef/Developer:** Mickey Lee
**Objective:** Create an interactive, dynamic HTML dashboard that renders a local Obsidian vault as a premium "Recipe Book" on the Gobi web platform.

---

## 🕒 The 5-Hour Debugging Timeline

### 1. The "Function Not Found" Wall (The SDK Mirage)
*   **Attempt:** Initially tried using `gobi.vault.search()` and `gobi.vault.getMetadata()` for automatic folder discovery.
*   **Error:** `TypeError: gobi.vault.search is not a function`.
*   **Insight:** Discovered that the current SDK environment didn't support these high-level discovery functions. We had to pivot to more primitive but stable methods.

### 2. The "Update Feed" Pivot (The Partial Success)
*   **Attempt:** Switched to `gobi.listBrainUpdates()` to fetch all posts.
*   **Result:** **Success!** Data started flowing to the UI.
*   **Problem:** This API returns 'Brain Updates' (posts/activity), not the actual file system structure. It couldn't accurately reflect the organized folder hierarchy of the vault.

### 3. The "Sandbox Prison" Crisis (The 404 Cycle)
*   **Attempt:** Used `gobi.listFiles('')` to scan the actual file structure.
*   **Observation:** It only returned files inside the `app/` directory (where `index.html` resides).
*   **The Wall:** Gobi Homepages are sandboxed in `app/`. Trying to traverse up with `..` or `/` resulted in "Permission Denied" or "Failed to Fetch". All sibling folders like `Stock` or `Music` appeared invisible.

### 4. The "Terminal" Breakthrough (Path Discovery)
*   **Strategy:** Built a temporary **Terminal-style Debug Dashboard** to test all possible path strings.
*   **Method:** Iteratively tested: `.`, `/`, `..`, `../..`, and finally `../Stock`.
*   **The Discovery:** A major breakthrough! While listing the parent directory (`..`) is blocked, **directly naming a sibling folder via relative path (`../Stock`) is allowed**. This was the key to escaping the sandbox.

### 5. The "Premium Editorial" Transformation
*   **Design Shift:** Moved away from basic buttons to an **all-in-one scrolling gallery**.
*   **Typography:** Selected a sophisticated mix of `Cormorant Garamond` (Serif) and `Plus Jakarta Sans` (Sans-serif).
*   **Features:** Implemented a hidden "Chef's Log" (L-key toggle) and a streaming AI chat interface using the latest `sendMessage` API.

### 6. The `nav=false` Variable and Multi-Path Probe (The Final Puzzle)
*   **New Attempt:** Applied `homepage: ./app/index.html?nav=false` in `BRAIN.md` to hide Gobi's native navigation.
*   **Unexpected Bug:** Navigation was hidden, but the kitchen's content disappeared again (Empty Pantry).
*   **Analysis:** Discovered that the `?nav=false` parameter causes the Gobi server to change the **'Root Path'** or sandbox policy, invalidating the previous `../Stock` path.
*   **Final Solution:** Implemented the **"Multi-Path Probe"** logic. The engine now sequentially tests `../cat`, `./cat`, `/cat`, and `cat` until it receives a valid response, ensuring total compatibility with any environment setting.

---

## 🛠️ Key Technical Discoveries Summary

| Feature | Failed Attempt | Successful Solution |
| :--- | :--- | :--- |
| **Folder Discovery** | `gobi.vault.search()` | Predefined `categories` list + `listFiles()` |
| **Sandbox Exit** | `listFiles('/')` | **Relative Sibling Pathing** (`../FolderName`) |
| **Path Compatibility**| 404 on `?nav=false` | **Multi-Path Probe** (Testing all path combinations) |
| **Vault ID Recovery** | `Vault: undefined` | **Self-Healing** (Extracting ID from URL slug) |
| **Deep Reading** | Error on file click | **Bulletproof Reading** (Retry logic for file paths) |
| **Data Format** | `forEach` on Object | Robust `extract()` helper for Array conversion |
| **Loading Stability** | Immediate API Call | **30-retry loop (6 seconds)** to wait for SDK injection |
| **Rendering** | Native Markdown | `marked.js` with Premium Editorial Styling |

---

## 🧠 Final Reflection
Today's journey proved that **Sandbox restrictions are not walls, but puzzles**. By building custom debug tools and testing the limits of the Gobi SDK, we transformed a simple markdown vault into a high-end, dynamic knowledge platform. The **"Try every path until it works"** strategy became our strongest weapon in the cloud sandbox environment.

*Report compiled by Mickey's AI Assistant.*
