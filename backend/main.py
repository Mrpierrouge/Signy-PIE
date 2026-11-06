import unicodedata
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from ai_service import VideoWordPredictor
from database import Base, SessionLocal, engine
from models import (
    Lesson,
    User,
    Video,
    Word,
    WordCorespondance,
    lesson_words,
    user_lessons_done,
    word_corespondance_words,
)
from schemas import (
    AIWordResponse,
    LessonDetail,
    LessonListItem,
    UserDetail,
    UserListItem,
    VideoDetail,
    VideoListItem,
    WordCorespondanceDetail,
    WordCorespondanceListItem,
    WordDetail,
    WordListItem,
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


def serialize_corespondance(item: WordCorespondance, db: Session) -> WordCorespondanceDetail:
    matched = item.get_words(db)
    return WordCorespondanceDetail(
        id=item.id,
        label=item.label,
        words=item.words,
        matched_words=[serialize_word(w) for w in matched],
    )


def normalize_label(text: str) -> str:
    """Normalize string for robust comparison: lowercase, strip, remove accents."""
    if not text:
        return ""
    text = unicodedata.normalize("NFD", text.lower().strip())
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def find_corespondance_by_label(db: Session, label: str) -> Optional[WordCorespondance]:
    if not label:
        return None
    norm = normalize_label(label)

    all_items = db.query(WordCorespondance).all()

    # 1. Exact match on label
    for item in all_items:
        if normalize_label(item.label) == norm:
            return item

    # 2. Check if normalized label matches any sub-label separated by '/' or '_'
    for item in all_items:
        parts = [normalize_label(p) for p in item.label.replace("_", "/").split("/")]
        if norm in parts:
            return item

    # 3. Check if label matches any word string in db associated with this item
    for item in all_items:
        words = item.get_words(db)
        for w in words:
            if normalize_label(w.string) == norm:
                return item

    return None


# ── DB dependency ─────────────────────────────────────────────────────────────

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── Seed data ─────────────────────────────────────────────────────────────────

def seed_database(db: Session, force: bool = False) -> None:
    age_corresp = db.query(WordCorespondance).filter(WordCorespondance.label == "age").first()
    bj_corresp = db.query(WordCorespondance).filter(WordCorespondance.label == "bonjour-merci").first()
    if bj_corresp is None:
        bj_corresp = (
            db.query(WordCorespondance)
            .filter(WordCorespondance.label == "bonjour/merci")
            .first()
        )
        if bj_corresp is not None:
            bj_corresp.label = "bonjour-merci"
            db.commit()
    word_1 = db.query(Word).filter(Word.id == 1).first()
    has_all_corresp = db.query(WordCorespondance).count() >= 6
    is_aligned = (
        age_corresp is not None
        and 1 in (age_corresp.words or [])
        and bj_corresp is not None
        and word_1 is not None
        and normalize_label(word_1.string) == "age"
        and has_all_corresp
    )

    if not force and is_aligned:
        return

    # Clear previous seed data to ensure key alignment across all tables
    db.query(user_lessons_done).delete()
    db.query(lesson_words).delete()
    db.query(word_corespondance_words).delete()
    db.query(WordCorespondance).delete()
    db.query(Lesson).delete()
    db.query(Word).delete()
    db.query(Video).delete()
    db.query(User).delete()
    db.commit()

    # 1. Videos (aligned with model_meta.json classes 0..5)
    videos = {
        1: Video(id=1, url="/videos/age.mp4"),
        2: Video(id=2, url="/videos/bonjour.mp4"),
        3: Video(id=3, url="/videos/coiffeur.mp4"),
        4: Video(id=4, url="/videos/habiter.mp4"),
        5: Video(id=5, url="/videos/non.mp4"),
        6: Video(id=6, url="/videos/prenom.mp4"),
    }
    db.add_all(videos.values())

    # 2. Words (IDs 1..6 match video IDs 1..6 and model classes; ID 7 is Merci sharing Video 2 with Bonjour)
    words = {
        1: Word(id=1, string="Âge", video=videos[1]),
        2: Word(id=2, string="Bonjour", video=videos[2]),
        3: Word(id=3, string="Coiffeur", video=videos[3]),
        4: Word(id=4, string="Habiter", video=videos[4]),
        5: Word(id=5, string="Non", video=videos[5]),
        6: Word(id=6, string="Prénom", video=videos[6]),
        7: Word(id=7, string="Merci", video=videos[2]),
    }
    db.add_all(words.values())

    # 3. Word Correspondance table (word_corespondance)
    # IDs 1..6 match Videos 1..6, Words 1..6, and model classes; Bonjour maps to words [2, 7]
    corespondances = [
        WordCorespondance(id=1, label="age", words=[1], word_items=[words[1]]),
        WordCorespondance(id=2, label="bonjour-merci", words=[2, 7], word_items=[words[2], words[7]]),
        WordCorespondance(id=3, label="coiffeur", words=[3], word_items=[words[3]]),
        WordCorespondance(id=4, label="habiter", words=[4], word_items=[words[4]]),
        WordCorespondance(id=5, label="non", words=[5], word_items=[words[5]]),
        WordCorespondance(id=6, label="prenom", words=[6], word_items=[words[6]]),
    ]
    db.add_all(corespondances)

    # 4. Lessons
    lessons = {
        1: Lesson(id=1, title="Les salutations", words=[words[2], words[7]]),
        2: Lesson(id=2, title="Les bases", words=[words[4], words[5]]),
        3: Lesson(id=3, title="Les expressions utiles", words=[words[1], words[6]]),
    }
    db.add_all(lessons.values())

    # 5. Users
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
@app.get("/videos/{video_id:int}", response_model=VideoDetail)
async def get_video(
    video_id: int,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
) -> VideoDetail:
    video = db.query(Video).filter(Video.id == video_id).first()
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")

    return serialize_video(video)


# ── Word Correspondance ───────────────────────────────────────────────────────

@app.get("/word-corespondance", response_model=List[WordCorespondanceDetail])
@app.get("/word-correspondances", response_model=List[WordCorespondanceDetail])
async def list_word_corespondances(db: Session = Depends(get_db)) -> List[WordCorespondanceDetail]:
    """List all sign-to-words correspondances."""
    items = db.query(WordCorespondance).order_by(WordCorespondance.id).all()
    return [serialize_corespondance(item, db) for item in items]


@app.get("/word-corespondance/{corespondance_id}", response_model=WordCorespondanceDetail)
@app.get("/word-correspondances/{corespondance_id}", response_model=WordCorespondanceDetail)
async def get_word_corespondance(
    corespondance_id: int,
    db: Session = Depends(get_db),
) -> WordCorespondanceDetail:
    """Get a single sign correspondance by ID."""
    item = db.query(WordCorespondance).filter(WordCorespondance.id == corespondance_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Word correspondance not found")
    return serialize_corespondance(item, db)


@app.get("/word-corespondance/by-label/{label}", response_model=WordCorespondanceDetail)
@app.get("/word-correspondances/by-label/{label}", response_model=WordCorespondanceDetail)
async def get_word_corespondance_by_label(
    label: str,
    db: Session = Depends(get_db),
) -> WordCorespondanceDetail:
    """Find a sign correspondance by its model label or alias."""
    item = find_corespondance_by_label(db, label)
    if item is None:
        raise HTTPException(status_code=404, detail=f"No correspondance found for label '{label}'")
    return serialize_corespondance(item, db)


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
    expected_word: str = Form(...),
    db: Session = Depends(get_db),
) -> AIWordResponse:
    """
    Predict the LSF sign from the uploaded file and verify against the tested lesson word.

    Flow:
      1. Resolve the requested lesson word to its canonical model label.
      2. Predict a sign label from the uploaded keypoints.
      3. Lookup the predicted label in 'word_corespondance'.
      4. Verify whether the prediction matches the requested word's canonical label.
    """
    expected_word = expected_word.strip()
    expected_corresp = find_corespondance_by_label(db, expected_word)
    if expected_corresp is None:
        raise HTTPException(
            status_code=404,
            detail=f"No correspondance found for expected word '{expected_word}'",
        )

    payload = await video.read()
    try:
        prediction = predictor.predict(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    # 3. Lookup in word_corespondance by predicted label
    corresp = find_corespondance_by_label(db, prediction.word)

    label = corresp.label if corresp else prediction.word
    matched_word_ids = list(corresp.words) if (corresp and corresp.words) else []

    # 4. Retrieve matched words from words table
    matched_words_db = (
        corresp.get_words(db)
        if corresp
        else (db.query(Word).filter(Word.id.in_(matched_word_ids)).all() if matched_word_ids else [])
    )
    # Direct fallback if corresp was None or returned no words: query Word table
    if not matched_words_db:
        norm_pred = normalize_label(prediction.word)
        direct_matches = [w for w in db.query(Word).all() if normalize_label(w.string) == norm_pred]
        if direct_matches:
            matched_words_db = direct_matches
            matched_word_ids = [w.id for w in direct_matches]

    matched_strings = [w.string for w in matched_words_db] if matched_words_db else [prediction.word]

    tested_label = expected_word

    # 5. Verify the prediction against the requested word's canonical label.
    expected_true_label = normalize_label(expected_corresp.label)
    norm_matched = [normalize_label(s) for s in matched_strings]
    norm_label_parts = [normalize_label(p) for p in label.replace("_", "/").split("/")]
    norm_pred = normalize_label(prediction.word)
    norm_target = normalize_label(tested_label)
    is_valid = (
        expected_true_label == normalize_label(label)
        or norm_target in norm_matched
        or norm_target in norm_label_parts
        or norm_target == norm_pred
    )

    # 6. Formulate human-readable feedback message
    if is_valid:
        if len(matched_strings) > 1:
            message = (
                f"Bravo ! Le signe correspond bien à '{tested_label}'. "
                f"Ce signe en LSF correspond à : {', '.join(matched_strings)}."
            )
        else:
            message = f"Bravo ! Le signe pour '{tested_label}' a été reconnu avec succès !"
    else:
        message = (
            f"Le signe reconnu est '{label}' ({', '.join(matched_strings)}), "
            f"mais le mot testé dans cette leçon est '{tested_label}'. Réessayez !"
        )

    return AIWordResponse(
        word=label,
        confidence=prediction.confidence,
        label=label,
        true_label=label,
        matched_word_ids=matched_word_ids,
        matched_words=matched_strings,
        is_valid=is_valid,
        tested_word=tested_label,
        message=message,
    )


app.mount(
    "/videos",
    StaticFiles(directory=str(Path(__file__).resolve().parent / "videos")),
    name="videos",
)