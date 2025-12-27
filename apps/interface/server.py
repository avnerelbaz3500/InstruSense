"""
Serveur simple pour l'interface web InstruSense
Ce fichier sert les fichiers HTML, CSS et JavaScript
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

# Créer l'application FastAPI
app = FastAPI(title="InstruSense Interface")

# Chemin vers le dossier de l'interface
INTERFACE_DIR = Path(__file__).parent
STATIC_DIR = INTERFACE_DIR / "static"
TEMPLATES_DIR = INTERFACE_DIR / "templates"

# Servir les fichiers statiques (CSS, JS, images)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# Route principale - afficher la page d'accueil
@app.get("/")
async def read_root():
    """Affiche la page d'accueil"""
    index_path = TEMPLATES_DIR / "index.html"
    return FileResponse(str(index_path))


# Route de santé
@app.get("/health")
async def health():
    """Vérifie que le serveur fonctionne"""
    return {"status": "ok", "service": "interface"}
