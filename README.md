# Signy PIE

Signy PIE est une application pédagogique pour apprendre la langue des signes française (LSF). Le projet est découpé en deux parties principales : un frontend Vue 3 / Vite pour l'interface utilisateur, et un backend FastAPI pour l'API, les données et la prédiction IA sur vidéo.

## Vue d'ensemble

L'application propose :

- des leçons interactives pour progresser étape par étape,
- une vidéo de démonstration LSF pour chaque mot,
- un enregistrement vidéo in-app pour s'exercer,
- une route IA qui analyse les keypoints MediaPipe et renvoie une prédiction,
- une validation automatique avec feedback (Bravo / Réessayez).

## Architecture

- **Frontend** : [frontend/](frontend) — Vue 3 + Vite + TypeScript.
- **Backend** : [backend/](backend) — FastAPI, SQLAlchemy, modèle ONNX.
- **Base de données** : SQLite en local si `DATABASE_URL` absent, PostgreSQL via Docker Compose.
- **pgAdmin** : interface graphique PostgreSQL accessible sur `http://localhost:5050`.

Le frontend appelle le backend sur `http://localhost:8000`.

## Prérequis

- Node.js 20+ et npm.
- Python 3.12+.
- Docker et Docker Compose (recommandé).

---

## Lancer le projet avec Docker (recommandé)

```sh
docker compose up --build
```

Services exposés :

| Service | URL |
|---------|-----|
| Backend FastAPI | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |
| pgAdmin | http://localhost:5050 |

### Connexion pgAdmin

Ouvre http://localhost:5050 puis connecte-toi avec :

- **Email** : `admin@signy.com`
- **Password** : `admin`

Enregistre le serveur PostgreSQL (**Register → Server**) avec :

| Champ | Valeur |
|-------|--------|
| Host | `db` *(nom du service Docker, pas `localhost`)* |
| Port | `5432` |
| Database | `signy` |
| Username | `signy` |
| Password | `signy` |

---

## Lancer le backend en local (sans Docker)

```sh
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows : .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Sans `DATABASE_URL`, le backend utilise SQLite (`backend/signy.db`). Les tables et données de seed sont créées automatiquement au démarrage.

## Lancer le frontend en local

```sh
cd frontend
npm install
npm run dev
# Disponible sur http://localhost:5173
```

---

## Commandes utiles

```bash
# Frontend
cd frontend
npm run dev       # Dev avec hot-reload
npm run build     # Build de production (dist/)
npm run lint      # ESLint
npm run format    # Prettier

# Backend (dans le venv)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Docker
docker compose up --build   # Démarrer tous les services
docker compose down         # Arrêter
docker compose logs -f      # Logs en temps réel

# Inspecter PostgreSQL directement
docker compose exec db psql -U signy -d signy
```

---

## API backend

Base URL : `http://localhost:8000`

### Endpoints disponibles

#### Health

| Méthode | Route | Description |
|---------|-------|-------------|
| `GET` | `/` | Vérification que l'API tourne |

#### Users

| Méthode | Route | Description |
|---------|-------|-------------|
| `GET` | `/users` | Liste tous les utilisateurs |
| `GET` | `/users/{user_id}` | Détail d'un utilisateur (avec `lessons_done`) |

#### Lessons

| Méthode | Route | Description |
|---------|-------|-------------|
| `GET` | `/lessons` | Liste toutes les leçons |
| `GET` | `/lessons/{lesson_id}` | Détail d'une leçon (avec mots et vidéos) |

#### Words

| Méthode | Route | Description |
|---------|-------|-------------|
| `GET` | `/words` | Liste tous les mots |
| `GET` | `/words/{word_id}` | Détail d'un mot |

#### Videos

| Méthode | Route | Description |
|---------|-------|-------------|
| `GET` | `/videos` | Liste toutes les vidéos |
| `GET` | `/videos/{video_id}` | Détail d'une vidéo |

#### Word Correspondance

| Méthode | Route | Description |
|---------|-------|-------------|
| `GET` | `/word-corespondance` | Liste toutes les correspondances signe → mots |
| `GET` | `/word-corespondance/{id}` | Détail d'une correspondance |
| `GET` | `/word-corespondance/by-label/{label}` | Recherche par label du modèle |

#### IA

| Méthode | Route | Description |
|---------|-------|-------------|
| `POST` | `/ai/interrogate` | Analyse un fichier `.npy` (keypoints MediaPipe) et valide le signe |

**Paramètres `POST /ai/interrogate` :**

| Paramètre | Type | Description |
|-----------|------|-------------|
| `video` | `file` | Fichier `.npy` MediaPipe Holistic (shape `[T, 444]`) ou blob vidéo |
| `expected_word` | `string` (form/query) | Mot attendu (texte) |
| `expected_word_id` | `int` (form/query) | ID du mot attendu |

**Réponse 200 :**
```json
{
  "word": "age",
  "confidence": 0.97,
  "label": "age",
  "matched_word_ids": [1],
  "matched_words": ["Âge"],
  "is_valid": true,
  "tested_word": "Âge",
  "message": "Bravo ! Le signe pour 'Âge' a été reconnu avec succès !"
}
```

---

## Modèle IA

- **Fichier** : `backend/lsf_model.onnx`
- **Métadonnées** : `backend/model_meta.json`
- **Input** : keypoints MediaPipe Holistic, shape `[T, 444]`, rééchantillonnés à 60 frames
- **Output** : logits sur 6 classes → softmax → label prédit

**Classes du modèle** (ordre important, aligné avec les IDs en base) :

| Index | Label modèle | Mot(s) | ID Word |
|-------|-------------|--------|---------|
| 0 | `age` | Âge | 1 |
| 1 | `bonjour` | Bonjour, Merci | 2, 7 |
| 2 | `coiffeur` | Coiffeur | 3 |
| 3 | `habiter` | Habiter | 4 |
| 4 | `non` | Non | 5 |
| 5 | `prenom` | Prénom | 6 |

La table `word_corespondance` fait le lien entre les labels prédits par le modèle et les mots de la base. Bonjour et Merci partagent le même signe (label `bonjour/merci`).

---

## Données de seed

Au démarrage, si la base est vide ou désalignée, elle est automatiquement peuplée avec :

**Vidéos :**

| ID | Fichier |
|----|---------|
| 1 | `/videos/age.mp4` |
| 2 | `/videos/bonjour.mp4` |
| 3 | `/videos/coiffeur.mp4` |
| 4 | `/videos/habiter.mp4` |
| 5 | `/videos/non.mp4` |
| 6 | `/videos/prenom.mp4` |

**Mots :**

| ID | Mot | Vidéo ID |
|----|-----|----------|
| 1 | Âge | 1 |
| 2 | Bonjour | 2 |
| 3 | Coiffeur | 3 |
| 4 | Habiter | 4 |
| 5 | Non | 5 |
| 6 | Prénom | 6 |
| 7 | Merci | 2 *(même signe que Bonjour)* |

**Leçons :**

| ID | Titre | Mots |
|----|-------|------|
| 1 | Les salutations | Bonjour, Merci |
| 2 | Les bases | Habiter, Non |
| 3 | Les expressions utiles | Âge, Prénom |

**Word Correspondance :**

| ID | Label | Words (IDs) |
|----|-------|-------------|
| 1 | `age` | [1] |
| 2 | `bonjour/merci` | [2, 7] |
| 3 | `coiffeur` | [3] |
| 4 | `habiter` | [4] |
| 5 | `non` | [5] |
| 6 | `prenom` | [6] |

**Utilisateurs de test :**

| Nom | Email | Premium | Leçons complétées |
|-----|-------|---------|-------------------|
| Alice Dupont | `alice@example.com` | ✅ | Les salutations |
| Bob Martin | `bob@example.com` | ❌ | aucune |

---

## Structure du projet

```text
Signy-PIE/
├── docker-compose.yml          # PostgreSQL + Backend + pgAdmin
├── package.json                # Monorepo root
├── backend/
│   ├── main.py                 # Application FastAPI, routes, seed
│   ├── models.py               # Modèles SQLAlchemy
│   ├── schemas.py              # Schémas Pydantic
│   ├── database.py             # Connexion DB (SQLite / PostgreSQL)
│   ├── ai_service.py           # Chargement ONNX et prédiction
│   ├── lsf_model.onnx          # Modèle entraîné
│   ├── model_meta.json         # Métadonnées du modèle (classes, dims)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── videos/                 # Vidéos de démonstration LSF
└── frontend/
    ├── src/
    │   ├── views/              # Pages : home, lexique, profile
    │   ├── components/         # Composants réutilisables
    │   ├── api/api.ts          # Client HTTP vers le backend
    │   ├── types/              # Types TypeScript
    │   └── router/             # Vue Router
    ├── vite.config.ts
    └── package.json
```

---

## Stack technique

| Couche | Technologie |
|--------|------------|
| Frontend | Vue 3, Vite, TypeScript |
| Backend | FastAPI, SQLAlchemy, Pydantic |
| IA | ONNX Runtime, MediaPipe Holistic |
| Base de données | PostgreSQL (prod) / SQLite (dev) |
| DevOps | Docker, Docker Compose |
| Admin DB | pgAdmin 4 |

---

## Documentation interactive

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc
- **Vue 3 Guide** : https://vuejs.org
- **Vite** : https://vitejs.dev
