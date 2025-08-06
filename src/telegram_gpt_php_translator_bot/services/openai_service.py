from collections import OrderedDict
import tiktoken
import json
from openai import AsyncOpenAI
from telegram_gpt_php_translator_bot.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

MODEL = "gpt-4o"
MAX_TOKENS = 3500
_enc = tiktoken.encoding_for_model(MODEL)


async def translate_chunk(json_input: dict[str, str], lang: str) -> dict[str, str]:
    json_str = json.dumps(json_input, ensure_ascii=False, indent=2)

    system_msg = {
        "role": "system",
        "content": "You are a professional translator. Follow user instructions exactly.",
    }

    user_guide = {
        "role": "user",
        "content": f"""
You are a professional translator and localization expert. Translate ONLY the JSON values into {lang}.

## Personal Name Policy
- Replace BOTH given names **and** family names with common {lang} full names.
- Do NOT transliterate. Do NOT keep any part of the original spelling.
- Each character in this chunk must get a UNIQUE full name.
- If the same person appears twice **in this chunk**, reuse the exact same localized name.

Examples (Hungarian → German):
"Hegedűs Anna"          → "Anna Müller"
"Lopes-Szabó Zsuzsa"    → "Susanne Berger"
"Szabó György"          → "Jürgen Schneider"

## Other localisation rules
- Adapt places, companies, products, job titles
- Convert currencies, dates, phone numbers
- Preserve tone and marketing intent

## Never do
- Modify keys or JSON structure
- Add comments, explanations, markdown, or code blocks

Return valid JSON only.
""",
    }

    user_msg = {"role": "user", "content": json_str}

    resp = await client.chat.completions.create(
        model=MODEL,
        messages=[system_msg, user_guide, user_msg],
        response_format={"type": "json_object"},
        temperature=0.3,
        max_tokens=4000,
    )
    return json.loads(resp.choices[0].message.content)


async def translate_elements(element_map: dict[str, str], lang: str) -> dict[str, str]:
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
    for i, chunk in enumerate(chunks, start=1):
        result = await translate_chunk(chunk, lang)
        translated.update(result)

    missing = set(element_map) - set(translated)
    attempt = 1
    while missing:
        retry_chunk = OrderedDict((k, element_map[k]) for k in missing)
        try:
            retry_result = await translate_chunk(retry_chunk, lang)
            translated.update(retry_result)
        except Exception as e:
            raise RuntimeError(f"Retry failed: {e}")
        missing = set(element_map) - set(translated)
        attempt += 1

    return translated
