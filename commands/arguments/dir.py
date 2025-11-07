# copycode/commands/arguments/dir.py

import pyperclip
from pathlib import Path
import pathspec
from copycode.config.extension_sets_union import DEFAULT_ALLOWED_EXTENSIONS
from copycode.config.ignored_extensions import DEFAULT_IGNORED_FILES
from copycode.config.ignored_folders import DEFAULT_IGNORED_FOLDERS
from copycode.utilities.is_path_ignored import is_path_ignored
from copycode.utilities.resolve_extensions import resolve_extensions
from copycode.utilities.print_model_fit import print_model_fit_summary

def handle_dir_command(args):
    """Handle the --dir command with optional filtering."""
    modes = set([m.lower() for m in args.dir]) if args.dir else set()
    less_mode = "/less" in modes or "less" in modes
    no_print = "/no_print" in modes or "no_print" in modes
    target_folders = [m for m in args.dir if not m.startswith("/") and not m.lower().endswith("less") and not m.lower().endswith("no_print")]

    # Setup filtering (similar to copy_files.py)
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

    def list_dir_recursive(base_paths):
        paths = []
        for base in base_paths:
            base_path = Path(base)
            if not base_path.exists():
                print(f"⚠️  Skipping non-existent path: {base_path}")
                continue
            for path in base_path.rglob("*"):
                path_str = path.as_posix()
                
                # Apply filtering
                if gitignore_spec and gitignore_spec.match_file(path_str):
                    continue
                if is_path_ignored(path, ignored_folders, ignored_files):
                    continue
                if path.is_file() and allowed_extensions is not None:
                    if path.name.lower() == "makefile" and "makefile" in allowed_extensions:
                        pass
                    elif path.suffix not in allowed_extensions:
                        continue
                
                paths.append(path.resolve().as_posix())
        return paths

    # Determine what to scan
    if target_folders:
        paths = list_dir_recursive(target_folders)
    else:
        all_paths = []
        for path in Path(".").rglob("*"):
            path_str = path.as_posix()
            
            # Apply filtering
            if gitignore_spec and gitignore_spec.match_file(path_str):
                continue
            if is_path_ignored(path, ignored_folders, ignored_files):
                continue
            if path.is_file() and allowed_extensions is not None:
                if path.name.lower() == "makefile" and "makefile" in allowed_extensions:
                    pass
                elif path.suffix not in allowed_extensions:
                    continue
            
            all_paths.append(path.resolve().as_posix())
        paths = sorted(all_paths)

    # Group mode
    if less_mode:
        last_prefix = None
        similar_group_count = 0
        output_lines = []
        for path in paths:
            name = Path(path).name.lower()
            prefix = name[:5] if len(name) >= 5 else name
            if prefix == last_prefix:
                similar_group_count += 1
                continue
            else:
                if similar_group_count > 0:
                    output_lines.append(f"# {similar_group_count + 1} files had similar naming (prefix '{last_prefix}')")
                    similar_group_count = 0
                output_lines.append(path)
                last_prefix = prefix
        if similar_group_count > 0:
            output_lines.append(f"# {similar_group_count + 1} files had similar naming (prefix '{last_prefix}')")
    else:
        output_lines = [p for p in paths]

    final_output = "\n".join(output_lines)
    pyperclip.copy(final_output)

    if not no_print:
        print("Recursive directory listing:\n" + "-" * 40)
        print(final_output)
        print("-" * 40)

    total_chars = len(final_output)
    total_lines = final_output.count("\n") + 1
    est_tokens = total_chars // 4
    print(f"Total characters copied: {total_chars:,}")
    print(f"Total lines copied: {total_lines:,}")
    print(f"Estimated tokens: ~{est_tokens:,}")

    print_model_fit_summary(total_chars)

    print("\nCopied directory listing to clipboard.")