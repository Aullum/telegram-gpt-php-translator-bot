# services/translator.py

import os
import openai
import asyncio
import logging
from utils.validators import clean_markdown_wrappers, is_valid_translation

logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

def build_large_chunk_prompt(chunk: str, lang: str, chunk_num: int, total_chunks: int) -> str:
    """
    Builds a rich translation prompt with strong localization instructions.
    """
    return f"""
You are a professional translator and web localizer. You are translating part {chunk_num} of {total_chunks} of a large landing page.

⚠️ CRITICALLY IMPORTANT for consistency:
- This is part {chunk_num} out of {total_chunks} of the same single page
- Create UNIQUE first and last names for each person in this part
- Use culturally appropriate names for the target language
- If multiple people are mentioned, assign DIFFERENT names to each

🚫 STRICTLY FORBIDDEN:
- Do NOT change any PHP code (`<?php ... ?>`)
- Do NOT alter HTML tags or their attributes (only translate content)
- Do NOT change CSS classes or inline styles
- Do NOT modify JavaScript logic
- Do NOT add or remove any code lines
- Do NOT add comments or explanations
- Do NOT wrap the result in markdown or triple backticks
- Do NOT change the structure of the file

✅ YOU MUST translate and localize:
- All visible text between HTML tags
- Attribute values: title="", placeholder="", alt="", value=""
- PHP strings: echo "Text"; print 'Text';
- Text inside JavaScript strings
- Names, places, company names, addresses, phone numbers

🌍 LOCALIZATION RULES:
- Adapt personal names to culturally appropriate ones (each should be UNIQUE)
- Replace nationalities with appropriate equivalents (e.g. “Japanese developer” → “German developer”)
- Adapt company names, professions, and geographic locations
- Use local currency and date formats
- Reflect cultural norms and real-world examples in the target region

🧠 TRANSLATION QUALITY:
- Preserve the tone and emotional intent of the original
- Make the result sound natural to native speakers
- Adapt marketing slogans and expressions to the target culture

Target language: {lang}

--- START OF CONTENT ---
{chunk}
--- END OF CONTENT ---

Now provide ONLY the translated and localized content below (no commentary):
"""

async def translate_large_chunk(chunk: str, lang: str, chunk_num: int, total_chunks: int, max_retries: int = 2) -> str:
    """
    Sends a chunk to OpenAI for translation and validates response.
    """
    for attempt in range(max_retries):
        try:
            prompt = build_large_chunk_prompt(chunk, lang, chunk_num, total_chunks)

            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1 if attempt == 0 else 0.3,
                max_tokens=min(12000, int(len(chunk) * 1.5)),
                timeout=120,
                seed=chunk_num
            )

            translated = clean_markdown_wrappers(response.choices[0].message.content)

            if is_valid_translation(chunk, translated):
                return translated

        except Exception as e:
            logger.warning(f"Part {chunk_num}: translation error: {e}")
            await asyncio.sleep(5)

    logger.error(f"Part {chunk_num}: translation failed, returning original")
    return chunk
