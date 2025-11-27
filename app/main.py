from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db 
from app.schemas import UserCreate, UserResponse, Token, TranslateRequest, TranslateResponse
from app.models import User
from app.auth import create_access_token, hash_password, verify_password, get_current_user
from app.services.huggingface import translate_text_api
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

# Charger les variables d'environnement depuis .env
load_dotenv()

# Initialisation de l'app
app = FastAPI(title="TalAIt Secure Translate API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Création des tables au démarrage
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API opérationnelle"}
    
@app.post("/register", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    #  Vérifier si user existe
    existing_user = db.query(User).filter(User.username == user.username).first()
    
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")
    
    # Hasher le mot de passe
    hashed_pwd = hash_password(user.password)
    
    #  Sauvegarder (On utilise password_hash)
    db_user = User(username=user.username, password_hash=hashed_pwd)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    #  Chercher l'user UNIQUEMENT par username
    db_user = db.query(User).filter(User.username == user.username).first()

    #  Vérifier le mot de passe hashé
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

    #  Créer le token
    token = create_access_token(data={"sub": db_user.username})

    return {"access_token": token, "token_type": "bearer"}

@app.post("/translate", response_model=TranslateResponse)
def translate(
    request: TranslateRequest, 
    current_user: User = Depends(get_current_user) 
):
    # Construction de la direction (ex: "fr-en") à partir du schéma
    direction = f"{request.source_language}-{request.target_language}"
    
    # Appel au service
    translation = translate_text_api(request.text, direction)
    
    return {"translated_text": str(translation)}


@app.get("/test-env")
def test_env():
    return {
        "hf_key_configured": bool(os.getenv("HUGGING_FACE_API_KEY")),
        "jwt_secret_configured": bool(os.getenv("SECRET_KEY")),
        "hf_key_preview": os.getenv("HUGGING_FACE_API_KEY", "")[:10] + "..." if os.getenv("HUGGING_FACE_API_KEY") else "None"
    }