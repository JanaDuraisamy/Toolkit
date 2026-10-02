# 🛠️ CodePolish Setup Guide

### Installation, Requirements & Troubleshooting

This guide explains how to set up CodePolish, install the required formatter tools, and solve common problems.

If you are using CodePolish for the first time, start from the top and follow the steps in order.

---

# 📌 Before You Start

CodePolish is a Python-based terminal application.

You need:

- Python installed
- CodePolish downloaded
- Terminal access
- Required formatter tools for the languages you want to format

You do **not** need to install every formatter.

CodePolish checks the files in your project and only looks for the formatters actually required by those files.

---

# 🐍 1. Install Python

CodePolish requires Python.

Check whether Python is already installed:

```bash
python --version
```

You can also try:

```bash
python3 --version
```

If Python is installed, you should see something similar to:

```text
Python 3.x.x
```

If the command is not recognized, install Python first and make sure Python is available in your system PATH.

---

# 📥 2. Download CodePolish

Place `CodePolish.py` somewhere convenient.

Recommended structure:

```text
Tools/
└── CodePolish/
    └── CodePolish.py
```

You can also keep CodePolish directly inside your existing `Tools` folder.

---

# ▶️ 3. Run CodePolish

Open a terminal in the folder containing `CodePolish.py`.

Run:

```bash
python CodePolish.py
```

CodePolish will ask you for the file or project path.

You can also provide the path directly:

```bash
python CodePolish.py "path/to/project"
```

Example:

```bash
python CodePolish.py "P:\Jana\Training\college-project"
```

---

# 📦 4. Formatter Dependencies

CodePolish uses different formatters for different programming languages.

You only need the formatter required by the files you are processing.

| Formatter | Used For |
|---|---|
| Ruff | Python |
| Prettier | JavaScript, TypeScript, HTML, CSS, JSON, YAML, Markdown, etc. |
| gofmt | Go |
| rustfmt | Rust |
| clang-format | C / C++ |
| google-java-format | Java |
| ktfmt | Kotlin |
| dart format | Dart |
| swift-format | Swift |
| PHP-CS-Fixer | PHP |
| RuboCop | Ruby |
| SQLFluff | SQL |

---

# 🤖 5. Automatic Dependency Setup

CodePolish checks all required formatters before creating the output folder.

If one or more formatters are missing, you will see a menu similar to:

```text
[1] Install all missing formatters & continue
[2] Manual setup
[3] Skip files requiring missing formatters
[4] Cancel
```

## Option 1 — Install & Continue

Choose this when you want CodePolish to install the missing formatters automatically.

CodePolish attempts to install all missing formatters and then checks again to make sure they are actually available.

It does not silently install anything.

You must explicitly choose this option.

---

## Option 2 — Manual Setup

Choose this when you want to install the formatters yourself.

CodePolish shows the required formatter and an installation hint.

After installing the required tools, run CodePolish again.

---

## Option 3 — Skip Missing

Choose this when you want to continue without installing the missing formatter.

Only files requiring the unavailable formatter are skipped.

Other files can still be formatted.

For example:

```text
Python       → Ruff       → Ready
JavaScript   → Prettier   → Ready
SQL          → SQLFluff   → Missing
```

If you choose Skip:

```text
Python files       → Formatted
JavaScript files   → Formatted
SQL files          → Skipped
```

---

## Option 4 — Cancel

Stops the current CodePolish operation.

Your original project remains untouched.

---

# 🐍 6. Ruff — Python

Ruff is used for Python files.

Install manually with:

```bash
python -m pip install ruff
```

Or:

```bash
pip install ruff
```

Check the installation:

```bash
python -m ruff --version
```

You should see the installed Ruff version.

CodePolish uses Python's module invocation when running Ruff, so it can work even when the `ruff` command itself is not directly available in PATH.

---

# 🌐 7. Prettier — JavaScript & Web

Prettier is used for:

```text
JavaScript
JSX
TypeScript
TSX
MJS
CJS
CSS
SCSS
LESS
HTML
Vue
Svelte
Astro
JSON
JSONC
YAML
Markdown
MDX
GraphQL
XML
```

Install Node.js and npm first.

Then install Prettier:

```bash
npm install -g prettier
```

Check:

```bash
prettier --version
```

If a project contains `package.json`, `package-lock.json`, or other `.json` files, those files can also be formatted through Prettier.

---

# 🐹 8. gofmt — Go

Go files use `gofmt`.

CodePolish treats Go formatter setup as manual.

Install the Go SDK from the official Go distribution.

After installing Go, check:

```bash
go version
```

Then check:

```bash
gofmt -h
```

`gofmt` is included with the Go SDK.

If CodePolish reports:

```text
gofmt missing
```

make sure the Go installation directory is available through your system PATH.

Then restart your terminal and run CodePolish again.

---

# 🦀 9. rustfmt — Rust

Rust files use `rustfmt`.

Install Rust and the Rust toolchain.

The recommended Rust toolchain manager is `rustup`.

After installation, check:

```bash
rustc --version
```

Then:

```bash
rustfmt --version
```

If `rustfmt` is missing, make sure the Rust toolchain is installed correctly.

CodePolish treats `rustfmt` setup as manual.

---

# ⚙️ 10. clang-format — C / C++

`clang-format` is used for:

```text
C
C++
C headers
```

Examples:

```text
.c
.h
.cc
.cpp
.cxx
.hh
.hpp
.hxx
```

## Windows

CodePolish can try:

```text
winget
```

and then:

```text
choco
```

to install LLVM / clang-format.

If automatic installation does not work, install LLVM manually and make sure `clang-format` is available in PATH.

You can check:

```bash
clang-format --version
```

---

## macOS

CodePolish can use Homebrew:

```bash
brew install llvm
```

Then verify:

```bash
clang-format --version
```

---

## Linux

Depending on your Linux distribution, CodePolish can try package managers such as:

```bash
apt-get
dnf
pacman
```

You can also install `clang-format` manually using your distribution's package manager.

Then check:

```bash
clang-format --version
```

---

# ☕ 11. google-java-format — Java

Java files use `google-java-format`.

CodePolish requires a Java runtime for this formatter.

Check Java:

```bash
java --version
```

If Java is not installed, install a supported Java runtime/JDK first.

CodePolish can download and cache the formatter JAR automatically when Java is available.

The formatter is stored in CodePolish's cache directory:

```text
~/.codepolish/formatters/
```

Once downloaded, CodePolish can reuse the cached formatter instead of downloading it again.

If CodePolish reports:

```text
Java runtime (java) PATH-la kidaikkala.
```

make sure Java is installed and available in PATH.

Restart the terminal after changing PATH.

---

# 🟣 12. ktfmt — Kotlin

Kotlin files use `ktfmt`.

Java is required because CodePolish uses the ktfmt formatter JAR.

Check:

```bash
java --version
```

CodePolish can download and cache the ktfmt JAR automatically.

The cache is stored under:

```text
~/.codepolish/formatters/
```

If Java is missing, CodePolish cannot set up ktfmt automatically.

Install Java, make sure `java` is available in PATH, and run CodePolish again.

---

# 🎯 13. dart format — Dart

Dart files use:

```text
dart format
```

CodePolish treats Dart formatter setup as manual.

Install the Dart SDK or Flutter SDK.

Check:

```bash
dart --version
```

Then:

```bash
dart format --help
```

If you use Flutter, Dart is normally included with the Flutter SDK.

After installation, make sure the `dart` command is available in PATH.

---

# 🍎 14. swift-format — Swift

Swift files use:

```text
swift-format
```

Automatic installation is available through Homebrew on macOS.

You can install it with:

```bash
brew install swift-format
```

Then check:

```bash
swift-format --version
```

On platforms where CodePolish cannot reliably perform the automatic setup, manual Swift toolchain/package setup is required.

---

# 🐘 15. PHP-CS-Fixer — PHP

PHP files use:

```text
PHP-CS-Fixer
```

CodePolish can attempt to install it through Composer:

```bash
composer global require friendsofphp/php-cs-fixer
```

Check:

```bash
php-cs-fixer --version
```

If the command is not recognized after installation, check that Composer's global binary directory is available in PATH.

---

# 💎 16. RuboCop — Ruby

Ruby files use:

```text
RuboCop
```

Install manually:

```bash
gem install rubocop
```

Check:

```bash
rubocop --version
```

If `gem` or `rubocop` is not recognized, make sure Ruby is installed correctly and its executable directories are available in PATH.

---

# 🐍 17. SQLFluff — SQL

SQL files use:

```text
SQLFluff
```

Install with:

```bash
python -m pip install sqlfluff
```

Or:

```bash
pip install sqlfluff
```

Check:

```bash
sqlfluff --version
```

CodePolish also checks Python-based SQLFluff installation locations on Windows.

---

# 🧩 18. Rich Terminal Interface

CodePolish uses the Rich Python library for its enhanced terminal interface when Rich is available.

The interface provides:

- Panels
- Colored messages
- Progress indicators
- Spinners
- Status information
- Formatting summaries

If Rich is not available, CodePolish can fall back to a simpler terminal interface.

If you want the full terminal UI, install Rich:

```bash
python -m pip install rich
```

Then run CodePolish again.

---

# 🪟 19. Windows PATH Problems

Sometimes a formatter is installed correctly but the terminal cannot find it.

For example:

```text
'ruff' is not recognized
```

or:

```text
'prettier' is not recognized
```

First check whether the command exists:

```bash
where ruff
```

or:

```bash
where prettier
```

You can also check the formatter version directly.

For Python formatters, CodePolish may be able to detect them through Python even when the command is not directly available.

For example:

```bash
python -m ruff --version
```

If you recently installed a formatter, close and reopen the terminal before trying again.

---

# 🔄 20. After Installing a Formatter

After manually installing a missing formatter:

1. Close the current CodePolish run.
2. Make sure the formatter works from the terminal.
3. Restart the terminal if PATH was changed.
4. Run CodePolish again.

Example:

```bash
python CodePolish.py "my-project"
```

CodePolish will check the formatter again.

---

# ❌ 21. "Formatter Missing" Error

If CodePolish says:

```text
Prettier missing
```

it means CodePolish could not detect the `prettier` executable.

Try:

```bash
prettier --version
```

If that fails, install:

```bash
npm install -g prettier
```

Then reopen the terminal and try again.

---

# ❌ 22. "Java Runtime Missing"

If CodePolish reports that Java is unavailable:

```text
Java runtime (java) PATH-la kidaikkala.
```

Check:

```bash
java --version
```

If the command fails:

1. Install Java.
2. Make sure Java is added to PATH.
3. Restart the terminal.
4. Run CodePolish again.

This is required for:

```text
google-java-format
ktfmt
```

---

# ❌ 23. Automatic Installation Failed

Sometimes a package manager may fail even though the formatter is already installed or can be installed manually.

CodePolish verifies the formatter after attempting installation.

If it is still missing, CodePolish shows the remaining missing formatter and gives you the option to:

```text
[1] Manual setup and rerun
[2] Skip those formatter files
[3] Cancel
```

If automatic installation fails, manually install the formatter and run CodePolish again.

---

# 🌐 24. Internet / Download Problems

Some automatic setup operations require internet access.

This includes:

- Installing packages
- Downloading Java formatter JARs
- Accessing package repositories

For Java and Kotlin formatters, CodePolish downloads the required JAR when it is not already cached.

If the download fails, check:

- Internet connection
- Firewall
- Proxy configuration
- Package repository access

Then run CodePolish again.

---

# 🔐 25. Permission Problems

If you see a permission-related error:

```text
Permission denied
```

try:

- Closing applications that are using the file
- Checking whether the file is read-only
- Running the terminal with appropriate permissions
- Checking folder permissions

Avoid running CodePolish with elevated privileges unless necessary.

---

# 📝 26. Encoding Problems

CodePolish handles common Unicode and encoding-related errors.

If a file cannot be processed because of its encoding, CodePolish reports the problem instead of silently changing the original file.

If this happens:

1. Check the file encoding.
2. Open the file in your editor.
3. Convert it to a standard encoding such as UTF-8 if appropriate.
4. Run CodePolish again.

---

# 📁 27. Why Is My File Not Being Formatted?

If CodePolish does not process a file, check its extension.

CodePolish only processes registered file extensions.

For example:

```text
app.py       → Supported
main.ts      → Supported
data.json    → Supported
query.sql    → Supported
.env         → Not supported
.gitignore   → Not supported
```

Also check whether the file is inside a skipped directory such as:

```text
node_modules
.git
dist
build
target
vendor
```

---

# 🔁 28. Why Is My Project Folder Not Being Processed Again?

If you try to give CodePolish one of its previously generated output folders, CodePolish detects that it is already a formatted output.

Examples:

```text
project_formatted
project_formatted_2
project_formatted_3
```

Use the original project instead.

This prevents accidentally formatting an already generated result again.

---

# 📂 29. Where Is My Formatted Project?

CodePolish creates the output folder inside the same directory where `CodePolish.py` is located.

For example:

```text
Tools/
├── CodePolish.py
└── college-project_formatted/
```

If the folder already exists, CodePolish creates:

```text
college-project_formatted_2/
```

Then:

```text
college-project_formatted_3/
```

and so on.

---

# 🛡️ 30. Is My Original Project Safe?

Yes.

CodePolish copies the source file into the output location before running the formatter.

The formatter works on the copied file.

The original file is not used as the formatter's output target.

If formatting fails, CodePolish removes the failed output copy.

The original remains untouched.

---

# 📊 31. Understanding the Final Summary

At the end of the process, CodePolish shows a summary.

Example:

```text
Formatted       : 8
Already Neat    : 3
Skipped         : 1
Failed          : 0
```

### Formatted

The formatter changed the copied file.

### Already Neat

The formatter ran successfully, but the file was already formatted.

### Skipped

The required formatter was unavailable and the file was intentionally skipped.

### Failed

The formatter could not successfully process the file.

---

# 🧪 32. Recommended First Test

If you are setting up CodePolish for the first time, test it with a small project.

Example:

```text
test-project/
├── app.py
├── main.js
├── styles.css
└── data.json
```

Run:

```bash
python CodePolish.py "test-project"
```

CodePolish should:

```text
1. Scan the project
2. Detect Python
3. Detect JavaScript
4. Detect CSS
5. Detect JSON
6. Check Ruff
7. Check Prettier
8. Create the output folder
9. Format copies
10. Show the final summary
```

Your original `test-project` remains unchanged.

---

# 🧭 33. Quick Setup Checklist

Before using CodePolish, check:

```text
[ ] Python installed
[ ] CodePolish.py available
[ ] Terminal opened in the correct location
[ ] Required formatter installed
[ ] Formatter command works
[ ] PATH updated if necessary
[ ] Project path is correct
```

You do not need to install every formatter.

Only install the formatters required by your project.

---

# 🆘 34. If Something Still Doesn't Work

If CodePolish still reports a missing formatter:

### Step 1

Check the formatter directly.

For example:

```bash
ruff --version
```

```bash
prettier --version
```

```bash
sqlfluff --version
```

```bash
clang-format --version
```

```bash
java --version
```

### Step 2

If the command fails, install or repair that formatter.

### Step 3

Restart the terminal if you changed PATH.

### Step 4

Run CodePolish again.

---

# 📌 Important Notes

- CodePolish does not silently install missing formatters.
- Automatic installation requires your explicit choice.
- Only required formatters are checked.
- Unsupported files are ignored.
- Common dependency and generated directories are skipped.
- Previously generated `_formatted` folders are skipped.
- The original project is not modified.
- Failed output copies are removed.
- Some formatters require additional runtimes or SDKs.
- Automatic installation availability depends on the operating system.
- Manual setup is available when automatic installation is not reliable.

---

# 📚 Related Documentation

- **[README.md](./README.md)** — What CodePolish is and how it works
- **[CodePolish.py](./CodePolish.py)** — Main application source

---

# 👨‍💻 Created By

**Jana**

Full-Stack Developer • Product Creator

Building practical developer tools and digital experiences.

---

# 📄 License

CodePolish is released under the **MIT License**.

See the repository's `LICENSE` file for the complete license text.
