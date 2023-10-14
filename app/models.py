from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=True)

    question = relationship("Question", back_populates='user')


class Question(Base):
    __tablename__ = "question"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, unique=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    answer = Column(String)

    user = relationship("User", back_populates="question")
