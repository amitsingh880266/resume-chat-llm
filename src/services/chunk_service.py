def split_into_sections(text: str) -> list[str]:
    SECTION_HEADERS = [
        "SUMMARY",
        "EXPERIENCE",
        "PROJECTS",
        "SKILLS",
        "EDUCATION",
    ]

    sections: list[str] = []
    section_positions: list[tuple[int, str]] = []

    for section in SECTION_HEADERS:
        position = text.find(section)

        if position != -1:
            section_positions.append((position, section))

    section_positions.sort(key=lambda item: item[0])

    for index in range(len(section_positions)):
        start = section_positions[index][0]

        if index < len(section_positions) - 1:
            end = section_positions[index + 1][0]
        else:
            end = len(text)

        section = text[start:end].strip()

        sections.append(section)

    return sections


def split_large_section(
    section: str,
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if overlap < 0:
        raise ValueError("overlap cannot be negative.")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    chunks: list[str] = []

    start = 0
    section_length = len(section)

    while start < section_length:
        end = min(start + chunk_size, section_length)

        chunks.append(
            section[start:end].strip()
        )

        start += chunk_size - overlap

    return chunks


def split_into_chunks(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[str]:
    if not text.strip():
        raise ValueError("Text cannot be empty.")

    chunks: list[str] = []

    sections = split_into_sections(text)

    for section in sections:
        if len(section) <= chunk_size:
            chunks.append(section)
        else:
            chunks.extend(
                split_large_section(
                    section=section,
                    chunk_size=chunk_size,
                    overlap=overlap,
                )
            )

    return chunks