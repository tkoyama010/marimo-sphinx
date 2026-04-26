import uuid

from docutils.nodes import Element


class MarimoIframe(Element):
    def __init__(
        self,
        rawsource="",
        *children,
        iframe_src="",
        width="100%",
        height="400px",
        prompt=True,
        button_text="Try in Marimo",
        **attributes,
    ):
        super().__init__(
            "",
            iframe_src=iframe_src,
            width=width,
            height=height,
            prompt=prompt,
            button_text=button_text,
        )

    def html(self) -> str:
        uid = uuid.uuid4().hex[:8]
        iframe_src = self["iframe_src"]
        width = self["width"]
        height = self["height"]
        button_text = self["button_text"]

        if self["prompt"]:
            return (
                f'<div class="marimo-sphinx-container">'
                f'<div class="marimo-sphinx-prompt">'
                f'<button id="marimo-btn-{uid}" class="marimo-sphinx-try-it-button"'
                f" onclick=\"marimoShowIframe('marimo-btn-{uid}', '{iframe_src}')\">"
                f"{button_text}"
                f"</button>"
                f"</div>"
                f'<iframe id="marimo-iframe-{uid}" class="marimo-sphinx-iframe hidden"'
                f' src="" width="{width}" style="height:{height};border:none;">'
                f"</iframe>"
                f"</div>"
            )
        return (
            f'<div class="marimo-sphinx-container">'
            f'<iframe class="marimo-sphinx-iframe"'
            f' src="{iframe_src}" width="{width}" style="height:{height};border:none;">'
            f"</iframe>"
            f"</div>"
        )
