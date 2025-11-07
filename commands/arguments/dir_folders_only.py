# copycode/commands/arguments/dir_folders_only.py

import pyperclip
from pathlib import Path
import pathspec
from copycode.config.ignored_folders import DEFAULT_IGNORED_FOLDERS
from copycode.utilities.is_path_ignored import is_path_ignored
from copycode.utilities.print_model_fit import print_model_fit_summary

def handle_dir_folders_only(args):
    """Handle the --dir-folders-only command with optional filtering."""
    modes = set([m.lower() for m in args.dir_folders_only]) if args.dir_folders_only else set()
    less_mode = "/less" in modes or "less" in modes
    no_print = "/no_print" in modes or "no_print" in modes

    # Setup filtering (folder-specific)
    gitignore_spec = None
    ignored_folders = set()

    if args.all:
        print("Including all folders (--all). .gitignore will also be bypassed.")
    else:
        ignored_folders = DEFAULT_IGNORED_FOLDERS.copy()

        # Process inclusions
        for folder in args.add_folder:
            ignored_folders.discard(folder)

        # Process exclusions
        for folder in args.ignore_folders:
            ignored_folders.add(folder)

        # Load .gitignore patterns
        gitignore_patterns = []
        gitignore_path = Path(".gitignore")
        if gitignore_path.is_file():
            print("Loading patterns from .gitignore...")
            with gitignore_path.open("r", encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    try:
                        pathspec.PathSpec.from_lines("gitwildmatch", [line])
                        gitignore_patterns.append(line)
                    except Exception as e:
                        print(f"⚠️  Skipping invalid .gitignore pattern on line {i}: {line} ({e})")
        gitignore_patterns.append(".git/")
        gitignore_spec = pathspec.PathSpec.from_lines("gitwildmatch", gitignore_patterns)

    if less_mode:
        # Top-level folders only, space-separated output
        folders = []
        for f in Path(".").iterdir():
            if not f.is_dir():
                continue
            
            # Apply filtering
            path_str = f.as_posix()
            if gitignore_spec and gitignore_spec.match_file(path_str):
                continue
            if f.name in ignored_folders:
                continue
            
            folders.append(f.name)
        
        final_output = " ".join(sorted(folders))
    else:
        # Recursive all folders, full path
        folders = []
        for p in Path(".").rglob("*"):
            if not p.is_dir():
                continue
            
            # Apply filtering
            path_str = p.as_posix()
            if gitignore_spec and gitignore_spec.match_file(path_str):
                continue
            if is_path_ignored(p, ignored_folders, set()):
                continue
            
            folders.append(p.resolve().as_posix())
        
        final_output = "\n".join(folders)

    pyperclip.copy(final_output)

    if not no_print:
        print("Folder listing:\n" + "-" * 40)
        print(final_output)
        print("-" * 40)

    total_chars = len(final_output)
    total_lines = final_output.count("\n") + 1
    est_tokens = total_chars // 4
    print(f"Total characters copied: {total_chars:,}")
    print(f"Total lines copied: {total_lines:,}")
    print(f"Estimated tokens: ~{est_tokens:,}")

    print_model_fit_summary(total_chars)

    print("\nCopied folder listing to clipboard.")