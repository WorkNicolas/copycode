"""_summary_
Union of all extension_sets from extension_sets.py
"""
from copycode.config.extension_sets import EXTENSION_SETS
DEFAULT_ALLOWED_EXTENSIONS = set().union(*EXTENSION_SETS.values())