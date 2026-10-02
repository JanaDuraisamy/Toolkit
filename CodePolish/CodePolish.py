from __future__ import annotations

import shutil
import subprocess
import sys
import os
import platform
import site
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from time import monotonic

APP_NAME = "CODEPOLISH"
APP_SUBTITLE = "Code Readability Tool"
CREATOR = "Created by Jana"
OUTPUT_SUFFIX = "_formatted"

SKIP_DIRECTORIES = {
    "node_modules", ".git", ".next", ".nuxt", ".svelte-kit",
    "dist", "build", "coverage", ".venv", "venv", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".idea", ".vscode", ".ruff_cache",
    ".gradle", ".dart_tool", "target", "vendor",
}

EXTENSIONS = {
    ".py": "Ruff",
    ".js": "Prettier", ".jsx": "Prettier", ".ts": "Prettier", ".tsx": "Prettier",
    ".mjs": "Prettier", ".cjs": "Prettier", ".css": "Prettier", ".scss": "Prettier",
    ".less": "Prettier", ".html": "Prettier", ".htm": "Prettier", ".vue": "Prettier",
    ".svelte": "Prettier", ".astro": "Prettier", ".json": "Prettier", ".jsonc": "Prettier",
    ".yaml": "Prettier", ".yml": "Prettier", ".md": "Prettier", ".mdx": "Prettier",
    ".graphql": "Prettier", ".gql": "Prettier", ".xml": "Prettier",
    ".go": "gofmt", ".rs": "rustfmt",
    ".c": "clang-format", ".h": "clang-format", ".cc": "clang-format", ".cpp": "clang-format",
    ".cxx": "clang-format", ".hh": "clang-format", ".hpp": "clang-format", ".hxx": "clang-format",
    ".java": "google-java-format", ".kt": "ktfmt", ".kts": "ktfmt", ".dart": "dart format",
    ".swift": "swift-format", ".php": "PHP-CS-Fixer", ".rb": "RuboCop", ".sql": "SQLFluff",
}


@dataclass(frozen=True)
class Formatter:
    name: str
    executables: tuple[str, ...]
    install_mode: str
    install_command: tuple[str, ...] | None
    manual_hint: str


FORMATTERS = {
    "Ruff": Formatter("Ruff", ("ruff",), "auto",
                      (sys.executable, "-m", "pip", "install", "ruff"), "pip install ruff"),
    "Prettier": Formatter("Prettier", ("prettier",), "auto",
                          ("npm", "install", "-g", "prettier"), "npm install -g prettier"),
    "SQLFluff": Formatter("SQLFluff", ("sqlfluff",), "auto",
                          (sys.executable, "-m", "pip", "install", "sqlfluff"), "pip install sqlfluff"),
    "RuboCop": Formatter("RuboCop", ("rubocop",), "auto",
                         ("gem", "install", "rubocop"), "gem install rubocop"),
    "PHP-CS-Fixer": Formatter(
        "PHP-CS-Fixer", ("php-cs-fixer", "php-cs-fixer.phar"), "auto",
        ("composer", "global", "require", "friendsofphp/php-cs-fixer"),
        "composer global require friendsofphp/php-cs-fixer",
    ),
    "gofmt": Formatter(
        "gofmt", ("gofmt",), "manual", None,
        "Go SDK install pannunga; gofmt adhoda kooda varum.",
    ),
    "rustfmt": Formatter(
        "rustfmt", ("rustfmt",), "manual", None,
        "Rust toolchain install pannunga; rustfmt rustup moolama kidaikkum.",
    ),
    "clang-format": Formatter(
        "clang-format", ("clang-format",), "auto", None,
        "LLVM/clang-format install pannunga; CodePolish package-manager moolama install panna try pannum.",
    ),
    "google-java-format": Formatter(
        "google-java-format", ("google-java-format",), "auto", None,
        "Java runtime thevai; CodePolish google-java-format setup panna try pannum.",
    ),
    "ktfmt": Formatter(
        "ktfmt", ("ktfmt",), "auto", None,
        "Java runtime thevai; CodePolish ktfmt setup panna try pannum.",
    ),
    "dart format": Formatter(
        "dart format", ("dart",), "manual", None,
        "Dart/Flutter SDK install pannunga; dart format adhoda kooda varum.",
    ),
    "swift-format": Formatter(
        "swift-format", ("swift-format",), "auto", None,
        "Swift toolchain/package manager support thevai; CodePolish platform-ku suitable setup try pannum.",
    ),
}


try:
    from rich.console import Console
    from rich.align import Align
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
    from rich.prompt import Prompt
    from rich.table import Table
    RICH = True
    console = Console()
except ImportError:
    RICH = False
    console = None


def out(message=""):
    if RICH:
        console.print(message)
    else:
        for tag in (
            "[bold cyan]", "[/bold cyan]", "[green]", "[/green]",
            "[yellow]", "[/yellow]", "[red]", "[/red]", "[cyan]", "[/cyan]",
            "[bright_cyan]", "[/bright_cyan]", "[bold green]", "[/bold green]",
            "[bold white]", "[/bold white]", "[dim]", "[/dim]",
        ):
            message = message.replace(tag, "")
        print(message)


def banner():
    if RICH:
        console.print(
            Panel.fit(
                f"[bold cyan]✦ {APP_NAME} ✦[/bold cyan]\n"
                f"[white]{APP_SUBTITLE}[/white]\n\n"
                f"[dim]{CREATOR}[/dim]",
                border_style="cyan",
                padding=(1, 5),
            )
        )
    else:
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                      ✦ CODEPOLISH ✦                         ║")
        print("║                    Code Readability Tool                     ║")
        print("║                       Created by Jana                        ║")
        print("╚══════════════════════════════════════════════════════════════╝")


def section(title):
    if RICH:
        console.print()
        console.print(f"[bold cyan]╭─ {title}[/bold cyan]")
        console.print()
    else:
        print()
        print(f"--- {title} ---")
        print()


def ok(message):
    out(f"[green]✓[/green] {message}" if RICH else f"✓ {message}")


def warn(message):
    out(f"[yellow]⚠[/yellow] {message}" if RICH else f"⚠ {message}")


def fail(message):
    out(f"[red]✗[/red] {message}" if RICH else f"✗ {message}")


def info(message):
    out(f"[cyan]ℹ[/cyan] {message}" if RICH else f"ℹ {message}")


def choose(question, choices, default="1"):
    if RICH:
        while True:
            console.print()
            table = Table.grid(padding=(0, 1))
            table.add_column(width=3, justify="right")
            table.add_column(width=24)
            table.add_column()

            styles = {
                "1": ("green", "Install & Continue"),
                "2": ("yellow", "Manual Setup"),
                "3": ("cyan", "Skip Missing"),
                "4": ("red", "Cancel"),
            }

            for key, description in choices.items():
                color, label = styles.get(key, ("white", description))
                display_label = label if key in styles else description
                table.add_row(
                    f"[bold {color}]{key}[/bold {color}]",
                    f"[bold {color}]{display_label}[/bold {color}]",
                    f"[white]{description}[/white]",
                )

            console.print(
                Panel(
                    table,
                    title=f"[bold cyan]{question}[/bold cyan]",
                    border_style="bright_black",
                    padding=(1, 2),
                )
            )
            console.print()
            value = Prompt.ask(
                "[bold white]› Select an option[/bold white]",
                default=default,
            ).strip()
            if value in choices:
                return value
            fail("Invalid choice. Oru valid option select pannunga.")

    while True:
        print()
        print(f"╭─ {question}")
        print()
        labels = {
            "1": "Install & Continue",
            "2": "Manual Setup",
            "3": "Skip Missing",
            "4": "Cancel",
        }
        for key, description in choices.items():
            label = labels.get(key, description)
            print(f"  {key}  {label}")
            if key in labels:
                print(f"      {description}")
            print()
        print("╰────────────────────────────────────────────────────────────")
        value = input(f"› Select an option [{default}]: ").strip() or default
        if value in choices:
            return value
        print("❌ Invalid choice. Oru valid option select pannunga.")


def formatter_cache_dir():
    path = Path.home() / ".codepolish" / "formatters"
    path.mkdir(parents=True, exist_ok=True)
    return path


def java_runtime():
    java = shutil.which("java")
    return [java] if java else None


def cached_jar(name):
    jar = formatter_cache_dir() / f"{name}.jar"
    return jar if jar.exists() else None


def download_jar(url, name):
    target = formatter_cache_dir() / f"{name}.jar"
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "CodePolish"})
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()
        target.write_bytes(data)
        return target
    except Exception:
        try:
            target.unlink(missing_ok=True)
        except OSError:
            pass
        return None


def stream_process(command, cwd=None, label=None):
    """Run an installer live so users can see real installer output."""
    started = monotonic()
    detail_lines = []

    try:
        process = subprocess.Popen(
            list(command),
            cwd=str(cwd.resolve()) if cwd else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=False,
            bufsize=1,
        )
    except FileNotFoundError:
        return False, f"{command[0]} kandupidikka mudiyala.", monotonic() - started
    except PermissionError:
        return False, f"{command[0]} run panna permission illa.", monotonic() - started
    except OSError as exc:
        return False, str(exc), monotonic() - started

    if RICH:
        with console.status(
            f"[cyan]⏳ {label or command[0]} install pannitu irukkom...[/cyan]",
            spinner="dots",
        ):
            assert process.stdout is not None
            for raw in process.stdout:
                line = raw.rstrip()
                if line:
                    detail_lines.append(line)
            returncode = process.wait()
    else:
        assert process.stdout is not None
        for raw in process.stdout:
            line = raw.rstrip()
            if line:
                print(f"   {line}")
                detail_lines.append(line)
        returncode = process.wait()

    elapsed = monotonic() - started
    detail = "\n".join(detail_lines[-40:])

    if returncode == 0:
        return True, detail, elapsed
    return False, detail or f"Installer exited with code {returncode}.", elapsed


def package_manager_install(commands, label):
    last_detail = None
    last_elapsed = 0.0

    for command in commands:
        launcher = command[0]
        if shutil.which(launcher) is None:
            continue

        success, detail, elapsed = stream_process(command, label=label)
        if success:
            return True, detail, elapsed

        last_detail = detail
        last_elapsed = elapsed

    return (
        False,
        last_detail or "Compatible package manager kandupidikka mudiyala.",
        last_elapsed,
    )


def special_install(spec: Formatter):
    system = platform.system()

    if spec.name == "clang-format":
        if system == "Windows":
            return package_manager_install(
                [
                    (
                        "winget", "install", "--id", "LLVM.LLVM", "-e",
                        "--accept-package-agreements", "--accept-source-agreements",
                    ),
                    ("choco", "install", "llvm", "-y"),
                ],
                "clang-format / LLVM",
            )
        if system == "Darwin":
            return package_manager_install(
                [("brew", "install", "llvm")],
                "clang-format / LLVM",
            )
        return package_manager_install(
            [
                ("apt-get", "install", "-y", "clang-format"),
                ("dnf", "install", "-y", "clang-tools-extra"),
                ("pacman", "-S", "--noconfirm", "clang"),
            ],
            "clang-format",
        )

    if spec.name in {"google-java-format", "ktfmt"}:
        if not java_runtime():
            return False, "Java runtime (java) PATH-la kidaikkala. Java install pannunga.", 0.0

        if spec.name == "google-java-format":
            jar = cached_jar("google-java-format")
            if jar:
                return True, str(jar), 0.0
            url = (
                "https://repo1.maven.org/maven2/com/google/googlejavaformat/"
                "google-java-format/1.28.0/"
                "google-java-format-1.28.0-all-deps.jar"
            )
            jar = download_jar(url, "google-java-format")
        else:
            jar = cached_jar("ktfmt")
            if jar:
                return True, str(jar), 0.0
            url = (
                "https://repo1.maven.org/maven2/com/facebook/ktfmt/0.54/"
                "ktfmt-0.54-jar-with-dependencies.jar"
            )
            jar = download_jar(url, "ktfmt")

        if jar:
            return True, str(jar), 0.0
        return False, "Formatter JAR download panna mudiyala. Network/Java setup check pannunga.", 0.0

    if spec.name == "swift-format":
        if system == "Darwin":
            return package_manager_install(
                [("brew", "install", "swift-format")],
                "swift-format",
            )
        return (
            False,
            f"{system}-la swift-format-ku compatible Swift toolchain/package setup automatic-ah reliable illa.",
            0.0,
        )

    return False, "Automatic installer available illa.", 0.0


def detect(spec: Formatter):
    if spec.name in {"google-java-format", "ktfmt"}:
        java = java_runtime()
        jar = cached_jar(spec.name)
        if java and jar:
            return [java[0], "-jar", str(jar)]

    if spec.name == "Ruff":
        try:
            result = subprocess.run(
                [sys.executable, "-m", "ruff", "--version"],
                cwd=str(Path.home()),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                shell=False,
            )
            if result.returncode == 0:
                return [sys.executable, "-m", "ruff"]
        except OSError:
            pass

    for executable in spec.executables:
        path = shutil.which(executable)
        if path:
            return [path]

    # Windows/package-manager installs can place executables outside the
    # current process PATH. Check common installation locations explicitly.
    if platform.system() == "Windows":
        if spec.name == "clang-format":
            llvm_candidates = [
                Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "LLVM" / "bin" / "clang-format.exe",
                Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")) / "LLVM" / "bin" / "clang-format.exe",
            ]
            for exe in llvm_candidates:
                if exe.is_file():
                    return [str(exe)]

        if spec.name == "SQLFluff":
            # pip --user installs put sqlfluff.exe in a Scripts directory
            # that may not be present in the current PATH.
            # Windows pip --user commonly installs the package under
            #   %APPDATA%\Python\PythonXY\site-packages
            # and the executable under the sibling Scripts directory.
            # site.getuserbase() alone points to %APPDATA%\Python, so
            # check the versioned user-site parent as well.
            script_candidates = [
                Path(sys.executable).resolve().parent / "Scripts" / "sqlfluff.exe",
                Path(site.getuserbase()) / "Scripts" / "sqlfluff.exe",
            ]

            try:
                user_site = Path(site.getusersitepackages())
                script_candidates.extend([
                    user_site.parent / "Scripts" / "sqlfluff.exe",
                    user_site.parent.parent / "Scripts" / "sqlfluff.exe",
                ])
            except Exception:
                pass

            try:
                import sysconfig
                script_candidates.append(Path(sysconfig.get_path("scripts")) / "sqlfluff.exe")
            except Exception:
                pass

            seen = set()
            for exe in script_candidates:
                try:
                    key = str(exe.resolve()).lower()
                except OSError:
                    key = str(exe).lower()
                if key in seen:
                    continue
                seen.add(key)
                if exe.is_file():
                    return [str(exe)]

            # Last-resort module check for environments where the console
            # script exists but is not exposed through PATH.
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "sqlfluff", "--version"],
                    cwd=str(Path.home()),
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    shell=False,
                )
                if result.returncode == 0:
                    return [sys.executable, "-m", "sqlfluff"]
            except OSError:
                pass

    return None


def refresh_process_path():
    if platform.system() != "Windows":
        return
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "$env:Path"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            os.environ["PATH"] = result.stdout.strip()
    except OSError:
        pass


def scan(root: Path):
    if root.is_file():
        return [root] if root.suffix.lower() in EXTENSIONS else []

    result = []
    script_path = Path(__file__).resolve()
    tools_folder = script_path.parent
    formatter_files = {
        script_path.name,
        "format_code.py",
        "code_formatter.py",
        "CodePolish.py",
        "CodePolish_Final.py",
        "CodePolish_Release.py",
        "CodePolish_UI_Final.py",
    }

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if any(part in SKIP_DIRECTORIES for part in path.parts):
            continue

        if any(
            part == OUTPUT_SUFFIX
            or part.startswith(OUTPUT_SUFFIX + "_")
            or part.endswith(OUTPUT_SUFFIX)
            for part in path.parts
        ):
            continue

        if root.resolve() == tools_folder and path.name in formatter_files:
            continue

        if path.suffix.lower() in EXTENSIONS:
            result.append(path)

    return sorted(result, key=lambda p: str(p).lower())


def command_for(name, detected, target):
    if name == "Ruff":
        return [sys.executable, "-m", "ruff", "format", str(target)]
    if name == "Prettier":
        return [*detected, "--write", str(target)]
    if name == "SQLFluff":
        return [*detected, "format", str(target)]
    if name == "RuboCop":
        return [*detected, "-A", str(target)]
    if name == "PHP-CS-Fixer":
        return [*detected, "fix", str(target), "--quiet"]
    if name == "gofmt":
        return [*detected, "-w", str(target)]
    if name == "rustfmt":
        return [*detected, str(target)]
    if name == "clang-format":
        return [*detected, "-i", str(target)]
    if name == "google-java-format":
        return [*detected, "--replace", str(target)]
    if name == "ktfmt":
        return [*detected, str(target)]
    if name == "dart format":
        return [*detected, "format", str(target)]
    if name == "swift-format":
        return [*detected, "format", "--in-place", str(target)]
    raise ValueError(f"Unknown formatter: {name}")


def install(spec: Formatter):
    if spec.install_mode != "auto":
        return False, "Automatic install available illa.", 0.0

    if spec.install_command is None:
        result = special_install(spec)
        refresh_process_path()
        return result

    launcher = spec.install_command[0]
    if launcher in {"npm", "gem", "composer"} and shutil.which(launcher) is None:
        return False, f"{launcher} PATH-la kidaikkala.", 0.0

    returncode_like = stream_process(
        spec.install_command,
        label=spec.name,
    )
    refresh_process_path()
    return returncode_like


def dependency_check(files):
    required = {}
    for file in files:
        required.setdefault(EXTENSIONS[file.suffix.lower()], []).append(file)

    section("Formatter Check")
    available = {}
    missing = []

    for name, group in required.items():
        found = detect(FORMATTERS[name])
        if found:
            available[name] = found
            ok(f"{name} ready → {len(group)} file(s)")
        else:
            missing.append(name)
            mode = "automatic install" if FORMATTERS[name].install_mode == "auto" else "manual setup"
            warn(f"{name} missing → {len(group)} file(s) ({mode})")

    return required, available, missing


def resolve_dependencies(required, available, missing):
    if not missing:
        return available

    section("Missing Formatter Decision")
    warn("Input full scan mudinjathukku apram required formatter list complete-ah check pannirukkom.")

    choice = choose("Enna panna?", {
        "1": "Ella missing formatters-um install panni continue",
        "2": "Naan manual-ah install panren",
        "3": "Missing formatter files-ai skip panni continue",
        "4": "Cancel & Exit",
    })

    if choice == "4":
        raise SystemExit(0)

    if choice == "2":
        for name in missing:
            spec = FORMATTERS[name]
            warn(f"{name}: {spec.manual_hint}")
            if spec.install_command:
                out(f"   Example: {' '.join(spec.install_command)}")
        out("\nInstall mudinjathukku apram CodePolish-ah thirumba run pannunga.")
        raise SystemExit(0)

    if choice == "3":
        for name in missing:
            warn(f"{name} available illa; indha formatter files skip aagum.")
        return available

    section("Installing Missing Formatters")
    still_missing = []

    total = len(missing)
    if RICH:
        overview = Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]Dependency setup[/bold cyan]"),
            BarColumn(bar_width=30),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console,
            transient=False,
        )
        overview.start()
        task_id = overview.add_task("Installing formatters", total=total)
    else:
        overview = None
        task_id = None

    try:
        for number, name in enumerate(missing, start=1):
            spec = FORMATTERS[name]

            if spec.install_mode != "auto":
                still_missing.append(name)
                warn(f"{name}: automatic install reliable illa. Manual setup thevai.")
                if overview:
                    overview.update(task_id, completed=number)
                continue

            started = monotonic()
            if RICH:
                console.print(f"[bold white]⟳ [{number}/{total}][/bold white] [cyan]{name}[/cyan] install pannitu irukkom...")
            else:
                print(f"⟳ [{number}/{total}] {name} install pannitu irukkom...")

            success, detail, elapsed = install(spec)
            # Installer exit status alone is not authoritative. Some package
            # managers can return a non-zero status even when the formatter
            # is already installed/usable. Always verify the formatter after
            # the install attempt.
            detected = detect(spec)

            if detected:
                available[name] = detected
                ok(f"{name} ready  [dim]({elapsed:.1f}s)[/dim]" if RICH else f"{name} ready ({elapsed:.1f}s)")
            else:
                still_missing.append(name)
                fail(f"{name} automatic install failed.  [dim]({elapsed:.1f}s)[/dim]" if RICH else f"{name} automatic install failed. ({elapsed:.1f}s)")
                if detail:
                    out(f"   ↳ {detail}")

            if overview:
                overview.update(task_id, completed=number)
    finally:
        if overview:
            overview.stop()

    if still_missing:
        section("Remaining Missing Formatters")
        for name in still_missing:
            warn(f"{name}: {FORMATTERS[name].manual_hint}")

        # Clearer ordering: manual fix, skip missing, cancel.
        choice = choose("Remaining formatter files-ku enna panna?", {
            "1": "Manual setup mudichitu rerun pannuren",
            "2": "Indha formatter files mattum skip panni continue",
            "3": "Cancel & Exit",
        })

        if choice == "1":
            out("Manual setup mudichitu CodePolish-ah thirumba run pannunga.")
            raise SystemExit(0)
        if choice == "3":
            raise SystemExit(0)

    return available


def output_folder(input_path: Path):
    tools = Path(__file__).resolve().parent
    base = input_path.stem if input_path.is_file() else input_path.name
    name = f"{base.strip()}{OUTPUT_SUFFIX}"
    candidate = tools / name
    counter = 2
    while candidate.exists():
        candidate = tools / f"{name}_{counter}"
        counter += 1
    return candidate.resolve()


def target_for(source: Path, root: Path, output: Path):
    if root.is_file():
        return output / source.name
    return output / source.relative_to(root)


def run_formatter(source_file, output_file, formatter_name, formatter_command):
    source_file = Path(source_file).resolve()
    output_file = Path(output_file).resolve()
    working_directory = output_file.parent.resolve()

    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, output_file)

        before_content = output_file.read_bytes()
        command = command_for(formatter_name, formatter_command, output_file)

        result = subprocess.run(
            command,
            cwd=str(working_directory),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=False,
        )

        if result.returncode != 0:
            error_output = result.stderr.strip() or result.stdout.strip() or "Formatter failed."

            # SQLFluff requires a dialect. If the project has no SQLFluff
            # config/dialect, retry safely with ANSI as the generic fallback.
            if (
                formatter_name == "SQLFluff"
                and "No dialect was specified" in error_output
            ):
                fallback_command = [*command, "--dialect", "ansi"]
                result = subprocess.run(
                    fallback_command,
                    cwd=str(working_directory),
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    shell=False,
                )
                if result.returncode == 0:
                    error_output = ""
                else:
                    error_output = (
                        result.stderr.strip()
                        or result.stdout.strip()
                        or "Formatter failed."
                    )

            if result.returncode != 0:
                output_file.unlink(missing_ok=True)
                return False, (
                    f"Formatter command failed.\n\n"
                    f"Formatter:\n    {formatter_name}\n\n"
                    f"Source:\n    {source_file}\n\n"
                    f"Output:\n    {output_file}\n\n"
                    f"Error:\n    {error_output}"
                )

        after_content = output_file.read_bytes()
        if before_content == after_content:
            return True, "already_neat"
        return True, "formatted"

    except FileNotFoundError as error:
        output_file.unlink(missing_ok=True)
        return False, f"Required command/file kandupidikka mudiyala.\n\nError:\n    {error}"
    except PermissionError as error:
        output_file.unlink(missing_ok=True)
        return False, f"Permission denied.\n\nFile:\n    {output_file}\n\nError:\n    {error}"
    except UnicodeError as error:
        output_file.unlink(missing_ok=True)
        return False, f"File encoding read panna mudiyala.\n\nFile:\n    {source_file}\n\nError:\n    {error}"
    except OSError as error:
        output_file.unlink(missing_ok=True)
        return False, f"OS-level error vandhirukku.\n\nFile:\n    {output_file}\n\nError:\n    {error}"
    except Exception as error:
        output_file.unlink(missing_ok=True)
        return False, f"Unexpected error vandhirukku.\n\nFile:\n    {output_file}\n\nError:\n    {error}"


def format_file(source, root, output, available, index=None, total=None):
    name = EXTENSIONS[source.suffix.lower()]
    detected = available.get(name)
    display = source.name if root.is_file() else str(source.relative_to(root))

    out("")
    progress_label = f" [{index}/{total}]" if index and total else ""
    if RICH:
        out(f"[bold white]⏳ Checking:[/bold white] [cyan]{display}[/cyan][dim]{progress_label}[/dim]")
    else:
        out(f"⏳ Checking: {display}{progress_label}")

    if not detected:
        warn(f"{display}: {name} available illa; skip pannrom.")
        out("")
        return "skipped"

    target = target_for(source, root, output)

    if RICH:
        with console.status(f"[cyan]⏳ Formatting {display}...[/cyan]", spinner="dots"):
            success, status = run_formatter(source, target, name, detected)
    else:
        print("   ⏳ Formatting...")
        success, status = run_formatter(source, target, name, detected)

    if success and status == "formatted":
        out("   [green]✓[/green] Formatted successfully." if RICH else "   ✓ Formatted successfully.")
        out(f"   [dim]↳ Saved:[/dim] {target}" if RICH else f"   ↳ Saved: {target}")
        out("")
        return "formatted"

    if success and status == "already_neat":
        out("   [bright_cyan]✨ Already properly formatted.[/bright_cyan]" if RICH else "   ✨ Already properly formatted.")
        out("   [dim]↳ Changes edhuvum thevai illa.[/dim]" if RICH else "   ↳ Changes edhuvum thevai illa.")
        out("")
        return "neat"

    out("   [red]✗ Formatting failed.[/red]" if RICH else "   ✗ Formatting failed.")
    out(f"   ↳ {status}")
    out("   ↳ Original file safe-aa irukku.")
    out("")
    return "failed"


def summary(results, root, output):
    formatted, neat, failed, skipped = results
    section("Format Summary")

    if RICH:
        table = Table(show_header=True, header_style="bold white", border_style="bright_black")
        table.add_column("Status")
        table.add_column("Count", justify="right")
        table.add_row("Formatted", str(len(formatted)), style="green")
        table.add_row("Already Neat", str(len(neat)), style="cyan")
        table.add_row("Failed", str(len(failed)), style="red")
        table.add_row("Skipped", str(len(skipped)), style="yellow")
        console.print(table)
    else:
        print(f"✅ Formatted     : {len(formatted)}")
        print(f"✨ Already Neat  : {len(neat)}")
        print(f"❌ Failed        : {len(failed)}")
        print(f"⏭️ Skipped       : {len(skipped)}")

    for title, items, icon in (
        ("Formatted files", formatted, "🛠️"),
        ("Already neat files", neat, "✨"),
        ("Failed files", failed, "❌"),
        ("Skipped files", skipped, "⏭️"),
    ):
        if items:
            out(f"\n{icon} {title}:")
            for item in items:
                display = item.name if root.is_file() else str(item.relative_to(root))
                out(f"   • {display}")

    out("")
    out(f"📂 Output: {output}")
    out("")
    info("Original file/project-ai modify pannala. Formatted copy mattum output folder-la save pannirukkom.")


def supported_types():
    grouped = {}
    for extension, name in EXTENSIONS.items():
        grouped.setdefault(name, []).append(extension)
    section("Supported File Types")
    for name, extensions in grouped.items():
        out(f"  {name:<20} {', '.join(sorted(extensions))}")


def main():
    banner()

    section("What CodePolish does")
    out("CodePolish unga source files-ai readable-ah arrange panna formatter engines-ai use pannum.")
    out("Spacing, indentation, line arrangement madhiri readability-related changes apply aagalam.")
    out("Code logic-ai maatha purpose illa; actual formatter behavior language/tool-ku depend aagum.")
    out("Original files direct-ah modify panna maatom; output separate folder-la save pannrom.")

    if len(sys.argv) > 2:
        fail("Oru time-la oru file/project path mattum kudunga.")
        out('Usage: python CodePolish.py "P:\\Projects\\MyApp"')
        sys.exit(2)

    raw = sys.argv[1] if len(sys.argv) == 2 else input("\n📥 File/project path › ").strip().strip('"')
    if not raw:
        fail("Input path empty-ah irukku.")
        sys.exit(1)

    input_path = Path(raw).expanduser()
    if not input_path.exists():
        fail(f"Input kandupidikka mudiyala:\n  {input_path}")
        sys.exit(1)
    if not input_path.is_file() and not input_path.is_dir():
        fail(f"Input valid file/folder illa:\n  {input_path}")
        sys.exit(1)

    input_path = input_path.resolve()

    output_name = input_path.name.lower()
    if input_path.is_dir() and (
        output_name.endswith(OUTPUT_SUFFIX)
        or f"{OUTPUT_SUFFIX}_" in output_name
    ):
        section("Already Processed")
        info(
            f"Indha folder CodePolish create panna formatted output madhiri theriyudhu:\n  {input_path}"
        )
        out("")
        out("✨ Idhula irukkura files-ai CodePolish already process pannirukkum.")
        out("↳ Re-check panna original source folder-ai input-aa kudunga.")
        out("↳ Existing formatted output-ai safety-kaga automatic-ah rescan panna maatom.")
        out("")
        raise SystemExit(0)

    section("Scanning Input")
    out(f"📥 Input: {input_path}")
    files = scan(input_path)

    if not files:
        fail("Supported source files edhuvum kandupidikka mudiyala.")
        supported_types()
        sys.exit(1)

    out(f"🔎 Supported files found: {len(files)}")

    required, available, missing = dependency_check(files)
    available = resolve_dependencies(required, available, missing)

    usable = [file for file in files if EXTENSIONS[file.suffix.lower()] in available]
    pre_skipped = [file for file in files if file not in usable]

    if not usable:
        fail("Available formatter use panna koodiya files edhuvum illa.")
        sys.exit(1)

    output = output_folder(input_path)
    try:
        output.mkdir(parents=True, exist_ok=False)
    except PermissionError as exc:
        fail(f"Output folder create panna permission illa: {exc}")
        sys.exit(1)
    except OSError as exc:
        fail(f"Output folder create panna mudiyala: {exc}")
        sys.exit(1)

    section("Formatting")
    out("⏳ Code readability improve panna formatting start pannrom...")
    out("[dim]Original input-ai direct-ah modify panna maatom.[/dim]" if RICH else "Original input-ai direct-ah modify panna maatom.")
    out("")

    formatted, neat, failed, skipped = [], [], [], []
    total_files = len(usable)

    if RICH:
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]{task.description}[/bold cyan]"),
            BarColumn(bar_width=32),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console,
            transient=False,
        )
        progress.start()
        task_id = progress.add_task("Overall progress", total=total_files)
    else:
        progress = None
        task_id = None

    try:
        for index, file in enumerate(usable, start=1):
            if progress:
                progress.stop()

            status = format_file(
                file,
                input_path,
                output,
                available,
                index=index,
                total=total_files,
            )

            if status == "formatted":
                formatted.append(file)
            elif status == "neat":
                neat.append(file)
            elif status == "failed":
                failed.append(file)
            else:
                skipped.append(file)

            if progress:
                progress.start()
                progress.update(task_id, completed=index)
    finally:
        if progress:
            progress.stop()

    skipped.extend(pre_skipped)
    summary((formatted, neat, failed, skipped), input_path, output)

    if failed:
        warn("Sila files format aagala. Mela irukkura error details-ai check pannunga.")
        sys.exit(1)

    out("")
    out("")
    out(
        "[bold green]✦ CodePolish completed successfully. ✦[/bold green]"
        if RICH
        else "✦ CodePolish completed successfully. ✦"
    )
    out("")


if __name__ == "__main__":
    main()
