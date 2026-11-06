from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Table
from sqlalchemy.orm import relationship

from database import Base


# ── Association tables ────────────────────────────────────────────────────────

lesson_words = Table(
    "lesson_words",
    Base.metadata,
    Column("lesson_id", ForeignKey("lessons.id"), primary_key=True),
    Column("word_id", ForeignKey("words.id"), primary_key=True),
)

user_lessons_done = Table(
    "user_lessons_done",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("lesson_id", ForeignKey("lessons.id"), primary_key=True),
)

word_corespondance_words = Table(
    "word_corespondance_words",
    Base.metadata,
    Column("corespondance_id", ForeignKey("word_corespondance.id"), primary_key=True),
    Column("word_id", ForeignKey("words.id"), primary_key=True),
)


# ── Core tables ───────────────────────────────────────────────────────────────

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    string = Column(String, nullable=False)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)

    video = relationship("Video")
    lessons = relationship("Lesson", secondary=lesson_words, back_populates="words")
    corespondances = relationship(
        "WordCorespondance",
        secondary=word_corespondance_words,
        back_populates="word_items",
    )


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

    words = relationship("Word", secondary=lesson_words, back_populates="lessons")
    users_completed = relationship(
        "User", secondary=user_lessons_done, back_populates="lessons_done"
    )


class WordCorespondance(Base):
    __tablename__ = "word_corespondance"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, unique=True, nullable=False, index=True)
    words = Column(JSON, nullable=False, default=list)  # List of Word IDs: [1, 2]

    word_items = relationship(
        "Word",
        secondary=word_corespondance_words,
        back_populates="corespondances",
    )

    def get_words(self, db) -> list[Word]:
        if self.word_items:
            return list(self.word_items)
        if not self.words:
            return []
        return db.query(Word).filter(Word.id.in_(self.words)).all()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    premium = Column(Boolean, default=False, nullable=False)
    creation_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    lessons_done = relationship(
        "Lesson", secondary=user_lessons_done, back_populates="users_completed"
    )