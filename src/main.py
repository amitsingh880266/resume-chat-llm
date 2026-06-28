from pathlib import Path
import argparse

from workflows.indexing_workflow import index_document
from workflows.question_answering_workflow import answer_question


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--question",
        required = True,
        help = "Question to ask about the document."
    )

    args = parser.parse_args()

    document_id = "amit_resume"

    index_document(
        document_id=document_id,
        document_path=Path("resumes/resume.pdf"),
    )

    answer = answer_question(
        document_id=document_id,
        question=args.question
    )

    print(answer)


if __name__ == "__main__":
    main()