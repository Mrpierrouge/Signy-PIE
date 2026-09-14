from typing import Dict, List, Optional

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from ai_service import VideoWordPredictor
from database import Base, SessionLocal, engine
from models import Lesson, User, Video, Word
from schemas import (
    AIWordResponse,
    LessonDetail,
    LessonListItem,
    UserDetail,
    UserListItem,
    WordDetail,
    WordListItem,
    VideoDetail,
    VideoListItem,
)


app = FastAPI(title="Signy PIE API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = VideoWordPredictor()


def serialize_word(word: Word) -> WordDetail:
    return WordDetail(id=word.id, string=word.string, video=word.video.url)


def serialize_lesson(lesson: Lesson) -> LessonListItem:
    return LessonListItem(
        id=lesson.id,
        title=lesson.title,
        words=[serialize_word(word) for word in lesson.words],
    )


def serialize_lesson_detail(lesson: Lesson) -> LessonDetail:
    return LessonDetail(
        id=lesson.id,
        title=lesson.title,
        words=[serialize_word(word) for word in lesson.words],
    )

def serialize_video(video: Video) -> VideoDetail:
    return VideoDetail(id=video.id, url=video.url)


# ── DB dependency ─────────────────────────────────────────────────────────────

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── Seed data ─────────────────────────────────────────────────────────────────

def seed_database(db: Session) -> None:
    if db.query(Video).first() is not None:
        return

    videos = {
        i: Video(id=i, url=url)
        for i, url in enumerate(
            [
                "/videos/age.mp4",
                "/videos/bonjour.mp4",
                "/videos/coiffeur.mp4",
                "/videos/habiter.mp4",
                "/videos/non.mp4",
                "/videos/prenom.mp4",            ],
            start=1,
        )
    }
    db.add_all(videos.values())

    words = {
        i: Word(id=i, string=s, video=videos[i])
        for i, s in enumerate(
            [
                "Âge",
                "Bonjour",
                "Coiffeur",
                "Habiter",
                "Non",
                "Prénom",
            ],
            start=1,
        )
    }
    db.add_all(words.values())

    lessons = {
        1: Lesson(id=1, title="Les bases", words=[words[3], words[5]]),
        2: Lesson(id=2, title="Les expressions utiles", words=[words[2], words[4]]),
    }
    db.add_all(lessons.values())

    users = {
        1: User(
            id=1,
            nom="Dupont",
            prenom="Alice",
            email="alice@example.com",
            password="hashed_password_1",
            premium=True,
            lessons_done=[lessons[1]],
        ),
        2: User(
            id=2,
            nom="Martin",
            prenom="Bob",
            email="bob@example.com",
            password="hashed_password_2",
            premium=False,
            lessons_done=[],
        ),
    }
    db.add_all(users.values())
    db.commit()


# ── Startup ───────────────────────────────────────────────────────────────────

@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Signy PIE API is running"}


# ── Users ─────────────────────────────────────────────────────────────────────

@app.get("/users", response_model=List[UserListItem])
async def list_users(db: Session = Depends(get_db)) -> List[UserListItem]:
    users = db.query(User).order_by(User.id).all()
    return [
        UserListItem(
            id=u.id,
            nom=u.nom,
            prenom=u.prenom,
            email=u.email,
            premium=u.premium,
            creation_date=u.creation_date,
            lessons_done=[serialize_lesson(l) for l in u.lessons_done],
        )
        for u in users
    ]


@app.get("/users/{user_id}", response_model=UserDetail)
async def get_user(user_id: int, db: Session = Depends(get_db)) -> UserDetail:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return UserDetail(
        id=user.id,
        nom=user.nom,
        prenom=user.prenom,
        email=user.email,
        premium=user.premium,
        creation_date=user.creation_date,
        lessons_done=[serialize_lesson(l) for l in user.lessons_done],
    )


# ── Lessons ───────────────────────────────────────────────────────────────────

@app.get("/lessons", response_model=List[LessonListItem])
async def list_lessons(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
) -> List[LessonListItem]:
    lessons = db.query(Lesson).order_by(Lesson.id).all()

    return [serialize_lesson(l) for l in lessons]


@app.get("/lessons/{lesson_id}", response_model=LessonDetail)
async def get_lesson(
    lesson_id: int,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
) -> LessonDetail:
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return serialize_lesson_detail(lesson)


# ── Words ─────────────────────────────────────────────────────────────────────

@app.get("/words", response_model=List[WordListItem])
async def list_words(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
) -> List[WordListItem]:
    words = db.query(Word).order_by(Word.id).all()

    return [serialize_word(w) for w in words]


@app.get("/words/{word_id}", response_model=WordDetail)
async def get_word(
    word_id: int,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
) -> WordDetail:
    word = db.query(Word).filter(Word.id == word_id).first()
    if word is None:
        raise HTTPException(status_code=404, detail="Word not found")

    return serialize_word(word)


# ── Videos ────────────────────────────────────────────────────────────────────
@app.get("/videos", response_model=List[VideoListItem])
async def list_videos(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
) -> List[VideoListItem]:
    videos = db.query(Video).order_by(Video.id).all()

    return [serialize_video(v) for v in videos]

@app.get("/video/{video_id}", response_model=VideoDetail)
@app.get("/videos/{video_id}", response_model=VideoDetail)
async def get_video(
    video_id: int,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
) -> VideoDetail:
    video = db.query(Video).filter(Video.id == video_id).first()
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")

    return serialize_video(video)


# ── AI ────────────────────────────────────────────────────────────────────────

@app.post("/ai/interrogate", response_model=AIWordResponse)
async def interrogate_ai(
    video: UploadFile = File(
        ...,
        description=(
            "Either a NumPy .npy file of MediaPipe keypoints (shape [T, F]) "
            "or a raw video blob. The .npy format is strongly preferred as it "
            "maps directly to what the model was trained on."
        ),
    ),
) -> AIWordResponse:
    """
    Predict the LSF word shown in the uploaded file.

    **Preferred input**: a `.npy` file produced by MediaPipe Holistic, with
    shape `(T, F)` where T is the number of frames and F is the feature size
    (typically 444 = 33×4 pose + 21×3×2 hands + 468×3 face — adjust to match
    your training pipeline).

    **Fallback**: a raw video blob. The model will still run but accuracy will
    be low since the bytes are not proper keypoint data.
    """
    payload = await video.read()
    try:
        prediction = predictor.predict(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return AIWordResponse(word=prediction.word, confidence=prediction.confidence)


app.mount("/videos", StaticFiles(directory="videos"), name="videos")