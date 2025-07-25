import pytest
from telegram_gpt_php_translator_bot.services.openai_service import translate_chunks


@pytest.mark.asyncio
async def test_translate_chunks_mocker(mocker):
    fake = ["Hello", "World"]

    mocker.patch(
        "telegram_gpt_php_translator_bot.services.openai_service.translate_chunk",
        side_effect=lambda txt, lang: txt.upper(),
    )
    res = await translate_chunks(fake, "EN")
    assert res == ["HELLO", "WORLD"]
