from fastapi import FastAPI
app = FastAPI(title="InstruSense Inference")

@app.get("/health")
def health():
    return {"status": "inference ok"}
