from fastapi import FastAPI

from app.routers.routers import main_router

app = FastAPI(
    title="Test_async API",
    version="1.0.0"
)

app.include_router(main_router)


@app.get("/")
def read_root():
    return {"message": "Test_async API"}
