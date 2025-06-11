from fastapi import FastAPI
from routes import router

app = FastAPI(title="Transcript Summarization API (Modular)")
app.include_router(router)
