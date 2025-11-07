# __main__.py
from copycode.commands.parser import parser
from copycode.commands.arguments.list_sets import handle_list_sets
from copycode.commands.arguments.dir import handle_dir_command
from copycode.commands.arguments.dir_folders_only import handle_dir_folders_only
from copycode.commands.copy_files import handle_copy_files

def main():
    args = parser.parse_args()

    if args.list_sets is not None:
        handle_list_sets(args)
        return
    if args.dir is not None:
        handle_dir_command(args)
        return
    if args.dir_folders_only is not None:
        handle_dir_folders_only(args)
        return
    handle_copy_files(args)

if __name__ == "__main__":
    main()