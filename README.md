# InstruSense

┌───────────────────────────────┐
│         Frontend Streamlit    │
│  - Upload de fichiers audio   │
│  - Affichage des résultats    │
│  - Pages et composants UI     │
└──────────────┬────────────────┘
               │  Requête HTTP (POST /recognize)
               ▼
┌───────────────────────────────┐
│           API FastAPI         │
│  - Validation des fichiers    │
│  - Gestion des erreurs        │
│  - Logging structuré (Structlog) │
│  - Orchestration du moteur    │
└──────────────┬────────────────┘
               │ Appel interne au moteur audio
               ▼
┌───────────────────────────────┐
│     Moteur de traitement      │
│          maison               │
│  - Analyse du fichier audio   │
│  - Détection des instruments │
│  - Possibilité ML / DSP       │
└──────────────┬────────────────┘
               │ Retour des résultats
               ▼
┌───────────────────────────────┐
│     Résultat JSON / Liste     │
│       d’instruments           │
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│  Streamlit frontend affiche   │
│  la liste des instruments    │
└───────────────────────────────┘


my_audio_app/
│
├── apps/                             # Applications (frontend/backend)
│   ├── frontend/                     # Streamlit
│   │   ├── __init__.py
│   │   ├── main.py                   
│   │   ├── components/               
│   │   └── config.py                 
│   │
│   └── backend/                      # FastAPI
│       ├── __init__.py
│       ├── main.py                   
│       ├── routes/                   
│       ├── services/                 # Orchestration (appelle domain/)
│       ├── schemas/                  
│       └── config.py                 
│
├── domain/                           # Logique métier (PURE, pas de dépendance web)
│   ├── audio/                        
│   │   ├── __init__.py
│   │   ├── processor.py              # Traitement audio pur
│   │   └── analyzer.py               
│   └── ml/                           
│       ├── __init__.py
│       ├── model_loader.py           # Chargement modèle avec cache
│       └── predictor.py              
│
├── infrastructure/                   # Infrastructure technique
│   ├── __init__.py
│   ├── logging_config.py             
│   ├── settings.py                   # Config globale
│   └── utils.py                      # Utils GÉNÉRIQUES
│
├── data/                             # NOUVEAU: Séparation données
│   ├── models/                       
│   │   └── v1/
│   │       └── instrument_model.pkl
│   ├── samples/                      
│   └── processed/                    
│
├── tests/                            
│   ├── unit/                         
│   │   ├── test_domain/              
│   │   └── test_infrastructure/
│   ├── integration/                  
│   └── conftest.py                   
│
├── docker/                           
│   ├── frontend.Dockerfile           
│   ├── backend.Dockerfile            
│   └── docker-compose.yml
│
├── scripts/                          
│   ├── start_dev.sh                  
│   └── train_model.py                
│
├── pyproject.toml                    # Config uv workspace
├── uv.lock                           
└── .env.example                      
