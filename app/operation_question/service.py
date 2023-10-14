from urllib.request import urlopen

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.operation_question.schemas import QuestionDBID, QuestionAnswer
from app.models import User, Question
from app.auth.security.auth_security import get_current_user


async def get_bytes(question_id: int):
    async with urlopen(f'https://jservice.io/api/random?count={question_id}') as page:
        return page.readlines()


async def create_question_and_receiving_answer(
        obj_in: QuestionDBID,
        db_session: AsyncSession,
        get_current_user: User = Depends(get_current_user),
):
    query = select(Question)
    result = await db_session.execute(query)
    len_count = len(result.scalars().all())

    get_current_user = jsonable_encoder(get_current_user)
    get_id_current_user = get_current_user.get('id')

    this_bytes = await get_bytes(obj_in.question_num)
    this_bytes_in_string = this_bytes[0].decode('utf-8')

    answer = QuestionAnswer(id=len_count + 1, user_id=get_id_current_user,
                            answer=this_bytes_in_string)

    test_query = select(Question).where(Question.question_id == obj_in.question_num)
    test_result = await db_session.execute(test_query)
    if test_result.scalars().first():
        raise HTTPException(
            status_code=400, detail='This Question already exists in system'
        )

    query_answer = insert(Question).values(**answer.dict())

    await db_session.execute(query_answer)
    await db_session.commit()

    query_for_return = select(Question).where(Question.id == answer.id)
    result_for_return = await db_session.execute(query_for_return)
    return result_for_return.scalars().first()


async def get_all_questions(
        db_session: AsyncSession,
        skip: int = 0, limit: int = 100,
):
    query = select(Question).limit(limit)
    result = await db_session.execute(query)
    return result.scalars().all()
