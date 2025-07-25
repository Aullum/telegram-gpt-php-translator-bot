import asyncio
from typing import Generator, Sequence

from openai import AsyncOpenAI
import tiktoken
from telegram_gpt_php_translator_bot.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

MODEL = "gpt-4o"
MAX_TOKS = 8180

_enc = tiktoken.encoding_for_model(MODEL)


def _chunks_of_tokens(text: str, limit: int) -> Generator[str, None, None]:
    tokens = _enc.encode(text)
    for i in range(0, len(tokens), limit):
        yield _enc.decode(tokens[i : i + limit])


async def translate_chunk(text: str, lang: str) -> str:
    messages = [
        {
            "role": "user",
            "content": (
                f"Translate the following HTML fragment to {lang}.\n"
                "Keep HTML entities and markup intact. Only translate human-readable text.\n\n"
                f"{text}"
            ),
        }
    ]
    resp = await client.chat.completions.create(model=MODEL, messages=messages)
    return resp.choices[0].message.content.strip()


async def translate_chunks(texts: Sequence[str], lang: str) -> list[str]:
    tasks: list[asyncio.Task] = []
    for txt in texts:
        for part in _chunks_of_tokens(txt, MAX_TOKS // 2):
            tasks.append(asyncio.create_task(translate_chunk(part, lang)))
    results = await asyncio.gather(*tasks)
    return results
