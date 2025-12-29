# Interface Web InstruSense

Interface utilisateur simple pour InstruSense utilisant HTML, CSS et JavaScript.

## Structure

```
apps/interface/
├── server.py          # Serveur FastAPI pour servir l'interface
├── config.py          # Configuration (port, host)
├── templates/         # Fichiers HTML
│   └── index.html
└── static/            # Fichiers statiques
    ├── css/
    │   └── style.css
    ├── js/
    │   └── app.js
    └── images/
```

## Comment ça marche

### HTML (index.html)
- Structure de la page web
- Formulaire pour uploader un fichier audio
- Zones d'affichage pour les résultats

### CSS (style.css)
- Styles visuels (couleurs, espacements, animations)
- Mise en page responsive

### JavaScript (app.js)
- Gestion du formulaire
- Appels à l'API backend (`/predict`)
- Affichage des résultats

## Lancer l'interface

```bash
# Depuis la racine du projet
uvicorn apps.interface.server:app --reload --host 0.0.0.0 --port 3000
```

Puis ouvrez votre navigateur sur : http://localhost:3000

## Configuration

Modifiez `config.py` pour changer le port ou l'hôte.

Dans `static/js/app.js`, modifiez `API_BASE_URL` pour pointer vers votre API backend (par défaut: http://localhost:8000).

