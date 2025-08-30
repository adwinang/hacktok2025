from fastapi import APIRouter, HTTPException

# Import the reset function
from scripts.reset import reset_database


scripts_router = APIRouter(prefix="/scripts", tags=["scripts"])


@scripts_router.post("/reset")
async def run_reset_script():
    try:
        await reset_database()
        return {"success": True, "message": "Reset completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")
