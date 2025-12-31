# InstruSense

**Reconnaissance automatique d'instruments de musique par deep learning**

Projet réalisé par l'**Équipe 5**

---

## Présentation du projet

InstruSense est une application web permettant d'identifier automatiquement les instruments de musique présents dans un fichier audio. L'utilisateur importe un fichier audio via une interface web intuitive, et le système lui renvoie la liste des instruments détectés grâce à un modèle de deep learning.

Le projet repose sur un réseau de neurones convolutif (CNN) entraîné sur le dataset IRMAS, capable de reconnaître 8 classes d'instruments : guitare électrique, piano, violon, saxophone, trompette, guitare acoustique, orgue et flûte.

---

## Conformité aux critères d'évaluation

### Développement avec qualité 

#### Code quality

Le projet utilise **flake8** pour le linting et **black** pour le formatage automatique du code. La configuration est définie dans le fichier `.flake8` avec une longueur de ligne maximale de 120 caractères. Une pipeline CI/CD GitHub Actions vérifie automatiquement la qualité du code à chaque push.

```bash
# Vérification du linting
flake8 . --max-line-length=120 --extend-ignore=E203

# Formatage automatique
black .
```

#### Unit tests

Une suite complète de tests unitaires et d'intégration est disponible dans le dossier `tests/`. Les tests sont exécutés via **pytest** et couvrent les DTOs, les services métier et les routes FastAPI.

```bash
# Exécution des tests unitaires
uv run pytest tests/unit/ -v

# Exécution des tests d'intégration
uv run pytest tests/integration/ -v
```

Les tests sont également exécutés automatiquement dans la pipeline CI/CD à chaque commit.

#### Typing

L'ensemble du code Python utilise les **type hints** pour garantir la robustesse et la lisibilité.



---

### Partage du code 

Le code source est hébergé sur **GitHub** et partagé entre tous les membres de l'équipe. Le workflow de collaboration utilise les branches Git et les pull requests pour assurer une intégration continue du code.

La pipeline CI/CD (`.github/workflows/ci_cd.yml`) exécute automatiquement les vérifications suivantes à chaque push :
- Linting avec flake8
- Formatage avec black
- Exécution des tests unitaires

---

### Documentation 

Ce README constitue la documentation principale du projet. Il couvre :
- La présentation et les objectifs du projet
- L'architecture technique détaillée
- Les instructions d'installation et d'exécution
- La structure complète du projet
- Le fonctionnement du pipeline de prédiction
- La documentation des endpoints API

Des README supplémentaires sont disponibles dans les sous-dossiers `apps/api/` et `apps/interface/` pour documenter chaque service individuellement.

---

### Conteneurisation 

Le projet est entièrement conteneurisé avec **Docker**. Trois Dockerfiles distincts permettent de construire chaque service indépendamment :

- `docker/Dockerfile.api` — Service API léger
- `docker/Dockerfile.inference` — Service d'inférence avec PyTorch et FFmpeg
- `docker/Dockerfile.interface` — Interface web statique

Le fichier `docker-compose.yml` orchestre les trois services :

```yaml
services:
  api:
    build:
      context: .
      dockerfile: docker/Dockerfile.api
    ports:
      - "8000:8000"

  inference:
    build:
      context: .
      dockerfile: docker/Dockerfile.inference
    ports:
      - "8001:8001"

  interface:
    build:
      context: .
      dockerfile: docker/Dockerfile.interface
    ports:
      - "3000:3000"
```

Lancement en une seule commande :

```bash
docker-compose up --build
```

---

### Créativité 

L'interface utilisateur se démarque par son design original inspiré des disques vinyles. Lorsqu'une analyse est effectuée, les instruments détectés apparaissent sous forme de petits disques qui "explosent" autour du vinyle central avec une animation fluide.

Chaque disque d'instrument est cliquable et ouvre une modal affichant l'image de l'instrument ainsi qu'un bouton permettant d'écouter un sample audio de cet instrument.

Les animations CSS ont été réalisées sans librairie externe, en utilisant uniquement des keyframes et des transitions CSS natives.

---

## Architecture technique

```
┌──────────────────┐
│   INTERFACE      │  ← Interface utilisateur (HTML/CSS/JavaScript)
│   Port 3000      │
└────────┬─────────┘
         │ POST /api/predict
         ▼
┌──────────────────┐
│      API         │  ← Gateway REST (validation, routage)
│   Port 8000      │
└────────┬─────────┘
         │ POST /infer
         ▼
┌──────────────────┐
│   INFERENCE      │  ← Service de prédiction (PyTorch, CNN)
│   Port 8001      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Modèle CNN      │  ← Réseau entraîné (checkpoint.pth)
└──────────────────┘
```

L'architecture microservices permet de séparer les responsabilités : l'interface sert les fichiers statiques, l'API valide et route les requêtes, et le service d'inférence gère toute la logique de machine learning. Cette séparation facilite la maintenance et permet de scaler le service d'inférence indépendamment.

---

## Technologies utilisées

| Composant | Technologies |
|-----------|--------------|
| Backend API | FastAPI, Pydantic, HTTPX |
| Machine Learning | PyTorch, torchaudio |
| Frontend | HTML5, CSS3, JavaScript (vanilla) |
| Tests | pytest, pytest-asyncio |
| Qualité de code | flake8, black |
| Conteneurisation | Docker, docker-compose |
| CI/CD | GitHub Actions |
| Hébergement modèle | Hugging Face Hub |

---

## Instruments reconnus

| Classe | Instrument | Seuil de détection |
|--------|------------|-------------------|
| 0 | Guitare électrique | 0.475 |
| 1 | Piano | 0.723 |
| 2 | Violon | 0.554 |
| 3 | Saxophone | 0.683 |
| 4 | Trompette | 0.822 |
| 5 | Guitare acoustique | 0.900 |
| 6 | Orgue | 0.545 |
| 7 | Flûte | 0.614 |

---

## Installation et exécution

### Prérequis

Le projet nécessite Python 3.10 ou supérieur ainsi que le gestionnaire de paquets **uv**. Pour le service d'inférence, FFmpeg doit être installé sur le système.

### Installation des dépendances

```bash
git clone https://github.com/votre-repo/InstruSense.git
cd InstruSense

uv sync
uv sync --extra ml
```

### Lancement des services

**Terminal 1 — Service d'inférence :**
```bash
uv run uvicorn apps.inference.server:app --port 8001
```

**Terminal 2 — API :**
```bash
uv run uvicorn apps.api.main:app --port 8000
```

**Terminal 3 — Interface :**
```bash
uv run uvicorn apps.interface.server:app --port 3000
```

L'application est accessible à l'adresse http://localhost:3000.

### Déploiement avec Docker

```bash
docker-compose up --build
```

---

## Structure du projet

```
InstruSense/
├── apps/
│   ├── api/                   # Service API (port 8000)
│   │   ├── main.py            # Point d'entrée FastAPI
│   │   ├── routers/           # Définition des routes
│   │   ├── dto/               # Schémas de validation Pydantic
│   │   └── config.py          # Configuration
│   │
│   ├── inference/             # Service d'inférence ML (port 8001)
│   │   ├── server.py          # Point d'entrée FastAPI
│   │   ├── adapter.py         # Adaptateur modèle
│   │   └── config.py          # Configuration
│   │
│   └── interface/             # Interface web (port 3000)
│       ├── server.py          # Serveur de fichiers statiques
│       ├── templates/         # Fichiers HTML
│       └── static/            # CSS, JavaScript, images, sons
│
├── models/
│   └── CNN10_v1/
│       ├── config/            # Configuration du modèle
│       ├── weight/            # Poids entraînés (.pth)
│       └── stats/             # Historique d'entraînement
│
├── services/
│   └── prediction_service.py  # Service métier de prédiction
│
├── tests/
│   ├── unit/                  # Tests unitaires
│   └── integration/           # Tests d'intégration
│
├── docker/                    # Dockerfiles
├── docker-compose.yml         # Orchestration Docker
├── .github/workflows/         # Pipeline CI/CD
└── pyproject.toml             # Dépendances Python
```

---

## Pipeline de prédiction

### Étape 1 : Prétraitement audio

Le fichier audio est découpé en segments de 3 secondes. Chaque segment est converti en mel-spectrogramme (128 bandes de fréquences) puis normalisé avant d'être transmis au modèle.

### Étape 2 : Inférence CNN

Le modèle CNN traite chaque spectrogramme et produit un vecteur de 8 probabilités. L'architecture comprend trois blocs convolutifs suivis de couches fully-connected avec dropout.

### Étape 3 : Agrégation

Un instrument est considéré présent s'il est détecté dans au moins 60% des segments, ce qui réduit les faux positifs.

---

## Endpoints API

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/` | Informations sur l'API |
| GET | `/health` | Health check |
| GET | `/docs` | Documentation Swagger |
| POST | `/api/predict` | Analyse d'un fichier audio |

**Exemple :**

```bash
curl -X POST "http://localhost:8000/api/predict" -F "file=@audio.wav"
```

**Réponse :**

```json
{
  "instruments": ["piano", "violin"]
}
```

---

## Équipe 5

Projet réalisé dans le cadre du cours de développement logiciel.