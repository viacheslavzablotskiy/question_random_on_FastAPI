from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.operation_question.schemas import QuestionAnswer, QuestionDBID
from app.models import User
from app.auth.security.auth_security import get_current_user
from app.operation_question.service import create_question_and_receiving_answer, get_all_questions

router = APIRouter()


@router.post('/create_question', response_model=QuestionAnswer, tags=['question'])
async def create_question(obj_in: QuestionDBID,
                          db_session: AsyncSession = Depends(get_async_session),
                          get_current_user: User = Depends(get_current_user)):
    question = await create_question_and_receiving_answer(
        db_session=db_session, obj_in=obj_in,
    )
    return question


@router.get('/get_all_question', response_model=List[QuestionAnswer], tags=['question'])
async def get_all_question(skip: int = 0, limit: int = 100,
                           db_session: AsyncSession = Depends(get_async_session),
                           ):
    questions = await get_all_questions(
        db_session=db_session
    )
    return questions
