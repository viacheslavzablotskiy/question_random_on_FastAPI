from typing import Optional

from pydantic import BaseModel


class QuestionBase(BaseModel):
    id: Optional[int] = None
    user_id: int


class QuestionID(QuestionBase):
    question_id: int = None

    class Config:
        orm_mode = True


class QuestionAnswer(QuestionID):
    answer: Optional[str] = None


class QuestionDBID(BaseModel):
    question_num: int


