"""_summary_
Folders that are ignored by default. Things that are not needed to be copied into an LLM.
"""
DEFAULT_IGNORED_FOLDERS = {
    # IDEs & Editors
    ".vscode", ".idea", ".vs", "nbproject", ".eclipse", ".sublime-project", ".sublime-workspace",
    # Version Control
    ".git", ".svn", ".hg", ".bzr",
    # Build & Output Directories
    "build", "dist", "out", "target", "bin", "obj", "lib", "libs", "node_modules", "vendor",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".gradle", ".mvn",
    "coverage", "reports", "test-results",
    # Package Managers
    "node_modules", "bower_components", "jspm_packages",
    ".npm", ".yarn", ".pnpm",
    "Pods",
    # OS & Hidden
    ".DS_Store", "Thumbs.db", ".Trashes", ".Spotlight-V100",
    ".AppleDouble", ".LSOverride",
    # Docker & Containers
    ".docker",
    # CI/CD
    ".github", ".gitlab", ".circleci", ".travis", ".azure-pipelines",
    # Logs & Temp
    "logs", "log", "tmp", "temp", ".tmp", ".temp",
    # Android
    ".android", "android", "build", "gradle",
    # Flutter
    ".flutter-plugins", ".flutter-plugins-dependencies", ".dart_tool", "windows", "linux", "macos", "ios",
    # React / Web
    "public", "assets",
}