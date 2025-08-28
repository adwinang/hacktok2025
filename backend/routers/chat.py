from fastapi import APIRouter

chat_router = APIRouter(prefix="/chat", tags=["chat"])


@chat_router.get("/")
async def get_chat():
    return {"message": "Hello World"}
