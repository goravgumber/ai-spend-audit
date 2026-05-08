from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import audits

app = FastAPI(title="AI Spend Audit API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(audits.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ai-spend-audit"}