from services.storage_service import load_chunks
from services.embedding_service import generate_embedding
from services.retrieval_service import retrieve_relevant_chunks
from services.prompt_service import build_document_prompt
from services.llm_service import ask_llm

def answer_question(document_id: str, question: str)-> str:
    if not document_id.strip():
        raise ValueError("Document ID cannot be empty.")

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    chunks = load_chunks(document_id)

    question_embedding = generate_embedding(question)

    relevant_chunks = retrieve_relevant_chunks(chunks, question_embedding)

    prompt = build_document_prompt(relevant_chunks, question)

    # answer = ask_llm(prompt)

    return prompt