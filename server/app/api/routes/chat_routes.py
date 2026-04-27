from fastapi import APIRouter, Depends
from app.application.use_case.chat_use_case import ChatUseCase
from app.core.dependencies import get_chat_use_case
from app.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/chat", tags=["chat"])

@router.get("/history")
async def get_history(
    current_user=Depends(get_current_user),
    chat_use_case: ChatUseCase = Depends(get_chat_use_case)
):
    return await chat_use_case.get_user_history(str(current_user["_id"]))

@router.get("/{conversation_id}/messages")
async def get_messages(
    conversation_id: str,
    current_user=Depends(get_current_user),
    chat_use_case: ChatUseCase = Depends(get_chat_use_case)
):
    return await chat_use_case.get_messages(conversation_id)

@router.post("/{conversation_id}/message")
async def send_message(
    conversation_id: str,
    body: dict,
    current_user=Depends(get_current_user),
    chat_use_case: ChatUseCase = Depends(get_chat_use_case)
):
    return await chat_use_case.send_message(
        conversation_id,
        str(current_user["_id"]),
        body["prompt"]
    )

@router.post("/conversation")
async def create_conversation(
    body: dict,
    current_user=Depends(get_current_user),
    chat_use_case: ChatUseCase = Depends(get_chat_use_case)
):
    return await chat_use_case.create_conversation(
        str(current_user["_id"]),
        body["title"]
    )