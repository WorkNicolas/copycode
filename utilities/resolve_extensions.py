"""_summary_
Allows the user to use extension sets like /web, /py, etc.
Not relevant for adding anything to it.
"""
from copycode.config.extension_sets import EXTENSION_SETS

def resolve_extensions(input_list):
    """Resolves a list of mixed extensions (e.g., 'js', '/web') into a set of extensions."""
    resolved_set = set()
    for item in input_list:
        if item.startswith('/'):
            if item in EXTENSION_SETS:
                resolved_set.update(EXTENSION_SETS[item])
            else:
                print(f"⚠️  Warning: Extension set '{item}' not found. Ignoring.")
        else:
            resolved_set.add(f".{item.lstrip('.')}")
    return resolved_set