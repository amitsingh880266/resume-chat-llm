from fastapi import APIRouter

from src.api.schemas.question_request import QuestionRequest
from src.api.schemas.question_response import QuestionResponse
from src.workflows.question_answering_workflow import answer_question

router = APIRouter(
    prefix="/questions",
    tags = ["Questions"]
)

@router.post("")
def ask_question(request: QuestionRequest) -> QuestionResponse:
    answer =  answer_question(request.document_id, request.question)
    return QuestionResponse(answer=answer)