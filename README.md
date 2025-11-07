# copycode 📋✨

A small CLI to walk your project, pick out the files that matter, format them as Markdown code blocks, and copy everything straight to your clipboard — perfect for pasting into an LLM/chat, PR review, or docs.

---

## 🚀 What it does

* Recursively scans the current directory (`.`)
* Respects `.gitignore` (unless you tell it not to)
* Filters by **extension sets** (e.g. `/py`, `/web`, `/config`)
* Skips noisy folders/files by default (`node_modules`, `.git`, build dirs, lockfiles…)
* Emits output like:

```markdown
# --- path/to/file.py ---

<file contents>
```

* Copies the whole thing to your clipboard and prints a size/model-fit summary

---

## 📦 Installation

This repo is structured as a package:

```bash
python -m copycode
```

or, if installed as a console script:

```bash
copycode
```

The entrypoint is `copycode.__main__.py`, which wires the CLI to the subcommands.

If you install the release, do this:

**Windows**
Place `copycode.exe` (or the installed script) in your Python `Scripts` folder, for example:
`C:\Users\<your-username>\AppData\Local\Programs\Python\Python312\Scripts`
Make sure that folder is in your `PATH`.

**Linux**
Place the executable/script in `~/.local/bin/` (per-user) or `/usr/local/bin/` (system-wide):

```bash
chmod +x ~/.local/bin/copycode
```

Ensure that directory is in `$PATH`.

**macOS**
Place it in `/usr/local/bin/` (Intel) or `/opt/homebrew/bin/` (Apple Silicon):

```bash
chmod +x /usr/local/bin/copycode
```

Make sure that directory is in your shell’s `PATH`.

---

## 🧠 Core idea

You rarely want *everything* in a repo. You want “the source”, “the config”, “the docs” — but not caches, build output, or lockfiles. `copycode` encodes this as:

1. **Allowed extensions** → from `config/extension_sets.py` and `extension_sets_union.py`
2. **Ignored folders/files** → from `config/ignored_folders.py` and `config/ignored_extensions.py`
3. **Optional overrides** → CLI flags to add/remove extensions/folders
4. **.gitignore-aware** → reads `.gitignore` and applies it via `pathspec`

So you get a clean, LLM-friendly dump.

---

## 🧬 CLI overview

The CLI is defined in `commands/parser.py`.

```text
copycode                         # Copy all default file types
copycode -a                      # Copy absolutely ALL files
copycode -ls                     # List available extension sets
copycode -d                      # List files/folders (respecting filters)
copycode -dfo                    # List folders only
```

### Top-level commands

* **(default)** → copy filtered files to clipboard
  → `handle_copy_files(...)`
* **`-ls` / `--list-sets`** → list extension sets
  → `handle_list_sets(...)`
* **`-d` / `--dir`** → print directory listing (files + folders, filtered)
  → `handle_dir_command(...)`
* **`-dfo` / `--dir-folders-only`** → print folder listing only
  → `handle_dir_folders_only(...)`

If none of those are present, it falls back to copying files.

---

## 🛠 Flags (filters & overrides)

These flags are shared across commands and mirror the logic from `copy_files.py` and the dir commands.

| Flag                         | Meaning                                                             |
| ---------------------------- | ------------------------------------------------------------------- |
| `-a`, `--all`                | Include **everything**, bypass `.gitignore`, ignore extension rules |
| `-ae`, `--add-extension`     | Add extensions or extension sets to include (e.g. `.txt`, `/py`)    |
| `-af`, `--add-folder`        | Force-include folders that are ignored by default                   |
| `-ie`, `--ignore-extensions` | Remove extensions or extension sets from the allowed set            |
| `-if`, `--ignore-folders`    | Add folders to the ignore list                                      |

Examples:

```bash
# Add all Python AND web files on top of defaults
copycode -ae /py /web

# Copy everything, even generated stuff
copycode --all

# Ignore CSS and JS
copycode -ie .css .js

# Include .vscode even though it's ignored by default
copycode -af .vscode
```

---

## 📚 Extension sets

Run:

```bash
copycode -ls
```

to see all configured sets (from `config/extension_sets.py`), e.g.:

* `/py` → Python*
* `/web` → TS/JS/CSS/HTML/JSON/SVG…
* `/config` → YAML/TOML/INI/env
* `/docs` → Markdown, reST, AsciiDoc
* `/sql`, `/gql`, `/idl`, `/script`, …

You can use them anywhere an extension is accepted:

```bash
copycode -ae /py
copycode -ie /web
```

If you reference a non-existent set, it warns and continues.

---

## 🗂 Directory commands

Sometimes you just want to see *what* would be copied.

### 1. `--dir`

```bash
copycode --dir
```

* Recursively lists files/folders
* Applies the **same filters** as the copy step
* Copies the listing to clipboard
* Prints model-fit

Modifiers:

* `/less` → groups “similar” names to reduce noise
* `/no_print` → still copies to clipboard, but doesn’t print to stdout

```bash
copycode --dir /less
copycode --dir src /less
```

You can also pass target folders:

```bash
copycode --dir src backend
```

### 2. `--dir-folders-only`

```bash
copycode --dir-folders-only
```

* Only folders
* Same filtering
* `/less` → only top-level folders, space-separated
* `/no_print` → quiet

---

## 📋 Copying logic (default mode)

`commands/copy_files.py` does the heavy lifting:

1. Build **allowed extensions** (unless `--all`)

2. Load `.gitignore` and turn it into a `pathspec`

3. Walk `Path(".").rglob("*")`

4. For each file that:

   * isn’t ignored by `.gitignore`
   * isn’t in `DEFAULT_IGNORED_FOLDERS`
   * isn’t in `DEFAULT_IGNORED_FILES`
   * **and** matches an allowed extension
     → emit a Markdown block:

   ```markdown
   # --- path/to/file.ext ---
   <file contents>
   ```

5. Concatenate all parts with blank lines

6. Copy to clipboard (`pyperclip.copy(...)`)

7. Print counts and estimated tokens

8. Print model-context fit via `utilities/print_model_fit.py`

If a file can’t be read, the block contains an error line but the process continues.

---

## 🧾 .gitignore behavior

* If `.gitignore` exists at project root, it’s loaded
* Each non-comment, non-empty line is added to the matcher
* Invalid patterns are skipped with a warning
* `.git/` is always ignored
* `--all` bypasses this whole part

This makes the output match what you actually keep in version control.

---

## 📊 Model-fit summary

At the end of a run, you’ll see something like:

```text
Processed 17 files.
Total characters copied: 42,381
Total lines copied: 1,204
Estimated tokens: ~10,595

Model fit summary:
OpenAI GPT-4o/GPT-5: ✅ within
Claude 3.5 Sonnet:    ✅ within
Gemini 1.5 Pro:       ✅ within
Grok-2:               ✅ within
Meta LLaMA 3.1:       ✅ within
```

That comes from `utilities/print_model_fit.py` and is based on a simple `chars // 4` token estimate.

---

## 🧩 Modules (map)

* `__main__.py` → CLI entrypoint
* `commands/parser.py` → defines all args
* `commands/copy_files.py` → main copy logic
* `commands/arguments/dir.py` → `--dir`
* `commands/arguments/dir_folders_only.py` → `--dir-folders-only`
* `commands/arguments/list_sets.py` → `-ls`
* `config/*.py` → extension sets + default ignore lists
* `utilities/*.py` → helpers (ignore check, set resolution, printing)

Everything is under the `copycode` package, so imports look like:

```python
from copycode.commands.parser import parser
from copycode.utilities.resolve_extensions import resolve_extensions
```

---

## 🧪 Example sessions

```bash
# 1) Basic: copy “interesting” files only
copycode

# 2) Copy everything, even build output
copycode --all

# 3) Explore what would be copied
copycode --dir /less

# 4) See all extension groups, then pick one
copycode --list-sets
copycode -ae /py

# 5) Copy defaults but exclude web assets
copycode -ie /web
```

---

## ⚙️ Requirements

* Python 3.8+
* `pyperclip`
* `pathspec`

Clipboard support depends on your OS; on some Linux distros you may need `xclip`/`xsel`.

---

## ✅ Summary

* 📁 Walks the repo
* 🧹 Filters smartly
* 🧱 Emits Markdown blocks
* 📎 Copies to clipboard
* 🧪 Gives you model-fit info

Drop this into any project and you’ve got a one-liner to “show the LLM the code.”
