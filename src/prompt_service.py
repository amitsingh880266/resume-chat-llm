def build_resume_prompt (resume_text: str, question: str) -> str:
    return f"""
    Based on the given resume answer the question in just one word.

    Resume:
    {resume_text}

    Question:
    {question}
    """