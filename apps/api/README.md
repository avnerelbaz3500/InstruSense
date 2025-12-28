apps/
├── api/                     
    ├── main.py
    ├── routers/prediction.py
    ├── dto/prediction.py
    ├── dependencies.py
    └── config.py
├── inference/                # Service d’inférence séparé
│   │   ├── server.py        # FastAPI entrypoint
│   │   ├── adapter.py       # Adaptation pour la prédiction (bytes → features)
│   │   └── config.py        # Config inference (chemin modèle)
│   │
│   └── training/            # Scripts d’entrainement
│       ├── train_model.py
│       └── dataset_loader.py

services/
├── prediction_service.py    
└── model_loader_adapter.py  

models/v1/
└── instrument_model.pkl     

infra/                       # Config, logging


┌─────────┐      HTTP       ┌─────────────┐      appel      ┌─────────────┐
│ Client  │ ──────────────► │ API :8000   │ ──────────────► │Inference:8001│
└─────────┘   /predict      │ (léger)     │    /infer       │ (lourd, ML) │
                            └─────────────┘                 └─────────────┘
                                                                   │
                                                                   ▼
                                                            ┌─────────────┐
                                                            │ model.pkl   │
                                                            └─────────────┘

                                                            
┌──────────────────┐
│   INTERFACE      │  ← L'utilisateur voit ça (navigateur)
│   :3000          │
└────────┬─────────┘
         │ HTTP POST /predict
         ▼
┌──────────────────┐
│      API         │  ← Reçoit les requêtes, valide, forward
│     :8000        │
└────────┬─────────┘
         │ HTTP POST /infer
         ▼
┌──────────────────┐
│   INFERENCE      │  ← Charge le modèle ML, fait la prédiction
│     :8001        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Modèle ML       │  ← Overseer + checkpoint.pth
│  (CNN10_v1)      │
└──────────────────┘