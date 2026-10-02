# 🧹 CodePolish

### Code Readability Tool

**Created by Jana**

CodePolish is a lightweight terminal-based code readability and formatting tool that scans files or complete projects, detects supported programming languages, checks the required formatters, and creates a clean formatted copy without modifying the original source.

---

## ✨ What is CodePolish?

CodePolish helps make source code easier to read by automatically applying the appropriate formatter for each supported file type.

It can work with:

- A single source file
- An entire project folder
- Projects containing multiple programming languages

CodePolish automatically detects supported file types and selects the corresponding formatter.

> **Important:** CodePolish focuses on readability formatting such as indentation, spacing, and line arrangement. It is not intended to change your program's logic.

---

## 🖥️ Platform Support

CodePolish is designed to work across major desktop operating systems:

| Platform | Support |
|---|---|
| 🪟 Windows | ✅ Supported |
| 🍎 macOS | ✅ Supported |
| 🐧 Linux | ✅ Supported |

Formatter availability and automatic installation methods can vary depending on the operating system.

CodePolish can work with tools installed through:

- `pip`
- `npm`
- `gem`
- `composer`
- `winget`
- `choco`
- `brew`
- Linux package managers
- Java-based formatter JAR files

When automatic installation is not available or reliable for a formatter on a platform, CodePolish provides manual setup guidance.

---

# 🚀 Features

## 🔍 Automatic Language Detection

CodePolish identifies supported files based on their file extensions and automatically selects the appropriate formatter.

| File Type | Formatter |
|---|---|
| `.py` | Ruff |
| `.js`, `.jsx` | Prettier |
| `.ts`, `.tsx` | Prettier |
| `.mjs`, `.cjs` | Prettier |
| `.css`, `.scss`, `.less` | Prettier |
| `.html`, `.htm` | Prettier |
| `.vue` | Prettier |
| `.svelte` | Prettier |
| `.astro` | Prettier |
| `.json`, `.jsonc` | Prettier |
| `.yaml`, `.yml` | Prettier |
| `.md`, `.mdx` | Prettier |
| `.graphql`, `.gql` | Prettier |
| `.xml` | Prettier |
| `.go` | gofmt |
| `.rs` | rustfmt |
| `.c`, `.h` | clang-format |
| `.cc`, `.cpp`, `.cxx` | clang-format |
| `.hh`, `.hpp`, `.hxx` | clang-format |
| `.java` | google-java-format |
| `.kt`, `.kts` | ktfmt |
| `.dart` | dart format |
| `.swift` | swift-format |
| `.php` | PHP-CS-Fixer |
| `.rb` | RuboCop |
| `.sql` | SQLFluff |

---

## 📁 Project-Wide Formatting

CodePolish can scan an entire project recursively.

For example:

```text
my-project/
├── src/
│   ├── app.py
│   ├── main.ts
│   └── styles.css
├── config/
│   └── settings.json
├── database/
│   └── query.sql
└── package.json
```

CodePolish detects the supported files and uses the correct formatter for each one.

A project can contain multiple programming languages and formatters at the same time.

---

## 📄 Single File Formatting

CodePolish can also process a single supported file.

Example:

```bash
python CodePolish.py "app.py"
```

The formatted copy is created separately inside the `Tools` directory.

---

# 🔄 How CodePolish Works

```text
┌────────────────────────┐
│   Select File/Folder   │
└────────────┬───────────┘
             │
             ▼
┌────────────────────────┐
│      Scan Input        │
│  Find Supported Files  │
└────────────┬───────────┘
             │
             ▼
┌────────────────────────┐
│ Detect Required        │
│ Formatters             │
└────────────┬───────────┘
             │
             ▼
┌────────────────────────┐
│  Check Dependencies    │
└────────────┬───────────┘
             │
        ┌────┴────┐
        │ Missing?│
        └────┬────┘
             │
      ┌──────┼──────────┐
      ▼      ▼          ▼
   Install Manual      Skip
      │      │          │
      └──────┴──────────┘
             │
             ▼
┌────────────────────────┐
│  Create Output Folder  │
└────────────┬───────────┘
             │
             ▼
┌────────────────────────┐
│   Format File Copies   │
└────────────┬───────────┘
             │
             ▼
┌────────────────────────┐
│    Show Summary        │
└────────────────────────┘
```

---

# 🛡️ Original Files Stay Safe

CodePolish never formats the original file directly.

Instead, it:

1. Scans the original project.
2. Detects supported files.
3. Checks the required formatters.
4. Creates a new output folder.
5. Copies the source files.
6. Runs the formatter on the copied files.
7. Compares the result.
8. Reports the final status.

```text
Original Project
       │
       │ ❌ Never modified
       ▼
   Copy Files
       │
       ▼
 Run Formatter
       │
       ▼
 Compare Result
       │
       ├── Changed → Formatted
       │
       └── Same    → Already Neat
```

---

# 📦 Dependency Management

Before formatting begins, CodePolish scans the complete input and determines all required formatters.

For example:

```text
Python       → Ruff
JavaScript   → Prettier
SQL          → SQLFluff
Java         → google-java-format
```

CodePolish checks all required formatters before creating the output folder.

If formatters are missing, it shows one consolidated dependency menu:

```text
[1] Install all missing formatters & continue
[2] Manual setup
[3] Skip files requiring missing formatters
[4] Cancel
```

This avoids repeatedly asking for each missing formatter.

---

# ⚙️ Automatic Formatter Installation

Depending on the formatter and operating system, CodePolish can automatically install some dependencies.

### Python

```text
Ruff
SQLFluff
```

Installed using Python's package manager.

### JavaScript / Web

```text
Prettier
```

Installed using npm.

### Ruby

```text
RuboCop
```

Installed using RubyGems.

### PHP

```text
PHP-CS-Fixer
```

Installed using Composer.

### C / C++

`clang-format` can use the appropriate package manager depending on the operating system.

### Java

`google-java-format` can use a cached formatter JAR and requires Java.

### Kotlin

`ktfmt` can use a cached formatter JAR and requires Java.

### Swift

Automatic installation is supported on macOS through Homebrew.

---

# 🔧 Manual Formatters

Some formatters are handled through manual setup because reliable automatic installation is not provided for every platform.

These include:

```text
gofmt
rustfmt
dart format
```

Swift formatting may also require manual setup on platforms where automatic installation is not available.

Detailed setup instructions are available in:

**[SETUP.md](./SETUP.md)**

---

# 🚫 Skipped Directories

CodePolish intentionally skips common dependency, build, cache, IDE, and generated directories during recursive scanning.

```text
node_modules
.git
.next
.nuxt
.svelte-kit
dist
build
coverage
.venv
venv
__pycache__
.pytest_cache
.mypy_cache
.idea
.vscode
.ruff_cache
.gradle
.dart_tool
target
vendor
```

This prevents CodePolish from unnecessarily processing dependency and generated files.

---

# 🔁 Previously Formatted Output

CodePolish also skips its own generated output directories.

For example:

```text
project_formatted/
project_formatted_2/
project_formatted_3/
```

This prevents recursive scans from processing previously generated results again.

---

# 📄 Supported File Types

CodePolish formats only extensions registered in its formatter registry.

```text
.py

.js
.jsx
.ts
.tsx
.mjs
.cjs

.css
.scss
.less

.html
.htm
.vue
.svelte
.astro

.json
.jsonc
.yaml
.yml

.md
.mdx
.graphql
.gql
.xml

.go
.rs

.c
.h
.cc
.cpp
.cxx
.hh
.hpp
.hxx

.java
.kt
.kts
.dart
.swift
.php
.rb
.sql
```

---

# ❌ Unsupported Files

Files that are not registered in CodePolish's supported extension list are ignored.

Examples:

```text
.env
.env.local
.env.production
.gitignore
```

These files are not passed to any formatter.

> `package.json` and `package-lock.json` are supported because they use the `.json` extension.

---

# 📂 Output Structure

CodePolish creates the formatted result as a new folder inside the `Tools` directory.

For example:

```text
Tools/
├── CodePolish.py
└── my-project_formatted/
    ├── src/
    │   ├── app.py
    │   ├── main.ts
    │   └── styles.css
    ├── config/
    │   └── settings.json
    └── database/
        └── query.sql
```

The original project remains untouched.

---

# 🔢 Output Folder Collision Handling

If an output folder already exists:

```text
my-project_formatted/
```

CodePolish automatically creates:

```text
my-project_formatted_2/
```

If that also exists:

```text
my-project_formatted_3/
```

And so on.

Existing formatted results are not overwritten.

---

# 🧩 Project Structure Preservation

When formatting a project, CodePolish preserves the relative folder structure.

For example:

```text
Original:

project/
├── src/
│   └── app.py
├── config/
│   └── settings.json
└── database/
    └── query.sql
```

Becomes:

```text
project_formatted/
├── src/
│   └── app.py
├── config/
│   └── settings.json
└── database/
    └── query.sql
```

Only the formatted copies are changed.

---

# 📊 Formatting Results

After processing, CodePolish displays a final summary.

Example:

```text
Formatting Complete

Formatted       : 8
Already Neat    : 3
Skipped         : 1
Failed          : 0
```

### ✅ Formatted

The formatter successfully changed the copied file.

### ✓ Already Neat

The formatter completed successfully, but the file content remained unchanged.

### ⏭️ Skipped

The required formatter was unavailable and the file was selected to be skipped.

### ❌ Failed

The formatter could not successfully process the copied file.

The original source remains untouched.

---

# 🛠️ Error Handling

CodePolish handles common problems during scanning, dependency checking, and formatting.

It provides clear error handling for:

- Missing formatter commands
- Missing input files
- Invalid input paths
- Unsupported files
- Permission errors
- Encoding / Unicode errors
- Formatter execution failures
- Operating system errors
- Unexpected formatting errors

If a formatter fails, CodePolish removes the failed output copy instead of leaving an incomplete formatted file.

The original file remains safe.

---

# 🔍 Formatting Verification

CodePolish compares the file content before and after formatting.

This allows it to distinguish between:

```text
Formatted
```

and:

```text
Already Neat
```

If the formatter runs successfully but produces exactly the same file content, CodePolish reports the file as **Already Neat**.

---

# 🖥️ Terminal Interface

CodePolish uses a Rich-powered terminal interface designed to make the workflow easy to follow.

The interface includes:

- Branded startup screen
- Colored status messages
- Formatter detection status
- Dependency status
- Installation progress
- Formatting progress
- Final summary
- Clear error messages

The goal is to provide a proper terminal application experience instead of a basic formatter script.

---

# 💻 Usage

## Run CodePolish

From the `CodePolish` directory:

```bash
python CodePolish.py
```

CodePolish will ask for the file or folder you want to process.

---

## Pass a File or Folder Directly

You can also provide the path as an argument:

```bash
python CodePolish.py "path/to/project"
```

Example:

```bash
python CodePolish.py "P:\Jana\Training Tasks\college eligiblity check"
```

---

# 🧪 Example Workflow

Suppose a project contains:

```text
college-project/
├── src/
│   ├── app.py
│   ├── main.jsx
│   └── styles.css
├── config/
│   └── settings.json
├── database/
│   └── query.sql
├── node_modules/
└── .git/
```

CodePolish detects:

```text
app.py        → Ruff
main.jsx      → Prettier
styles.css    → Prettier
settings.json → Prettier
query.sql     → SQLFluff
```

And skips:

```text
node_modules/
.git/
```

After formatting:

```text
Tools/
└── college-project_formatted/
    ├── src/
    │   ├── app.py
    │   ├── main.jsx
    │   └── styles.css
    ├── config/
    │   └── settings.json
    └── database/
        └── query.sql
```

The original project is not modified.

---

# 📋 Requirements

CodePolish requires:

- Python
- Required formatter dependencies for the languages being processed

Depending on the project, additional tools may be required:

```text
Node.js / npm
Java
Ruby / gem
Composer
Go
Rust
Dart
Swift
C/C++ toolchain
```

Not every formatter is required.

Only the formatters needed by the detected files are checked.

---

# 📖 Setup & Troubleshooting

For detailed installation instructions, formatter requirements, platform-specific setup, and troubleshooting:

**[Open SETUP.md](./SETUP.md)**

---

# 🎬 Demo

> 🚧 **Demo GIF coming soon**

The demo will show a real CodePolish run including:

```text
Project Scan
     ↓
Language Detection
     ↓
Dependency Check
     ↓
Formatter Setup
     ↓
File Formatting
     ↓
Final Summary
```

The repository will include an actual terminal recording rather than a simulated demo.

---

# 🗺️ Roadmap

## V1

- [x] Multi-language formatter registry
- [x] Automatic language detection
- [x] Recursive project scanning
- [x] Single-file formatting
- [x] Dependency detection
- [x] Consolidated dependency workflow
- [x] Automatic formatter installation
- [x] Manual formatter setup
- [x] Missing formatter skip option
- [x] Safe output generation
- [x] Original source protection
- [x] Output collision handling
- [x] Project structure preservation
- [x] Formatting verification
- [x] Formatting summary
- [x] Error handling
- [x] Cross-platform support
- [x] Rich terminal interface

## Future

Potential future improvements include:

- More language formatters
- Additional CLI options
- Configuration support
- Custom formatting profiles
- More advanced project controls

---

# 📁 Project Structure

```text
CodePolish/
├── CodePolish.py
├── README.md
└── SETUP.md
```

---

# 👨‍💻 Created By

**Jana**

Full-Stack Developer • Product Creator

Building practical developer tools and digital experiences.

---

# 📄 License

CodePolish is released under the **MIT License**.

See the repository's `LICENSE` file for the complete license text.
