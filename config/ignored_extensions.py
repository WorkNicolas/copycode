"""_summary_
Extensions that are ignored by default. Things that are not needed to be copied into an LLM.
"""
DEFAULT_IGNORED_FILES = {
    # Common Project Files
    ".gitignore", ".gitattributes", ".gitmodules",
    "README.md", "README", "readme.md", "readme",
    "LICENSE", "LICENSE.txt", "license", "COPYING",
    "CHANGELOG.md", "CHANGELOG", "changelog.md", "HISTORY.md",
    "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md",
    # Environment & Secrets
    ".env", ".env.local", ".env.development", ".env.production", ".env.test",
    ".env.*.local",
    ".secrets", ".secret", "secrets.json", "config.local",
    # OS & Editor Junk
    "Thumbs.db", ".DS_Store", "desktop.ini", ".Spotlight-V100", ".Trashes",
    # IDE & Tooling
    ".vscodeignore", ".editorconfig", ".prettierrc", ".eslintrc*",
    "tsconfig.json", "jsconfig.json",
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "Gemfile.lock", "Pipfile.lock",
    "Cargo.lock", "poetry.lock", "composer.lock",
    # Build & Config
    "Dockerfile", ".dockerignore",
    "Makefile", "makefile", "CMakeLists.txt",
    "webpack.config.js", "vite.config.js", "rollup.config.js", "babel.config.js",
    "gradlew", "gradlew.bat", "mvnw", "mvnw.cmd",
    # Logs & Databases
    "*.log", "debug.log", "error.log", "app.log", "development.log",
    "*.sqlite3", "*.db",
}