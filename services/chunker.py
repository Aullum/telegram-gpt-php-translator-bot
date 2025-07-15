# services/chunker.py

import re
import logging

logger = logging.getLogger(__name__)

def smart_split_large(content: str, max_chunk_len: int = 8000) -> list[str]:
    section_pattern = r'(<section[^>]*>.*?</section>|<div[^>]*class="[^"]*(?:section|block|content)[^"]*"[^>]*>.*?</div>|<\?php.*?\?>)'
    sections = re.split(section_pattern, content, flags=re.DOTALL | re.IGNORECASE)

    chunks = []
    current_chunk = ""

    def force_split_by_length(text: str) -> list[str]:
        # Грубое деление по max_chunk_len, не ломает порядок
        return [text[i:i+max_chunk_len] for i in range(0, len(text), max_chunk_len)]

    def split_too_large(section: str) -> list[str]:
        if len(section) <= max_chunk_len:
            return [section]
        # Сначала пробуем разбить по абзацам (пустым строкам)
        parts = re.split(r'(\n\s*\n|\r\n\r\n)', section)
        sub_chunks = []
        sub_chunk = ""
        for part in parts:
            if len(sub_chunk) + len(part) > max_chunk_len and sub_chunk.strip():
                sub_chunks.append(sub_chunk)
                sub_chunk = part
            else:
                sub_chunk += part
        if sub_chunk.strip():
            sub_chunks.append(sub_chunk)
        # Если после деления хоть один sub_chunk всё ещё слишком большой — режем по длине
        really_final = []
        for chunk in sub_chunks:
            if len(chunk) > max_chunk_len:
                really_final.extend(force_split_by_length(chunk))
            else:
                really_final.append(chunk)
        return really_final

    for section in sections:
        if not section.strip():
            continue

        # если кусок слишком большой — сначала дробим
        if len(section) > max_chunk_len:
            small_parts = split_too_large(section)
            for part in small_parts:
                if len(current_chunk) + len(part) > max_chunk_len and current_chunk.strip():
                    chunks.append(current_chunk)
                    current_chunk = part
                else:
                    current_chunk += part
        else:
            if len(current_chunk) + len(section) > max_chunk_len and current_chunk.strip():
                chunks.append(current_chunk)
                current_chunk = section
            else:
                current_chunk += section

    if current_chunk.strip():
        chunks.append(current_chunk)

    return chunks
