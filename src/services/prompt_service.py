def build_resume_prompt (context: str, question: str) -> str:
    return f"""
    Answer using ONLY the context.
    Reply with one word.

    Context:
    {context}

    Question:
    {question}
    """