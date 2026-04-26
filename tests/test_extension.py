"""Basic tests for marimo-sphinx."""

import base64

import pytest

from marimo_sphinx._docstring import (
    _wrap_as_marimo_script,
    code_to_marimo_url,
    insert_marimo_directive,
)
from marimo_sphinx.nodes import MarimoIframe


class TestCodeToMarimoUrl:
    def test_returns_marimo_app_url(self):
        url = code_to_marimo_url("x = 1")
        assert url.startswith("https://marimo.app/?code=")

    def test_embed_param_present(self):
        url = code_to_marimo_url("x = 1")
        assert "embed=true" in url

    def test_code_is_base64_encoded(self):
        code = "x = 42"
        url = code_to_marimo_url(code)
        encoded = url.split("?code=")[1].split("&")[0]
        decoded = base64.b64decode(encoded).decode()
        assert "x = 42" in decoded

    def test_wraps_as_marimo_script(self):
        script = _wrap_as_marimo_script("x = 1")
        assert "import marimo" in script
        assert "app = marimo.App()" in script
        assert "@app.cell" in script
        assert "x = 1" in script


class TestInsertMarimoDirective:
    def test_no_examples_section_unchanged(self):
        lines = ["Some text.", "No examples here."]
        assert insert_marimo_directive(lines) == lines

    def test_inserts_directive_after_examples(self):
        lines = [
            ".. rubric:: Examples",
            "",
            ">>> x = 1",
            ">>> print(x)",
        ]
        result = insert_marimo_directive(lines)
        joined = "\n".join(result)
        assert ".. marimo::" in joined
        assert "x = 1" in joined
        assert "print(x)" in joined

    def test_skips_if_already_has_marimo(self):
        lines = [
            ".. rubric:: Examples",
            "",
            ">>> x = 1",
            "",
            ".. marimo::",
            "",
            "   x = 1",
        ]
        result = insert_marimo_directive(lines)
        assert result.count(".. marimo::") == 1

    def test_skips_if_disabled(self):
        lines = [
            ".. rubric:: Examples",
            "",
            ".. disable_marimo_try_it",
            "",
            ">>> x = 1",
        ]
        result = insert_marimo_directive(lines)
        assert ".. marimo::" not in "\n".join(result)

    def test_passes_options(self):
        lines = [
            ".. rubric:: Examples",
            "",
            ">>> x = 1",
        ]
        result = insert_marimo_directive(lines, height="600px", button_text="Run")
        joined = "\n".join(result)
        assert ":height: 600px" in joined
        assert ":button_text: Run" in joined


class TestMarimoIframe:
    def test_prompt_mode_html(self):
        node = MarimoIframe(iframe_src="https://marimo.app/?code=abc", prompt=True)
        html = node.html()
        assert "marimo-sphinx-try-it-button" in html
        assert "marimo-sphinx-iframe hidden" in html
        assert "marimoShowIframe" in html

    def test_direct_mode_html(self):
        node = MarimoIframe(
            iframe_src="https://marimo.app/?code=abc", prompt=False
        )
        html = node.html()
        assert "marimo-sphinx-iframe" in html
        assert "hidden" not in html
        assert "button" not in html

    def test_custom_dimensions(self):
        node = MarimoIframe(
            iframe_src="https://marimo.app/?code=abc",
            prompt=False,
            width="800px",
            height="600px",
        )
        html = node.html()
        assert 'width="800px"' in html
        assert "height:600px" in html
