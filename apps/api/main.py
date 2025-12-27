from fastapi import FastAPI
from apps.api.routers import prediction

app = FastAPI(title="InstruSense API", description="API pour la reconnaissance d'instruments de musique")

# Enregistrer les routers
app.include_router(prediction.router, prefix="/api", tags=["prediction"])

@app.get("/")
def root():
    """Page d'accueil de l'API"""
    return {
        "message": "InstruSense API",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health():
    """Vérifie que l'API fonctionne"""
    return {"status": "ok"}
