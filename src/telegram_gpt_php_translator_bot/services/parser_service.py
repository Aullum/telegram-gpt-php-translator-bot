from bs4 import BeautifulSoup, NavigableString, Comment
from collections import OrderedDict


def is_visible(element: NavigableString) -> bool:
    parent = element.parent
    if parent.name in ["style", "script", "head", "meta", "[document]"]:
        return False
    if isinstance(element, Comment):
        return False
    return True


def extract_text_elements_from_html(html: str) -> tuple[str, dict[str, str]]:
    soup = BeautifulSoup(html, "lxml")
    element_map = OrderedDict()
    counter = 0

    for element in soup.find_all(string=True):
        if not is_visible(element):
            continue

        text = " ".join(element.split())
        if not text:
            continue

        marker = f"__chunk_{counter:04}__"
        element_map[marker] = text
        element.replace_with(marker)
        counter += 1

    return soup.prettify(formatter="html"), element_map


def apply_translations_to_html(html: str, translations: dict[str, str]) -> str:
    replaced_html = html

    for marker, translated in translations.items():
        replaced_html = replaced_html.replace(marker, translated)

    return replaced_html
