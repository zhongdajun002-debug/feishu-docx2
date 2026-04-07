---
name: feishu-docx2
description: Export and download Feishu/Lark cloud documents. Supports docx, sheets (Markdown/Excel/CSV), bitable, wiki, WeChat article export, drive management, and browser-based export for public or browser-readable docs. Use this skill when you need to read, download, or export content from a Feishu knowledge base.
---

# Feishu Docx Exporter

Export Feishu/Lark cloud documents to Markdown / Excel / CSV for AI analysis and automation.

## Setup (One-time)

```bash
pip install feishu-docx2
feishu-docx2 config set --app-id YOUR_APP_ID --app-secret YOUR_APP_SECRET
```

> Token auto-refreshes. No user interaction required.

### Optional: Browser-Based Export

`export-browser` requires Playwright and a Chromium runtime:

```bash
pip install playwright
playwright install chromium
```

## Export Documents

```bash
feishu-docx2 export "<FEISHU_URL>" -o ./output
```

The exported Markdown file will be saved with the document's title as filename.

### Export Formats

| Format | Flag | Applicable Types | Output |
|--------|------|------------------|--------|
| Markdown (default) | `--format md` | docx, sheet, bitable, wiki | `.md` |
| HTML table | `--table html` | docx (tables only) | `.md` with HTML tables |
| Excel | `--format excel` | sheet | `.xlsx` |
| CSV | `--format csv` | sheet | `.csv` (one file per sheet) |

```bash
# Export spreadsheet as Excel
feishu-docx2 export "https://xxx.feishu.cn/sheets/xxx" --format excel

# Export spreadsheet as CSV
feishu-docx2 export "https://xxx.feishu.cn/sheets/xxx" --format csv

# Export document tables as HTML (better for complex tables)
feishu-docx2 export "https://xxx.feishu.cn/docx/xxx" --table html
```

### Browser-Based Export

If the document is public or only readable in your current browser session:

```bash
feishu-docx2 export-browser "<FEISHU_OR_LARK_URL>" -o ./output

# Reuse an existing Playwright session
feishu-docx2 export-browser "<FEISHU_OR_LARK_URL>" --storage-state ./storage_state.json
```

### Supported Document Types

- **docx**: Feishu cloud documents → Markdown with images
- **sheet**: Spreadsheets → Markdown tables / Excel / CSV
- **bitable**: Multidimensional tables → Markdown tables
- **wiki**: Knowledge base nodes → Auto-resolved and exported
- **public/browser-readable docs**: Browser-based export with local images and attachments

## Command Reference

| Command | Description |
|---------|-------------|
| **Export** | |
| `feishu-docx2 export <URL>` | Export document to Markdown / Excel / CSV |
| `feishu-docx2 export-browser <URL>` | Export in a real browser session with local assets |
| `feishu-docx2 export-wechat <URL>` | Export WeChat article to Markdown |
| `feishu-docx2 export-wiki-space <URL>` | Batch export entire wiki space |
| `feishu-docx2 export-workspace-schema <ID>` | Export bitable database schema |
| **Drive Management** | |
| `feishu-docx2 drive ls` | List app or personal cloud-space files |
| `feishu-docx2 drive rm <TOKEN>` | Delete a file from cloud space |
| `feishu-docx2 drive clear` | Clear files with double confirmation |
| `feishu-docx2 drive perm-show <TOKEN>` | Show public permission settings |
| `feishu-docx2 drive perm-set <TOKEN>` | Update public permission settings |
| `feishu-docx2 drive perm-members <TOKEN>` | List permission members |
| `feishu-docx2 drive perm-add <TOKEN>` | Add a permission member |
| `feishu-docx2 drive perm-update <TOKEN>` | Update a permission member |
| `feishu-docx2 drive perm-rm <TOKEN>` | Remove a permission member |
| **Auth & Config** | |
| `feishu-docx2 auth` | OAuth authorization |
| `feishu-docx2 config set` | Set credentials |
| `feishu-docx2 config show` | Show current config |
| `feishu-docx2 config clear` | Clear token cache |
| `feishu-docx2 tui` | Interactive TUI interface |

## Examples

### Export a wiki page

```bash
feishu-docx2 export "https://xxx.feishu.cn/wiki/ABC123" -o ./docs
```

### Export a document with custom filename

```bash
feishu-docx2 export "https://xxx.feishu.cn/docx/XYZ789" -o ./docs -n meeting_notes
```

### Export spreadsheet as Excel / CSV

```bash
# Export as Excel (.xlsx)
feishu-docx2 export "https://xxx.feishu.cn/sheets/ABC123" --format excel -o ./output

# Export as CSV (one .csv per sheet)
feishu-docx2 export "https://xxx.feishu.cn/sheets/ABC123" --format csv -o ./output
```

### Export a public or browser-readable doc in a real browser session

```bash
feishu-docx2 export-browser "https://xxx.larkoffice.com/wiki/ABC123" -o ./browser_docs
```

### Export with board metadata

```bash
# Include drawing board node metadata (position, size, type)
feishu-docx2 export "https://xxx.feishu.cn/docx/ABC123" --export-board-metadata
```

### Read content directly (recommended for AI Agent)

```bash
# Output content to stdout instead of saving to file
feishu-docx2 export "https://xxx.feishu.cn/wiki/ABC123" --stdout
# or use short flag
feishu-docx2 export "https://xxx.feishu.cn/wiki/ABC123" -c
```

### Batch Export Entire Wiki Space

```bash
# Export all documents in a wiki space (auto-extract space_id from URL)
feishu-docx2 export-wiki-space "https://xxx.feishu.cn/wiki/ABC123" -o ./wiki_backup

# Specify depth limit
feishu-docx2 export-wiki-space "https://xxx.feishu.cn/wiki/ABC123" -o ./docs --max-depth 3
```

### Export Database Schema

```bash
# Export bitable/workspace database schema as Markdown
feishu-docx2 export-workspace-schema <workspace_id>

# Specify output file
feishu-docx2 export-workspace-schema <workspace_id> -o ./schema.md
```

## Manage Drive Files

```bash
# List app cloud-space documents
feishu-docx2 drive ls --auth-mode tenant --type docx

# List personal cloud-space documents
feishu-docx2 drive ls --auth-mode oauth --type docx

# Show public permission
feishu-docx2 drive perm-show "https://xxx.feishu.cn/docx/ABC123"

# List permission members
feishu-docx2 drive perm-members "https://xxx.feishu.cn/docx/ABC123"

# Clear files with double confirmation
feishu-docx2 drive clear --type docx
```

## Tips

- Images and attachments auto-download to `{doc_title}/` folder when local assets are available
- Prefer `export-browser` for public share links or browser-readable docs
- Use `--stdout` or `-c` for direct content output (recommended for agents)
- Use `--format excel` or `--format csv` to export spreadsheets in native formats
- Use `--export-board-metadata` to include drawing board node metadata
- Token auto-refreshes, no re-auth needed
- For Lark (overseas): add `--lark` flag
- `tenant_access_token` manages app cloud space, `user_access_token` manages personal cloud space
