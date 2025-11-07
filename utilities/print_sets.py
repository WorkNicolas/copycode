"""_summary_
copycode -ie /web /py
- ignores extension sets from /web and /py

Applies to all other arguments. Check --help for more info.
"""
from copycode.config.extension_sets import EXTENSION_SETS

def print_sets(requested_sets):
    """Prints the specified extension sets, or all if none are specified."""
    sets_to_print = {}
    if not requested_sets:  # User typed just '-ls'
        sets_to_print = EXTENSION_SETS
    else:  # User typed '-ls /web /py'
        for set_name in requested_sets:
            if set_name in EXTENSION_SETS:
                sets_to_print[set_name] = EXTENSION_SETS[set_name]
            else:
                print(f"⚠️  Warning: Set '{set_name}' not found.")

    if not sets_to_print:
        print("No matching sets found.")
        return

    print("\nAvailable Extension Sets:\n" + "-" * 40)
    for set_name in sorted(sets_to_print.keys()):
        print(f"\n{set_name} extensions:")
        # Format the extensions to match the prompt's style
        extensions = sorted(list(sets_to_print[set_name]))
        lines = []
        current_line = []
        for ext in extensions:
            current_line.append(f'"{ext}"')
            if len(current_line) >= 4: # 4 per line
                lines.append("    " + ", ".join(current_line) + ",")
                current_line = []
        if current_line: # Add any remaining
            lines.append("    " + ", ".join(current_line))
        
        print("\n".join(lines))
        
    print("\n" + "-" * 40)