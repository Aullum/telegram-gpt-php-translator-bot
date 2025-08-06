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
        "content": f"""
You are an elite translator & localization specialist.
Task: translate *only* the JSON values into {lang}.
Return **valid JSON only**, same keys – no extra fields.

### Localization rules (must-follow):
1. Replace demonyms/adjectives of nationality with the target one
   (e.g. 'Hungarian seller' → 'Romanian seller').
2. Transliterate or localize personal names to the target language rules.
3. If a company/product has an established local name, use it;
   otherwise keep the brand in Latin script and localize legal suffixes (Inc., LLC, Kft. → SRL etc.).
4. Localize currencies, phone formats, and dates.
5. Preserve tone & intent, no explanations.
6. Use exactly the same spelling for every personal name
   each time it appears. Do NOT invent alternatives.
""",
    }

    user_msg = {"role": "user", "content": json_str}

    resp = await client.chat.completions.create(
        model=MODEL,
        messages=[system_msg, user_msg],
        response_format={"type": "json_object"},
        temperature=0.1,
        top_p=1.0,
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
