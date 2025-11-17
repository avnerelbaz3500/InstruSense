# Architecture my_audio_app

## Principes
- DDD : domain/ isolé
- Services orchestrent domain/ + infrastructure/
- Tests par module

## Flux de données
1. Frontend Streamlit upload fichier
2. Backend FastAPI reçoit via /predict
3. Service appelle domain/audio/processor.py
4. Modèle chargé via domain/ml/model_loader.py
5. Retour JSON au frontend
