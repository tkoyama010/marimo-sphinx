"""marimo-sphinx: Sphinx extension for embedding Marimo notebooks in API docs."""

from pathlib import Path
from typing import List

from docutils.nodes import SkipNode
from sphinx.application import Sphinx
from sphinx.util.fileutil import copy_asset

from ._docstring import insert_marimo_directive
from .directives import MarimoDirective
from .nodes import MarimoIframe

__version__ = "0.1.0"

HERE = Path(__file__).parent


def _skip(self, node):
    raise SkipNode


def _visit_marimo_iframe(self, node):
    self.body.append(node.html())
    raise SkipNode


def _copy_static_files(app: Sphinx, exception) -> None:
    if exception:
        return
    static_dir = Path(app.outdir) / "_static"
    copy_asset(str(HERE / "_static" / "marimo_sphinx.js"), str(static_dir))
    copy_asset(str(HERE / "_static" / "marimo_sphinx.css"), str(static_dir))


def _process_autodoc_docstrings(
    app: Sphinx, what: str, name: str, obj, options, lines: List[str]
) -> None:
    marimo_options = {}
    button_text = app.config.marimo_global_button_text
    height = app.config.marimo_global_height
    if button_text:
        marimo_options["button_text"] = button_text
    if height:
        marimo_options["height"] = height
    modified = insert_marimo_directive(lines, **marimo_options)
    lines.clear()
    lines.extend(modified)


def _conditional_process_examples(app: Sphinx, config) -> None:
    if config.global_enable_marimo_examples:
        app.connect("autodoc-process-docstring", _process_autodoc_docstrings)


def setup(app: Sphinx) -> dict:
    app.add_node(
        MarimoIframe,
        html=(_visit_marimo_iframe, None),
        latex=(_skip, None),
        text=(_skip, None),
        man=(_skip, None),
        texinfo=(_skip, None),
    )

    app.add_directive("marimo", MarimoDirective)

    app.add_config_value("global_enable_marimo_examples", False, "html")
    app.add_config_value("marimo_global_button_text", "Try in Marimo", "html")
    app.add_config_value("marimo_global_height", "400px", "html")
    app.add_config_value("marimo_global_prompt", True, "html")

    app.connect("config-inited", _conditional_process_examples)
    app.connect("build-finished", _copy_static_files)

    app.add_css_file("marimo_sphinx.css")
    app.add_js_file("marimo_sphinx.js")

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "env_version": 1,
    }
