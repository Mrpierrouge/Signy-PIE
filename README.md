# Signy PIE

Signy PIE est une application pédagogique pour apprendre la langue des signes française. Le projet est découpé en deux parties principales : un frontend Vue 3 / Vite pour l’interface utilisateur, et un backend FastAPI pour l’API, les données et la prédiction IA sur vidéo.

## Vue d'ensemble

L’application propose :

- des pages de leçons pour progresser étape par étape,
- un lexique vidéo pour revoir les mots,
- un profil utilisateur pour suivre l’avancement,
- une route IA qui analyse une vidéo et renvoie une prédiction,
- des vidéos pédagogiques servies par le backend.

## Architecture

- Frontend: [frontend/](frontend) - application Vue 3 + Vite.
- Backend: [backend/](backend) - API FastAPI, base de données et modèle IA.
- Base de données: SQLite en local si `DATABASE_URL` n’est pas défini, PostgreSQL via Docker Compose.

Le frontend appelle le backend sur `http://localhost:8000`.

## Prérequis

- Node.js 20.19 ou plus récent.
- Python 3.12 ou plus récent.
- Optionnel: Docker et Docker Compose.

## Lancer le projet avec Docker

Cette option démarre le backend et PostgreSQL. C’est le plus simple pour obtenir l’API fonctionnelle rapidement.

```sh
docker compose up --build
```

Services exposés :

- Backend FastAPI: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

Le backend est configuré avec `DATABASE_URL=postgresql+psycopg2://signy:signy@db:5432/signy` dans [docker-compose.yml](docker-compose.yml).

## Lancer le backend en local

Depuis la racine du dépôt :

```sh
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Comportement par défaut :

- si `DATABASE_URL` est absent, le backend utilise SQLite en local,
- au démarrage, les tables sont créées et les données de démonstration sont initialisées,
- les vidéos sont servies depuis `/videos`.

## Lancer le frontend en local

Dans un autre terminal :

```sh
cd frontend
npm install
npm run dev
```

Le frontend démarre avec Vite et consomme l’API du backend sur `http://localhost:8000`.

## Commandes utiles

Frontend :

- `npm run build` pour produire une version de production,
- `npm run lint` pour vérifier le code,
- `npm run format` pour formater le code.

Backend :

- `uvicorn main:app --reload --host 0.0.0.0 --port 8000` pour le mode développement,
- `pip install -r requirements.txt` pour installer les dépendances Python.

## API backend

Principales routes exposées par FastAPI :

- `GET /`
- `GET /users`
- `GET /users/{user_id}`
- `GET /lessons`
- `GET /lessons/{lesson_id}`
- `GET /words`
- `GET /words/{word_id}`
- `GET /videos`
- `GET /videos/{video_id}`
- `POST /ai/interrogate`

La route `POST /ai/interrogate` accepte une vidéo ou un fichier de type keypoints et renvoie la prédiction du mot en LSF.

## Structure du projet

```text
Signy-PIE/
├── docker-compose.yml
├── package.json
├── backend/
└── frontend/
```

## Notes techniques

- Le backend utilise SQLAlchemy et Pydantic.
- Le modèle IA chargé par défaut est `backend/lsf_model.onnx`.
- Les labels IA peuvent être ajustés via `AI_LABELS` dans l’environnement Docker.
  - video: string (URL)
```

#### Réponse IA
```json
AIWordResponse:
  - word: string        # Mot prédit
  - confidence: float   # Score de confiance (0.0 à 1.0)
```

---

## 🔌 Routes API Backend

### Base URL
```
http://localhost:8000 (développement)
```

### Routes disponibles

#### 0. **GET `/`** - Health check
Vérifie que l'API est en ligne.

**Réponse 200:**
```json
{
  "message": "Signy PIE API is running"
}
```

---

### 👤 Users Endpoints

#### 1. **GET `/users`** - Récupérer la liste de tous les utilisateurs
Liste tous les utilisateurs enregistrés de l'application avec leurs leçons complétées.

**Réponse 200:**
```json
[
  {
    "id": 1,
    "nom": "Dupont",
    "prenom": "Alice",
    "email": "alice@example.com",
    "premium": true,
    "creation_date": "2024-01-15T10:30:00",
    "lessons_done": [
      {
        "id": 1,
        "title": "Les bases"
      }
    ]
  },
  {
    "id": 2,
    "nom": "Martin",
    "prenom": "Bob",
    "email": "bob@example.com",
    "premium": false,
    "creation_date": "2024-02-20T14:45:00",
    "lessons_done": []
  }
]
```

**Détails:**
- Retourne tous les utilisateurs triés par ID
- Ne retourne pas les mots de passe
- Inclut le statut premium, la date d'inscription et les leçons complétées
- Chaque utilisateur a une liste `lessons_done` contenant ses leçons complétées

---

#### 2. **GET `/users/{user_id}`** - Récupérer les détails d'un utilisateur
Récupère un utilisateur spécifique avec toutes ses leçons complétées.

**Paramètres:**
- `user_id` (path param): identifiant de l'utilisateur

**Réponse 200:**
```json
{
  "id": 1,
  "nom": "Dupont",
  "prenom": "Alice",
  "email": "alice@example.com",
  "premium": true,
  "creation_date": "2024-01-15T10:30:00",
  "lessons_done": [
    {
      "id": 1,
      "title": "Les bases"
    }
  ]
}
```

**Réponse 404:**
```json
{
  "detail": "User not found"
}
```

**Détails:**
- Affiche toutes les leçons que l'utilisateur a complétées
- Permet de tracker la progression pédagogique
- Utilisé pour la page profil du frontend

---

### 📚 Lessons Endpoints

#### 3. **GET `/lessons`** - Récupérer la liste des leçons
Liste toutes les leçons disponibles.

**Réponse 200:**
```json
[
  {
    "id": 1,
    "title": "Les bases"
  },
  {
    "id": 2,
    "title": "Les expressions utiles"
  }
]
```

**Détails:**
- Retourne toutes les leçons triés par ID
- Le statut (complétée ou non) est déterminé côté client en fonction de l'utilisateur

---

#### 4. **GET `/lesson/{lesson_id}`** - Récupérer les détails d'une leçon
Récupère une leçon spécifique avec tous ses mots et leurs vidéos.

**Paramètres:**
- `lesson_id` (path param): identifiant de la leçon

**Réponse 200:**
```json
{
  "id": 1,
  "title": "Les bases",
  "words": [
    {
      "id": 1,
      "string": "Bonjour",
      "video": "/videos/bonjour.mp4"
    },
    {
      "id": 2,
      "string": "Merci",
      "video": "/videos/merci.mp4"
    }
  ]
}
```

**Réponse 404:**
```json
{
  "detail": "Lesson not found"
}
```

---

### 📖 Words Endpoints

#### 5. **GET `/words`** - Récupérer le lexique complet
Liste tous les mots du vocabulaire (utilisé pour le lexique interactif).

**Réponse 200:**
```json
[
  {
    "id": 1,
    "string": "Bonjour",
    "video": "/videos/bonjour.mp4"
  },
  {
    "id": 2,
    "string": "Merci",
    "video": "/videos/merci.mp4"
  }
]
```

**Détails:**
- Tous les mots du vocabulaire pédagogique
- Retourne les mots triés par ID
- Utilisé dans la page lexique du frontend

---

#### 6. **GET `/word/{word_id}`** - Récupérer un mot spécifique
Récupère un mot unique avec sa vidéo de démonstration.

**Paramètres:**
- `word_id` (path param): identifiant du mot

**Réponse 200:**
```json
{
  "id": 1,
  "string": "Bonjour",
  "video": "/videos/bonjour.mp4"
}
```

**Réponse 404:**
```json
{
  "detail": "Word not found"
}
```

---

### 🤖 AI Endpoint

#### 7. **POST `/ai/interrogate`** - Analyser une vidéo pour prédire un mot
Envoie une vidéo enregistrée pour obtenir une prédiction de mot LSF via le modèle ONNX.

**Content-Type:** `multipart/form-data`

**Paramètres:**
- `video` (form file): fichier vidéo MP4/WebM à analyser

**Réponse 200:**
```json
{
  "word": "Bonjour",
  "confidence": 0.95
}
```

**Réponse 400:**
```json
{
  "detail": "Erreur lors du traitement vidéo (ex: format invalide)"
}
```

**Détails:**
- Accepte les fichiers vidéo (UploadFile)
- Modèle: `backend/lsf_model.onnx`
- Confidence: score entre 0.0 et 1.0
- Utilise `VideoWordPredictor` de `ai_service.py`
- Variables d'environnement:
  - `AI_LABELS` : labels personnalisés (optionnel)

---

### CORS & Headers

CORS activé avec :
- `allow_origins: ["*"]`
- `allow_credentials: true`
- `allow_methods: ["*"]`
- `allow_headers: ["*"]`

---

## 🛣️ Routes Frontend

### Routes Vue Router

| Route | Vue File | Description |
|-------|----------|-------------|
| `/` | - | Redirection vers `/home` |
| `/home` | `views/home.vue` | **Liste des leçons** avec statuts (locked/unlocked/completed) |
| `/lexique` | `views/lexique.vue` | **Lexique vidéo interactif** - tous les mots avec démonstrations |
| `/profile` | `views/profile.vue` | **Profil utilisateur** - suivi de progression |

### Architecture du composant racine

```
App.vue (Layout principal)
├── Logo (en haut)
├── RouterView (contenu dynamique selon la route)
│   ├── home.vue (affiche les leçons)
│   ├── lexique.vue (affiche les mots)
│   └── profile.vue (affiche le profil)
└── Menu.vue (barre de navigation fixe en bas)
    ├── Lien vers /home
    ├── Lien vers /lexique
    └── Lien vers /profile
```

### Composants réutilisables

- **LessonCard** (`components/cards/lessonCard.vue`)
  - Affiche une leçon avec titre et statut
  - Événement `@click` pour sélectionner

- **VideoCard** (`components/cards/videoCard.vue`)
  - Affiche un mot avec sa vidéo
  - Contrôles de lecture

- **VideoBlock** (`components/videoBlock.vue`)
  - Lecteur vidéo réutilisable
  - Intégré dans lexique et leçons

---

## ✨ Fonctionnalités

### 🎓 Pédagogie

- **Leçons structurées** : progression guidée avec déverrouillage progressif
- **Vocabulaire illustré** : chaque mot LSF accompagné d'une vidéo de démonstration
- **Statuts d'apprentissage** : trois états pour chaque ressource
  - 🔒 `locked` : à débloquer après prérequis
  - 🔓 `unlocked` : accessible, non complété
  - ✅ `completed` : maîtrisé

### 🤖 Intelligence Artificielle

- **Analyse vidéo en temps réel** : prédiction de mots LSF à partir d'une vidéo utilisateur
- **Modèle ONNX** : inférence rapide (`lsf_model.onnx`)
- **Scores de confiance** : retour utilisateur sur la qualité de la prédiction

### 🎨 Interface utilisateur

- **Responsive** : adaptée aux appareils mobiles et tablettes
- **Navigation intuitive** : menu fixe en bas pour accès constant
- **Composants réutilisables** : architecture Vue modulaire et maintenable
- **Design cohérent** : système de variables CSS partagées

### 🔄 Intégration Frontend-Backend

- **Appels HTTP** : communication RESTful via fetch/axios
- **Gestion d'état** : réactivité Vue 3 avec `ref()` et `reactive()`
- **Typage complet** : TypeScript pour réduire les bugs

---

## 🛠️ Stack technique

### Frontend
- **Vue 3** : framework réactif moderne
- **Vue Router** : routage côté client
- **TypeScript** : typage statique pour JS
- **Vite** : build tool ultra-rapide
- **CSS personnalisé** : variables et grille flexbox

### Backend
- **FastAPI** : framework web Python haute-performance
- **SQLAlchemy** : ORM pour intéraction BD
- **Pydantic** : validation de données avec schémas
- **ONNX Runtime** : inférence de modèles ML
- **FastAPI CORS** : gestion cross-origin

### Données
- **PostgreSQL** : base de données production (Docker Compose)
- **SQLite** : fallback développement local
- **SQLAlchemy ORM** : abstraction BD agnostique

### DevOps
- **Docker** : containerisation des services
- **Docker Compose** : orchestration multi-conteneur
- **Node.js 20+** : runtime JavaScript
- **ESLint + Prettier** : qualité de code

---

## 📦 Installation & Démarrage

### Prérequis

- **Node.js** 20+ et npm
- **Python** 3.9+ (pour backend local)
- **Docker & Docker Compose** (optionnel, pour démarrage complet)
- **Git**

### Installation locale

#### 1️⃣ Cloner & installer les dépendances

```bash
# Cloner le repo
git clone <repository-url>
cd Signy-PIE

# Installer les dépendances du monorepo
npm install
```

#### 2️⃣ Lancer le backend (local)

```bash
cd backend

# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate

# Installer les dépendances Python
pip install -r requirements.txt

# Démarrer le serveur FastAPI
python main.py
# Disponible sur http://localhost:8000
```

#### 3️⃣ Lancer le frontend (dans un autre terminal)

```bash
cd frontend
npm install
npm run dev
# Disponible sur http://localhost:5173
```

---

### Démarrage complet avec Docker Compose

```bash
# À la racine du projet
docker compose up --build

# Services démarrés:
# - Backend FastAPI: http://localhost:8000
# - PostgreSQL: localhost:5432
# - Documentation Swagger: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

Pour arrêter:
```bash
docker compose down
```

---

### Vérification du code

```bash
# À la racine
npm run lint      # Vérifier les erreurs de style
npm run format    # Formater le code

# Ou dans frontend/ ou backend/
cd frontend
npm run lint
npm run format
```

---

### Build de production

#### Frontend

```bash
cd frontend
npm run build     # Crée dist/ optimisé
npm run preview   # Prévisualiser la build
```

#### Backend

Le backend est buildé automatiquement par Docker Compose.

---

## 🔄 Flux de données

### Exemple 1: Frontend récupère le profil utilisateur

```
1. Utilisateur accède à la page /profile
   ↓
2. profile.vue récupère l'ID utilisateur (stocké en session/localStorage)
   ↓
3. Frontend effectue: GET /users/{user_id}
   ↓
4. Backend query la BD pour l'utilisateur
   ↓
5. Backend charge les leçons complétées via la relation user_lessons_done
   ↓
6. Backend retourne UserDetail (infos user + lessons_done[])
   ↓
7. Frontend affiche le profil (nom, email, premium, leçons complétées)
```

### Exemple 2: Utilisateur consulte une leçon

```
1. Utilisateur clique sur une leçon dans /home
   ↓
2. home.vue reçoit l'événement @click
   ↓
3. Frontend effectue: GET /lesson/{id}
   ↓
4. Backend query la BD pour trouver la leçon
   ↓
5. Backend retourne LessonDetail (leçon + mots + vidéos)
   ↓
6. Frontend affiche les mots avec composant VideoCard
   ↓
7. Frontend marque la leçon comme "completed" en vérifiant les lessons_done de l'utilisateur
   ↓
8. Utilisateur clique sur une vidéo
   ↓
9. VideoBlock.vue démarre la lecture vidéo
```

### Exemple 3: Utilisateur teste son LSF avec l'IA

```
1. Utilisateur enregistre une vidéo sur /lexique
   ↓
2. lexique.vue capture le blob vidéo
   ↓
3. Frontend effectue: POST /ai/interrogate (video file)
   ↓
4. Backend reçoit la vidéo dans ai_service.VideoWordPredictor
   ↓
5. Modèle ONNX analyse la vidéo
   ↓
6. Backend retourne AIWordResponse (word + confidence)
   ↓
7. Frontend affiche le résultat "Prédit: Bonjour (95%)"
```

### Synchronisation User-Lessons

```
Architecture de suivi:
User.lessons_done ←→ [many-to-many] ←→ Lesson

Quand un utilisateur complète une leçon:
1. Frontend envoie confirmation (ex: POST /users/{id}/complete-lesson/{lesson_id})
2. Backend ajoute la Lesson aux lessons_done de l'User
3. Relation persist en base via table user_lessons_done
4. Prochains appels GET /users/{id} retournent la leçon dans lessons_done[]
```

---

## 📝 Données d'exemple (seed)

À chaque démarrage, la BD est pré-remplie avec :

**Videos:**
- `/videos/bonjour.mp4` → "Bonjour"
- `/videos/merci.mp4` → "Merci"
- `/videos/au_revoir.mp4` → "Au revoir"
- `/videos/oui.mp4` → "Oui"

**Words:**
- "Bonjour" (leçon "Les bases")
- "Merci" (leçon "Les bases")
- "Au revoir" (leçon "Les expressions utiles")
- "Oui" (leçon "Les expressions utiles")

**Lessons:**
1. "Les bases" (2 mots: Bonjour, Merci)
2. "Les expressions utiles" (2 mots: Au revoir, Oui)

**Users (exemples pour test):**
1. **Alice Dupont** 
   - Email: `alice@example.com`
   - Premium: `true`
   - Leçons complétées: "Les bases"
   
2. **Bob Martin**
   - Email: `bob@example.com`
   - Premium: `false`
   - Leçons complétées: aucune

---

## 🚀 Commandes utiles

```bash
# Frontend
cd frontend
npm run dev       # Démarrage développement
npm run build     # Build production
npm run preview   # Prévisualiser build
npm run lint      # ESLint
npm run format    # Prettier

# Backend (dans virtualenv)
python main.py              # Démarrer serveur
python -m pytest            # Lancer tests (si disponible)

# Docker Compose
docker compose up --build   # Démarrer tous les services
docker compose down         # Arrêter tous les services
docker compose logs -f      # Voir les logs en temps réel

# Monorepo
npm install                 # Installer dépendances tous les workspaces
```

---

## 📚 Documentation supplémentaire

- **FastAPI Swagger UI** : http://localhost:8000/docs
- **FastAPI ReDoc** : http://localhost:8000/redoc
- **Vue 3 Guide** : https://vuejs.org
- **Vite** : https://vitejs.dev

---

## 👨‍💻 Architecture résumée

```
Utilisateur → Frontend (Vue 3) → API HTTP → Backend (FastAPI) → BD (PostgreSQL)
              ↓                                    ↓
            Types TS                         ORM SQLAlchemy
            Composants                       Schémas Pydantic
            Router                           Services IA (ONNX)
```

Chaque couche est indépendante, scalable et testable ! 🎉
