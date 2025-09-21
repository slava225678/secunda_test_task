from fastapi import FastAPI

from app.routers.routers import main_router

app = FastAPI(
    title="Secunda Test Task API",
    version="1.0.0"
)

app.include_router(main_router)


@app.get("/")
def read_root():
    return {"message": "Secunda_test_task API"}
