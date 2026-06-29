def split_into_chunks(text:str) -> list[str]:
    chunks = []

    section_list = ["SUMMARY", "EXPERIENCE", "PROJECTS", "SKILLS", "EDUCATION"]
    section_positions: list[tuple[int, str]] = []
   
    for section in section_list:
        position = text.find(section)
        if position != -1:
            section_positions.append((position, section))

    section_positions.sort(key = lambda item: item[0])

    for index in range(len(section_positions)):
        start = section_positions[index][0]

        if index < len(section_positions) -1:
            end = section_positions[index + 1][0]
        else:
            end = len(text)
        
        chunk = text[start:end].strip()

        chunks.append(chunk)
        
    return chunks