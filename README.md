# InstruSense
Architecture détaillée générée automatiquement.

## Arborescence & flux

InstruSense/
│
├── apps/
│   ├── api/                 # API principale exposant les endpoints
│   │   ├── main.py          # FastAPI entrypoint
│   │   ├── routers/         # Définition des routes
│   │   ├── dto/             # Schémas Pydantic pour requêtes/réponses
│   │   ├── dependencies.py  # Injection de dépendances (modèles, config)
│   │   └── config.py        # Config API (host, port)
│   │
│   ├── inference/           # Service d’inférence séparé
│   │   ├── server.py        # FastAPI entrypoint
│   │   ├── adapter.py       # Adaptation pour la prédiction (bytes → features)
│   │   └── config.py        # Config inference (chemin modèle)
│   │
│   └── training/            # Scripts d’entrainement
│       ├── train_model.py
│       └── dataset_loader.py
│
├── core/                    # Logique métier et ML
│   ├── audio/
│   │   ├── processor.py     # Chargement audio
│   │   └── analyzer.py      # Extraction de features
│   │
│   ├── ml/
│   │   ├── model_loader.py  # Chargement modèle (pickle)
│   │   ├── predictor.py     # Prédiction sur features
│   │   └── postprocess.py   # Formatage de réponse
│   │
│   ├── interfaces/          # Ports pour architecture hexagonale
│   │   ├── model_loader_port.py
│   │   ├── predictor_port.py
│   │   └── audio_port.py
│   │
│   └── exceptions.py        # Exceptions métier
│
├── services/                # Adaptateurs / orchestrateurs
│   ├── prediction_service.py # Orchestrateur prédiction
│   ├── audio_adapter.py      # Chargement et preprocessing audio
│   └── model_loader_adapter.py # Chargement modèle depuis disk
│
├── infra/
│   ├── logging/config.py     # Setup logging
│   ├── settings/base.py      # Config globale (env, paths)
│   └── utils/paths.py        # Helpers chemins
│
├── models/
│   └── v1/instrument_model.pkl
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── features/
│
├── docker/
│   ├── api.Dockerfile
│   ├── inference.Dockerfile
│   ├── training.Dockerfile
│   └── docker-compose.yml
│
├── scripts/
│   └── dev/start_dev.sh
│
└── tests/
    ├── unit/
    ├── integration/
    └── e2e/

## Flux principaux

```

Client
│
▼
[apps/api/main.py]  ---> [routers] ---> [services/prediction_service.py] ---> [core/audio/analyzer.py + core/ml/predictor.py]
│
▼
[core/ml/postprocess.py]
│
▼
Response

apps/inference/server.py ---> services/audio_adapter.py ---> core/audio/processor.py
services/model_loader_adapter.py ---> core/ml/model_loader.py

apps/training/train_model.py ---> core/ml/model_loader.py + core/audio/analyzer.py ---> data/features

```

### Légende
- `apps/` : services exposés (API, inference, training)
- `core/` : logique métier et ML
- `services/` : adaptateurs entre core et apps
- `infra/` : config et utils
- `models/` : modèles ML
- `data/` : données brutes et features
- `docker/` : containerisation
- `scripts/` : scripts pratiques (dev, etc.)
- `tests/` : tests unitaires, intégration et E2E
```

