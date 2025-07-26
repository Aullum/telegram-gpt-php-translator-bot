import json
from openai import AsyncOpenAI
import tiktoken
from telegram_gpt_php_translator_bot.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

MODEL = "gpt-4o"
MAX_TOKS = 8180

_enc = tiktoken.encoding_for_model(MODEL)


async def translate_chunk(json_input: dict[str, str], lang: str) -> str:
    prompt = f"""
You are a professional translator and localization expert.

Translate ONLY the values of the following JSON dictionary into {lang}.
DO NOT modify the keys. DO NOT change the JSON structure or formatting.

Return the result as valid JSON using the same key:value structure.

✅ Translation & Localization Guidelines:
- Adapt names of people, places, companies, and products to the target culture.
- Localize phone numbers, currencies, date/time formats.
- Maintain tone, emotion, and intent of each message.
- Translate slogans and marketing phrases to sound natural in the target language.

🚫 Do NOT:
- Modify or translate the keys
- Add comments or explanations
- Change the structure or format of the JSON
- Wrap the result in Markdown or code blocks

Here is the JSON input:
{json_input}

Respond with the translated JSON only:
"""

    messages = [{"role": "user", "content": prompt}]
    resp = await client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.3,
        top_p=0.9,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        response_format="json",
    )
    return resp.choices[0].message.content.strip()


async def translate_elements(element_map: dict[str, str], lang: str) -> dict[str, str]:
    batches = []
    current_batch = {}
    current_tokens = 0

    for marker, text in element_map.items():
        tokens = len(_enc.encode(text))
        if current_tokens + tokens > MAX_TOKS - 500 and current_batch:
            batches.append(current_batch)
            current_batch = {}
            current_tokens = 0

        current_batch[marker] = text
        current_tokens += tokens

    if current_batch:
        batches.append(current_batch)

    translated_map = {}

    for batch in batches:
        json_input = json.dumps(batch, ensure_ascii=False, indent=2)
        translated_raw = await translate_chunk(json_input, lang)

        try:
            translated_batch = json.loads(translated_raw)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON returned from OpenAI: {e}")

        translated_map.update(translated_batch)

    return translated_map
