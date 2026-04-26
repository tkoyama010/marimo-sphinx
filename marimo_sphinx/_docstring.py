import base64
import re
import textwrap
from typing import List

_MARIMO_APP_BASE_URL = "https://marimo.app/"

# Pattern for Examples section header (NumPy / Google / reST style)
_EXAMPLES_PATTERN = re.compile(
    r"^\s*(?:\.\.\s+(?:rubric|admonition)::\s+Examples|Examples\s*\n\s*[-=]+)",
    re.IGNORECASE | re.MULTILINE,
)
_EXAMPLES_LINE_PATTERN = re.compile(
    r"^\s*\.\.\s+(?:rubric|admonition)::\s+Examples\s*$",
    re.IGNORECASE,
)
_DISABLE_PATTERN = re.compile(r"^\s*\.\.\s+disable_marimo_try_it\s*$")
# Only another rubric/admonition marks a new section boundary (not ">>> " content lines)
_NEXT_SECTION_PATTERN = re.compile(
    r"^\s*\.\.\s+(?:rubric|admonition)::",
    re.IGNORECASE,
)


def code_to_marimo_url(code: str) -> str:
    """Convert Python code string to a marimo.app playground URL.

    The encoding uses base64 of the full marimo app script.
    Verify against https://marimo.app sharing URL format when upgrading marimo.
    """
    marimo_script = _wrap_as_marimo_script(code)
    encoded = base64.b64encode(marimo_script.encode()).decode()
    return f"{_MARIMO_APP_BASE_URL}?code={encoded}&embed=true"


def _wrap_as_marimo_script(code: str) -> str:
    indented = textwrap.indent(code.strip(), "    ")
    return (
        "import marimo\n\n"
        '__generated_with = "0.1.0"\n'
        "app = marimo.App()\n\n\n"
        "@app.cell\n"
        "def _():\n"
        f"{indented}\n"
        "    return\n"
    )


def insert_marimo_directive(lines: List[str], **options) -> List[str]:
    """Insert a ``.. marimo::`` directive after the Examples section.

    Modelled after jupyterlite_sphinx._try_examples.insert_try_examples_directive.
    """
    examples_start = None
    for i, line in enumerate(lines):
        if _EXAMPLES_LINE_PATTERN.match(line):
            examples_start = i
            break

    if examples_start is None:
        return lines

    # Check for disable marker or existing directive
    for line in lines[examples_start:]:
        if _DISABLE_PATTERN.match(line):
            return lines
        if line.strip().startswith(".. marimo::"):
            return lines

    # Find end of Examples section: stop at the next section header directive
    right_index = len(lines)
    for i in range(examples_start + 1, len(lines)):
        if _NEXT_SECTION_PATTERN.match(lines[i]):
            right_index = i
            break

    # Extract code from doctest-style (>>>) lines
    code_lines = []
    for line in lines[examples_start + 1 : right_index]:
        stripped = line.strip()
        if stripped.startswith(">>> "):
            code_lines.append(stripped[4:])
        elif stripped.startswith("..."):
            code_lines.append(stripped[3:].lstrip())

    if not code_lines:
        return lines

    # Build directive
    directive = ["", ".. marimo::"]
    for key, value in options.items():
        directive.append(f"   :{key}: {value}")
    directive.append("")
    for code_line in code_lines:
        directive.append(f"   {code_line}")
    directive.append("")

    return lines[:right_index] + directive + lines[right_index:]
