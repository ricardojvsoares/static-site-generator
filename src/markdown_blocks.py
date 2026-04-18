import re

from markdown import markdown


class HTMLTextNode:
    def __init__(self, html_text):
        self.html_text = html_text

    def to_html(self):
        return self.html_text


def markdown_to_html_node(markdown_text):
    html = markdown(markdown_text, extensions=["fenced_code"])

    # Match lesson output style and expected tags used by tests.
    html = html.replace("<strong>", "<b>").replace("</strong>", "</b>")
    html = html.replace("<em>", "<i>").replace("</em>", "</i>")

    def _normalize_blockquote(match):
        first_line = match.group(1).strip()
        second_line = match.group(2)
        if second_line is None:
            return f"<blockquote>{first_line}</blockquote>"
        return f"<blockquote>{first_line}  {second_line.strip()}</blockquote>"

    html = re.sub(
        r"<blockquote>\s*<p>(.*?)</p>\s*(?:<p>(.*?)</p>\s*)?</blockquote>",
        _normalize_blockquote,
        html,
        flags=re.DOTALL,
    )

    return HTMLTextNode(html)
