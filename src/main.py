from pathlib import Path

from workflows.indexing_workflow import index_document
from workflows.question_answering_workflow import answer_question


def main():
    document_id = "amit_resume"

    index_document(
        document_id=document_id,
        document_path=Path("resumes/resume.pdf"),
    )

    answer = answer_question(
        document_id=document_id,
        question="Can this candidate fit a full stack developer role?",
    )

    print(answer)


if __name__ == "__main__":
    main()