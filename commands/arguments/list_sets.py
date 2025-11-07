# commands/list_sets.py
from copycode.utilities.print_sets import print_sets

def handle_list_sets(args):
    """Handle the -ls command to print extension sets."""
    print_sets(args.list_sets)