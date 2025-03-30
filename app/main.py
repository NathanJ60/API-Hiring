from fastapi import FastAPI
from app.routes import datasets

app = FastAPI(title="Dataset API")

app.include_router(datasets.router, prefix="/datasets", tags=["Datasets"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)