from fastapi import FastAPI
from routers import prediction

# L'application FastAPI
app = FastAPI(title="InstruSense API",
    description="API de reconnaissance d'instruments")

# les routes
app.include_router(prediction.router)

@app.get("/health")
def health():
    return {"status": "ok"}
