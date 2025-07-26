from telegram_gpt_php_translator_bot.services.parser_service import (
    extract_text_elements_from_html,
)
from telegram_gpt_php_translator_bot.services.parser_service import (
    apply_translations_to_html,
)


def test_extract_text_elements_basic():
    html = "<html><head><title>Test</title></head><body><h1>Hello</h1><p>World</p></body></html>"
    replaced_html, marker_map = extract_text_elements_from_html(html)

    assert isinstance(marker_map, dict)
    assert len(marker_map) == 3

    for marker in marker_map:
        assert marker in replaced_html

    texts = list(marker_map.values())
    assert "Test" in texts
    assert "Hello" in texts
    assert "World" in texts


def test_apply_translations_to_html_success():
    html = "<div>__chunk_0001__</div><p>__chunk_0002__</p>"
    translations = {
        "__chunk_0001__": "Bonjour",
        "__chunk_0002__": "Comment ça va?",
    }

    result = apply_translations_to_html(html, translations)

    assert "Bonjour" in result
    assert "Comment ça va?" in result
    assert "__chunk_" not in result
