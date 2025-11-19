from fastapi import FastAPI
app = FastAPI(title="InstruSense API")

@app.get("/health")
def health():
    return {"status": "ok"}
