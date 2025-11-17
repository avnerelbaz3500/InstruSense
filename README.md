# InstruSense


### Architecture proposée


```
InstruSense/
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
```
