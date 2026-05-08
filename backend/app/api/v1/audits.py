from fastapi import APIRouter

router = APIRouter(prefix="/audits", tags=["audits"])

@router.get("/test")
def test():
    return {"message": "audit router working"}