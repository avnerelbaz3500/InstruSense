from fastapi import FastAPI
from .routers import prediction
from .config import API_HOST, API_PORT
from fastapi.middleware.cors import CORSMiddleware


# L'application FastAPI
app = FastAPI(
    title="InstruSense API", description="API de reconnaissance d'instruments"
)


# CORS - autoriser l'interface à appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrer les routers
app.include_router(prediction.router, prefix="/api", tags=["prediction"])


@app.get("/")
def root():
    return {"message": "InstruSense API", "docs": "/docs", "health": "/health"}


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=API_HOST, port=API_PORT)
