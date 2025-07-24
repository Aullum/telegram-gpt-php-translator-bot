from telegram_gpt_php_translator_bot.services.parser_service import extract_visible_text


def test_extract_visible_text_basic():
    html = "<html><head><title>Test</title></head><body><h1>Hello</h1><p>World</p></body></html>"
    replaced_html, chunks, marker_map = extract_visible_text(html)

    assert len(chunks) == 2
    assert all("Hello" in v or "World" in v for v in marker_map.values())
    for marker in marker_map:
        assert marker in replaced_html
