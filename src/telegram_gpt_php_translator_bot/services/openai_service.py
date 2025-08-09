from collections import OrderedDict
import json
import tiktoken
from openai import AsyncOpenAI
from telegram_gpt_php_translator_bot.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

MODEL = "gpt-4.1"
MAX_TOKENS = 3500

try:
    _enc = tiktoken.encoding_for_model(MODEL)
except Exception:
    _enc = tiktoken.get_encoding("cl100k_base")


async def translate_chunk(json_input: dict[str, str], lang: str) -> dict[str, str]:
    """Translate only JSON values while preserving keys and structure."""
    json_str = json.dumps(json_input, ensure_ascii=False, indent=2)

    system_prompt = {
        "role": "system",
        "content": (
            "You are a professional website localizer.\n"
            "Translate ONLY the values of this JSON object into the specified language.\n"
            "Keep the JSON structure and all keys unchanged.\n"
            "Return valid JSON. No markdown, no comments, no explanations."
        ),
    }

    user_prompt = {
        "role": "user",
        "content": f"""
Translate this JSON object into {lang}. Follow these rules:

1. Replace personal full names with culturally appropriate full names in {lang}.
2. Each character must receive a UNIQUE full name if present in this chunk.
3. DO NOT keep original spelling. DO NOT transliterate.
4. Reuse the same localized name if the same person appears more than once in this chunk.
5. Adapt places, companies, products, job titles, dates, and currencies.
6. Preserve tone, intent, and marketing style.

Only translate the values. Do not change the structure or keys.

JSON to translate:
{json_str}
""",
    }

    resp = await client.chat.completions.create(
        model=MODEL,
        messages=[system_prompt, user_prompt],
        response_format={"type": "json_object"},
        temperature=0.3,
        max_tokens=4000,
    )

    return json.loads(resp.choices[0].message.content)


async def translate_elements(element_map: dict[str, str], lang: str) -> dict[str, str]:
    """Chunk long inputs by value token count and merge translations."""
    chunks = []
    current_chunk = OrderedDict()
    current_tokens = 0

    for key, value in element_map.items():
        tokens = len(_enc.encode(value))
        if current_tokens + tokens > MAX_TOKENS and current_chunk:
            chunks.append(current_chunk)
            current_chunk = OrderedDict()
            current_tokens = 0

        current_chunk[key] = value
        current_tokens += tokens

    if current_chunk:
        chunks.append(current_chunk)

    translated = OrderedDict()
    for chunk in chunks:
        result = await translate_chunk(chunk, lang)
        translated.update(result)

    return translated
