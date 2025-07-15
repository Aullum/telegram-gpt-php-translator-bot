# services/chunker.py

import re
import logging

logger = logging.getLogger(__name__)

def smart_split_large(content: str, max_chunk_len: int = 8000) -> list[str]:
    """
    Splits HTML/PHP content into logical chunks for translation.
    Keeps <section>, <div>, <?php ?> blocks grouped when possible.
    """
    section_pattern = r'(<section[^>]*>.*?</section>|<div[^>]*class="[^\"]*(?:section|block|content)[^\"]*"[^>]*>.*?</div>|<\?php.*?\?>)'
    sections = re.split(section_pattern, content, flags=re.DOTALL | re.IGNORECASE)

    chunks = []
    current_chunk = ""

    for section in sections:
        if not section.strip():
            continue
        if len(current_chunk) + len(section) > max_chunk_len and current_chunk.strip():
            chunks.append(current_chunk)
            current_chunk = section
        else:
            current_chunk += section

    if current_chunk.strip():
        chunks.append(current_chunk)

    if len(chunks) > 12:
        logger.warning(f"Too many chunks ({len(chunks)}), merging...")
        final_chunks = []
        current_chunk = ""

        for chunk in chunks:
            if len(current_chunk) + len(chunk) > max_chunk_len * 1.5 and current_chunk.strip():
                final_chunks.append(current_chunk)
                current_chunk = chunk
            else:
                current_chunk += chunk

        if current_chunk.strip():
            final_chunks.append(current_chunk)

        chunks = final_chunks

    return chunks
