from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective

from ._docstring import code_to_marimo_url
from .nodes import MarimoIframe


class MarimoDirective(SphinxDirective):
    """Embed an interactive Marimo notebook in documentation."""

    has_content = True
    required_arguments = 0
    option_spec = {
        "width": directives.unchanged,
        "height": directives.unchanged,
        "prompt": directives.flag,
        "button_text": directives.unchanged,
    }

    def run(self):
        code = "\n".join(self.content)
        width = self.options.get("width", "100%")
        height = self.options.get("height", self.env.config.marimo_global_height)
        button_text = self.options.get(
            "button_text", self.env.config.marimo_global_button_text
        )
        prompt = "prompt" in self.options or self.env.config.marimo_global_prompt

        iframe_src = code_to_marimo_url(code)
        node = MarimoIframe(
            iframe_src=iframe_src,
            width=width,
            height=height,
            prompt=prompt,
            button_text=button_text,
        )
        return [node]
