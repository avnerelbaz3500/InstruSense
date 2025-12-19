from fastapi import FastAPI
from .routers import prediction
from .config import API_HOST, API_PORT


# L'application FastAPI
app = FastAPI(
    title="InstruSense API", description="API de reconnaissance d'instruments"
)

# les routes
app.include_router(prediction.router)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=API_HOST, port=API_PORT)
