from fastapi import FastAPI

app = FastAPI(
    title="AI Video Dubber",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "AI Video Dubber API is running"
    }