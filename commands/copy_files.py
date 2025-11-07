"""_summary_
Copying output logic.
"""

# commands/copy_files.py
from pathlib import Path
import pathspec
import pyperclip
from copycode.config.extension_sets_union import DEFAULT_ALLOWED_EXTENSIONS
from copycode.config.ignored_extensions import DEFAULT_IGNORED_FILES
from copycode.config.ignored_folders import DEFAULT_IGNORED_FOLDERS
from copycode.utilities.is_path_ignored import is_path_ignored
from copycode.utilities.resolve_extensions import resolve_extensions
from copycode.utilities.print_model_fit import print_model_fit_summary

def handle_copy_files(args):
    """Handle the file copying logic, applying filters and copying to clipboard."""
    gitignore_spec = None
    allowed_extensions = None
    ignored_folders = set()
    ignored_files = set()

    if args.all:
        print("Including all files and folders (--all). .gitignore will also be bypassed.")
    else:
        allowed_extensions = DEFAULT_ALLOWED_EXTENSIONS.copy()
        ignored_folders = DEFAULT_IGNORED_FOLDERS.copy()
        ignored_files = DEFAULT_IGNORED_FILES.copy()

        # Process inclusions
        extensions_to_add = resolve_extensions(args.add_extension)
        allowed_extensions.update(extensions_to_add)
        for folder in args.add_folder:
            ignored_folders.discard(folder)

        # Process exclusions
        extensions_to_ignore = resolve_extensions(args.ignore_extensions)
        allowed_extensions.difference_update(extensions_to_ignore)
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

    output_parts = []
    processed_files = 0
    print("\nFiles copied:\n" + "-" * 40)

    for path in Path(".").rglob("*"):
        path_str = path.as_posix()
        if gitignore_spec and gitignore_spec.match_file(path_str):
            continue
        if is_path_ignored(path, ignored_folders, ignored_files):
            continue
        if path.is_file():
            if allowed_extensions is not None:
                if path.name.lower() == "makefile" and "makefile" in allowed_extensions:
                    pass
                elif path.suffix not in allowed_extensions:
                    continue
            print(path_str)
            output_parts.append("```")
            output_parts.append(f"# --- {path_str} ---")
            try:
                output_parts.append(path.read_text(encoding="utf-8"))
            except Exception as e:
                output_parts.append(f"Error reading file: {e}")
            output_parts.append("```")
            processed_files += 1

    if output_parts:
        final_output = "\n\n".join(output_parts)
        pyperclip.copy(final_output)
        total_chars = len(final_output)
        total_lines = final_output.count("\n") + 1
        est_tokens = total_chars // 4
        print("-" * 40)
        print(f"\nProcessed {processed_files} files.")
        print(f"Total characters copied: {total_chars:,}")
        print(f"Total lines copied: {total_lines:,}")
        print(f"Estimated tokens: ~{est_tokens:,}")
        
        print_model_fit_summary(total_chars)
    else:
        print("No matching files found to process.")