from pathlib import Path
import argparse

from workflows.indexing_workflow import index_document
from workflows.question_answering_workflow import answer_question
from services.chroma_service import document_exists

document_id = "amit_resume"

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--question",
        required = True,
        help = "Question to ask about the document."
    )

    args = parser.parse_args()

    if not document_exists(document_id):
        print("Index not found. Indexing document...")

        index_document(
            document_path=Path("resumes/resume.pdf"),
        )
    else:
        print("Using existing document index.")

    answer = answer_question(
        document_id=document_id,
        question=args.question
    )

    print(answer)


if __name__ == "__main__":
    main()