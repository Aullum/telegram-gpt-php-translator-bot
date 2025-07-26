import pytest
from telegram_gpt_php_translator_bot.services.openai_service import translate_elements


@pytest.mark.asyncio
async def test_translate_elements_json_mock(mocker):
    input_map = {
        "__chunk_0001__": "Welcome",
        "__chunk_0002__": "Click here",
        "__chunk_0003__": "Explore tools",
    }

    mocked_json_response = """
    {
        "__chunk_0001__": "Добро пожаловать",
        "__chunk_0002__": "Нажмите здесь",
        "__chunk_0003__": "Изучить инструменты"
    }
    """

    mocker.patch(
        "telegram_gpt_php_translator_bot.services.openai_service.translate_chunk",
        return_value=mocked_json_response,
    )

    result = await translate_elements(input_map, "Russian")

    assert isinstance(result, dict)
    assert len(result) == 3
    assert result["__chunk_0001__"] == "Добро пожаловать"
    assert result["__chunk_0002__"] == "Нажмите здесь"
    assert result["__chunk_0003__"] == "Изучить инструменты"
