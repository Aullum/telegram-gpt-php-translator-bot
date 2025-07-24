from bs4 import BeautifulSoup, NavigableString, Comment
import uuid


def extract_visible_text(html: str) -> tuple[str, list[str], dict[str, str]]:
    soup = BeautifulSoup(html, "lxml")
    text_chunks = []
    marker_map = {}

    def is_visible(tag):
        return tag.parent.name not in [
            "style",
            "script",
            "head",
            "title",
            "meta",
            "[document]",
        ] and not isinstance(tag, Comment)

    for element in soup.find_all(string=True):
        if isinstance(element, NavigableString) and is_visible(element):
            stripped = element.strip()
            if stripped:
                marker = f"__chunk_{uuid.uuid4().hex[:8]}__"
                marker_map[marker] = stripped
                text_chunks.append(stripped)
                element.replace_with(marker)

    return str(soup), text_chunks, marker_map
