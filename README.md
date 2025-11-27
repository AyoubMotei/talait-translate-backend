# TalAIt Secure Translate API - Backend

> API sécurisée de traduction FR ↔ EN avec authentification JWT et intégration Hugging Face

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

---

##  Table des Matières

- [À Propos](#-à-propos)
- [Architecture](#-architecture)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Lancement](#-lancement)
- [Endpoints API](#-endpoints-api)
- [Tests](#-tests)
- [Docker](#-docker)


---

##  À Propos

### Contexte

TalAIt, start-up marocaine spécialisée dans l'e-commerce, prépare son expansion aux États-Unis. Ce projet fournit une API sécurisée permettant :

- **Traduction FR → EN** pour les fiches produits (équipe marketing)
- **Traduction EN → FR** pour les tickets clients (service client)
- **Authentification JWT** pour sécuriser l'accès
- **Intégration Hugging Face** pour la traduction IA

### Technologies

- **Backend** : FastAPI (Python 3.11)
- **Base de données** : PostgreSQL 15
- **Authentification** : JWT (JSON Web Tokens)
- **Hashage** : Argon2 (mots de passe sécurisés)
- **IA** : Hugging Face Inference API
- **Conteneurisation** : Docker + Docker Compose

---

##  Architecture

### Architecture 3-Tiers

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
│   Frontend  │ ───> │   Backend    │ ───> │  Hugging Face   │
│  (Next.js)  │      │  (FastAPI)   │      │      API        │
└─────────────┘      └──────┬───────┘      └─────────────────┘
                            │
                     ┌──────▼───────┐
                     │  PostgreSQL  │
                     │   Database   │
                     └──────────────┘
```

### Structure du Projet

```
talait-translate-backend/
│
├── app/                          # Code source principal
│   ├── __init__.py              # Package marker
│   ├── main.py                  # Point d'entrée FastAPI
│   ├── database.py              # Configuration PostgreSQL
│   ├── models.py                # Modèles SQLAlchemy
│   ├── schemas.py               # Schémas Pydantic
│   ├── auth.py                  # Logique JWT
│   └── services/
│       ├── __init__.py
│       └── huggingface.py       # Service de traduction
│
├── tests/                        # Tests unitaires
│   ├── __init__.py
│   └── test_api.py
│
├── .env                          # Variables d'environnement (secret)
├── .gitignore                    # Fichiers ignorés par Git
├── requirements.txt              # Dépendances Python
├── Dockerfile                    # Image Docker backend
├── docker-compose.yml            # Orchestration services
└── README.md                     # Cette documentation
```

---

## Prérequis

### Logiciels Requis

- **Python** 3.11+
- **PostgreSQL** 15+
- **Docker** et **Docker Compose** (optionnel mais recommandé)
- **Git**

### Compte Hugging Face

1. Créer un compte sur [huggingface.co](https://huggingface.co/)
2. Générer un token d'accès : [Settings > Tokens](https://huggingface.co/settings/tokens)
3. Sélectionner "Read" permissions

---

##  Installation

### Méthode 1 : Installation Locale (Sans Docker)

```bash
# 1. Cloner le dépôt
git clone https://github.com/AyoubMotei/talait-translate-backend.git
cd talait-translate-backend

# 2. Créer un environnement virtuel
python -m venv venv

# 3. Activer l'environnement virtuel
# Windows :
venv\Scripts\activate
# Mac/Linux :
source venv/bin/activate

# 4. Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# 5. Configurer PostgreSQL
# Créer la base de données
psql -U postgres -c "CREATE DATABASE talait_translate_db;"

# 6. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos vraies valeurs
```

### Méthode 2 : Installation avec Docker (Recommandé)

```bash
# 1. Cloner le dépôt
git clone https://github.com/AyoubMotei/talait-translate-backend.git
cd talait-translate-backend

# 2. Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos vraies valeurs

# 3. Lancer avec Docker Compose
docker-compose up -d

# 4. Vérifier que tout fonctionne
docker-compose ps
docker-compose logs -f backend
```

---

##  Configuration

### Fichier `.env`

Créez un fichier `.env` à la racine du projet :

```bash
# BASE DE DONNÉES POSTGRESQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=votre_mot_de_passe_securise
POSTGRES_HOST=localhost  # "postgres" si vous utilisez Docker
POSTGRES_PORT=5432
POSTGRES_DB=talait_translate_db

# SÉCURITÉ JWT
SECRET_KEY=votre_cle_secrete_super_longue_et_aleatoire
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# HUGGING FACE API
HUGGING_FACE_API_KEY=hf_votre_token_ici
```

### Générer une Clé Secrète Sécurisée

```bash
# Avec Python
python -c "import secrets; print(secrets.token_hex(32))"

# Avec OpenSSL
openssl rand -hex 32
```

---

## Lancement

### Démarrage Local

```bash
# Activer l'environnement virtuel
source venv/bin/activate  # Mac/Linux
# OU
venv\Scripts\activate  # Windows

# Lancer l'API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera accessible sur : **http://localhost:8000**

Documentation interactive : **http://localhost:8000/docs**

### Démarrage avec Docker

```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f backend

# Arrêter les services
docker-compose down
```

---

## Endpoints API

### Documentation Interactive

Une fois l'API lancée, accédez à :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

### Endpoints Disponibles

| Méthode | Endpoint | Description | Authentification |
|---------|----------|-------------|------------------|
| GET | `/health` | Vérification de santé | ❌ Non |
| POST | `/register` | Inscription | ❌ Non |
| POST | `/login` | Connexion (obtenir JWT) | ❌ Non |
| POST | `/translate` | Traduction | ✅ JWT requis |
| GET | `/test_env` | Info utilisateur |  ❌ Non  |

---

### 1️⃣ Health Check

```bash
GET http://localhost:8000/health
```

**Réponse :**
```json
{
  "status": "ok",
  "message": "API opérationnelle"
}
```

---

### 2️⃣ Inscription

```bash
POST http://localhost:8000/register
Content-Type: application/json

{
  "username": "jean",
  "password": "motdepasse123"
}
```

**Réponse (200) :**
```json
{
  "id": 1,
  "username": "jean",
  "created_at": "2025-11-24T10:30:00"
}
```

**Erreur (400) :**
```json
{
  "detail": "Nom d'utilisateur déjà pris"
}
```

---

### 3️⃣ Connexion

```bash
POST http://localhost:8000/login
Content-Type: application/json

{
  "username": "jean",
  "password": "motdepasse123"
}
```

**Réponse (200) :**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Erreur (401) :**
```json
{
  "detail": "Identifiants incorrects"
}
```

---

### 4️⃣ Traduction (Protégé)

```bash
POST http://localhost:8000/translate
Authorization: Bearer VOTRE_TOKEN_JWT
Content-Type: application/json

{
  "text": "Bonjour le monde",
  "source_language": "fr",
  "target_language": "en"
}
```

**Réponse (200) :**
```json
{
  "translated_text": "Hello world"
}
```

**Erreur (401) :**
```json
{
  "detail": "Impossible de valider les identifiants"
}
```

**Erreur (503) :**
```json
{
  "detail": "Service de traduction indisponible"
}
```

---

##  Tests

### Installation des Dépendances de Test

```bash
pip install pytest 
```

### Lancer les Tests

```bash
# Tous les tests
pytest tests/test_api.py -v
```

### Tests Couverts

- ✅ Health check
- ✅ Inscription (succès, doublon, validation)
- ✅ Connexion (succès, mauvais mot de passe, utilisateur inexistant)
- ✅ Traduction (protection JWT, validation)
---

##  Docker

### Commandes Docker Compose

```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down

# Reconstruire les images
docker-compose build

# Arrêter et supprimer les volumes (⚠️ perte de données)
docker-compose down -v
```

### Accéder aux Services

```bash
# Shell du backend
docker-compose exec backend bash

# PostgreSQL
docker-compose exec postgres psql -U postgres -d talait_translate_db

# Voir les tables
docker-compose exec postgres psql -U postgres -d talait_translate_db -c "\dt"
```

---


##  Auteur

**AYOUB MOTEI**


---

