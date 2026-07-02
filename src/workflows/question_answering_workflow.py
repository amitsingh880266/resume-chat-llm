from src.services.embedding_service import generate_embedding
from src.services.prompt_service import build_document_prompt
from src.services.chroma_service import query_chunks
from src.services.llm_service import ask_llm

def answer_question(document_id: str, question: str)-> str:
    if not document_id.strip():
        raise ValueError("Document ID cannot be empty.")

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    question_embedding = generate_embedding(question)

    relevant_chunks = query_chunks(document_id, question_embedding)
    prompt = build_document_prompt(relevant_chunks, question)

    # answer = ask_llm(prompt)

    return prompt