"""
All arguments that will be used in the terminal.
Uses everything from /copycode/commands/arguments/
"""

import argparse
parser = argparse.ArgumentParser(
        description="Recursively lists files, copying their contents in Markdown to the clipboard.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  copycode                         # Copy all default file types.
  copycode -a                      # Copy absolutely ALL files.
  copycode -ae log txt             # Copy default files PLUS .log and .txt files.
  copycode -af .vscode             # Copy default files, but include the .vscode folder.
  copycode -ie .css js             # Copy default files, but IGNORE .css and .js files.
  copycode -if my_build_dir        # Copy default files, but IGNORE the 'my_build_dir' folder.
  
  --- Set Examples ---
  copycode -ae /py /web            # Copy defaults PLUS all Python and Web extensions.
  copycode -ie /jvm                # Copy defaults but IGNORE all JVM extensions.
  copycode -ls                     # List all available extension sets.
  copycode -ls /py /web            # List extensions for the /py and /web sets.
""")

parser.add_argument("-a", "--all", action="store_true", help="Include all files and folders.")
parser.add_argument("-ls", "--list-sets", nargs="*", metavar="SET",
                    help="List available extension sets (e.g., /py /web).")
parser.add_argument("-d", "--dir", nargs="*", metavar="MODE",
                    help="List files and folders.\n"
                            "Use '/less' for minimal output.\n"
                            "Add '/no_print' to suppress terminal output.")
parser.add_argument("-dfo", "--dir-folders-only", nargs="*", metavar="MODE",
                    help="List folders only.\n"
                            "Use '/less' to list only top-level folders.\n"
                            "Add '/no_print' to suppress terminal output.")
parser.add_argument("-ae", "--add-extension", nargs="*", default=[],
                    help="Add extensions or sets to include (e.g., '.txt', '/py').")
parser.add_argument("-af", "--add-folder", nargs="*", default=[],
                    help="Add folders to include (e.g., 'node_modules').")
parser.add_argument("-ie", "--ignore-extensions", nargs="*", default=[],
                    help="Ignore extensions or sets (e.g., '.log', '/web').")
parser.add_argument("-if", "--ignore-folders", nargs="*", default=[],
                    help="Ignore folders (e.g., 'dist').")