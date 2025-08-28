from fastapi import APIRouter

knowledge_base_router = APIRouter(
    prefix="/knowledge-base", tags=["knowledge-base"])


@knowledge_base_router.get("/")
async def get_knowledge_base():
    return {"message": "Hello World"}


@knowledge_base_router.post("/webhook")
async def create_knowledge_base(knowledge_base: str):
    # TODO:
    # 1. Pull data from knowledge base
    # 2. Conduct analysis on the data
    # 3. Update feature statuses
    # 4. Notify frontend

    return {"message": f"Webhook called with {knowledge_base}"}
