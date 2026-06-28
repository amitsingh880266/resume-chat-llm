from pathlib import Path

from models.chunk import Chunk
from services.chunk_service import chunk_text
from services.embedding_service import generate_embedding
from services.llm_service import ask_llm
from services.pdf_service import read_pdf
from services.prompt_service import build_resume_prompt
from services.retrieval_service import retrieve_relevant_chunks


def main():
    resume_path = Path("resumes/resume.pdf")

    question = "Can this candidate fit a full stack developer role?"

    # Step 1: Read the resume
    resume_text = read_pdf(resume_path)

    # Step 2: Split into chunks
    chunk_texts = chunk_text(resume_text)

    # Step 3: Generate embeddings for each chunk
    chunks: list[Chunk] = []

    for chunk in chunk_texts:
        embedding = generate_embedding(chunk)

        chunks.append(
            Chunk(
                text=chunk,
                embedding=embedding,
            )
        )

    # Step 4: Generate embedding for the user's question
    question_embedding = generate_embedding(question)

    # Step 5: Retrieve the most relevant chunks
    top_chunks = retrieve_relevant_chunks(
        chunks=chunks,
        query_embedding=question_embedding,
        top_k=3,
    )

    # Step 6: Build context from retrieved chunks
    context = "\n\n".join(
        chunk.text for chunk in top_chunks
    )

    # Step 7: Build the prompt
    prompt = build_resume_prompt(
        context=context,
        question=question,
    )

    # Step 8: Ask the LLM
    answer = ask_llm(prompt)

    print("\nAnswer")
    print("=" * 80)
    print(answer)


if __name__ == "__main__":
    main()