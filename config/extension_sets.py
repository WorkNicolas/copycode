"""_summary_
List of extensions with categories of what programming language they use.
Default things that will be copied.
"""
EXTENSION_SETS = {
    "/py": {
        ".py", ".pyw", ".pyd", ".pyx", ".pxd", ".pxi"
    },
    "/jvm": {
        ".java", ".class", ".jar", ".kt", ".kts", ".scala", ".clj", ".cljs", ".edn"
    },
    "/c": {
        ".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx", ".hh", ".ino", ".cu", ".cuh"
    },
    "/dotnet": {
        ".cs", ".csx", ".fs", ".fsx", ".vb"
    },
    "/web": {
        ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".mts", ".cts",
        ".html", ".htm", ".xhtml", ".css", ".scss", ".sass", ".less", ".styl",
        ".json", ".json5", ".jsonc", ".xml", ".svg", ".webmanifest"
    },
    "/frontend": {
        ".vue", ".svelte", ".astro", ".elm", ".pug", ".jade", ".handlebars", ".hbs"
    },
    "/script": {
        ".sh", ".bash", ".zsh", ".fish", ".ps1", ".psm1", ".psd1",
        ".pl", ".pm", ".lua", ".rb", ".erb", ".rake", ".swift", ".go", ".rs"
    },
    "/config": {
        ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
        ".env", ".env.local", ".env.development", ".env.production",
        ".properties", ".gradle", ".gradle.kts", ".dockerfile", ".dockerignore"
    },
    "/sql": {
        ".sql", ".sqlite", ".db", ".db3", ".mdb", ".accdb"
    },
    "/docs": { # From commented-out section
        ".md", ".markdown", ".mkd", ".mdown", ".rst", ".adoc"
    },
    "/idl": {
        ".proto", ".thrift", ".avdl"
    },
    "/gql": {
        ".gql", ".graphql", ".graphqls"
    },
    "/mobile": { # .xml, .kt, .yaml are in other sets
        ".dart"
    },
    "/build": {
        ".mk", ".makefile", "makefile"
    },
}