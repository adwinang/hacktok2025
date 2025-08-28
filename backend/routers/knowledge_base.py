from fastapi import APIRouter

knowledge_base_router = APIRouter(
    prefix="/knowledge-base", tags=["knowledge-base"])


@knowledge_base_router.get("/")
async def get_knowledge_base():
    return {"message": "Hello World"}


@knowledge_base_router.post("/webhook")
async def create_knowledge_base(knowledge_base: str):
    """
    Webhook for the knowledge base to call when new regulation is available.
    This will be used to trigger the knowledge base service to process the new regulation and check on existing features.
    """

    knowledge_base_service = knowledge_base_router.knowledge_base_service

    # TODO: Implement
    # knowledge_base_service.process_new_regulation(knowledge_base)

    return {"message": f"Webhook called with data: {knowledge_base}"}
