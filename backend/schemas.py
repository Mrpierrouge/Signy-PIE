from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# ── Word ──────────────────────────────────────────────────────────────────────

class WordListItem(BaseModel):
    id: int
    string: str
    video: str


class WordDetail(BaseModel):
    id: int
    string: str
    video: str


# ── Lesson ────────────────────────────────────────────────────────────────────

class LessonListItem(BaseModel):
    id: int
    title: str
    words: List[WordDetail]


class LessonDetail(LessonListItem):
    id: int
    title: str
    words: List[WordDetail]


# ── User ──────────────────────────────────────────────────────────────────────

class UserListItem(BaseModel):
    id: int
    nom: str
    prenom: str
    email: str
    premium: bool
    creation_date: datetime
    lessons_done: List[LessonListItem]


class UserDetail(BaseModel):
    id: int
    nom: str
    prenom: str
    email: str
    premium: bool
    creation_date: datetime
    lessons_done: List[LessonListItem]


# ── Video ─────────────────────────────────────────────────────────────────────
class VideoListItem(BaseModel):
    id: int
    url: str


class VideoDetail(VideoListItem):
    id: int
    url: str


# ── Word Corespondance ────────────────────────────────────────────────────────

class WordCorespondanceListItem(BaseModel):
    id: int
    label: str
    words: List[int]


class WordCorespondanceDetail(BaseModel):
    id: int
    label: str
    words: List[int]
    matched_words: List[WordDetail] = []


# ── AI ────────────────────────────────────────────────────────────────────────

class AIWordResponse(BaseModel):
    word: str
    confidence: Optional[float] = None
    label: str
    true_label: Optional[str] = None
    matched_word_ids: List[int] = []
    matched_words: List[str] = []
    is_valid: bool = True
    tested_word: Optional[str] = None
    message: Optional[str] = None