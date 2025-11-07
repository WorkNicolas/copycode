"""_summary_
Boolean for checking -ie and -if.
"""

def is_path_ignored(path, ignore_folders, ignore_files):
    """Checks if a path should be ignored based on folder and file lists."""
    if path.name in ignore_files:
        return True
    if any(part in ignore_folders for part in path.parts):
        return True
    return False