import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

def translate_text_api(text, direction):
    api_key = os.getenv("HUGGING_FACE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Clé API manquante")

    client = InferenceClient(
        provider="hf-inference",
        api_key=api_key,
    )

    try:
        # Appel API
        result = client.translation(
            text,
            model=f"Helsinki-NLP/opus-mt-{direction}",
        )
        
        # Gestion du format de retour (parfois objet, parfois liste)
        if isinstance(result, list) and len(result) > 0:
             return result[0].get('translation_text', "")
        
        return result.translation_text
        
    except Exception as e:
        print(f"Erreur HF: {e}")
        raise HTTPException(status_code=503, detail="Service de traduction indisponible")