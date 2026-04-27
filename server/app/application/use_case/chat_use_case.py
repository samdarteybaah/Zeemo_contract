from datetime import datetime
from app.domain.entities.chat import ChatMessage, ChatHistory
from app.infrastructure.ai.chat_templates import chat_prompt
from app.infrastructure.repository.user_repository import UserRepository
from app.infrastructure.repository.chat_repository import ChatRepository

class ChatUseCase:

    def __init__(self, chat_repo: ChatRepository, gpt_provider):
        self.chat_repo = chat_repo
        self.gpt_provider = gpt_provider


    async def create_conversation(self, user_id: str, title: str):
        existing = await self.chat_repo.find_one({"user_id": user_id, "title": title})
        if existing:
            return existing # use the existing convo
        
        conversation = ChatHistory(
            user_id=user_id,
            title=title
        )

        return await self.chat_repo.create_conversation(
            conversation.model_dump()
        ) 
    
    
    async def send_message(self, conversation_id: str, user_id: str, prompt: str):
        # user message 
        user_message = ChatMessage(
            user_id=user_id,
            role = "user",
            content= prompt
        )

        await self.chat_repo.add_message(
            conversation_id,
            user_message.model_dump()
        )

        # gpt response
        try:
            response = await self.gpt_provider.generate(
                prompt_template=chat_prompt,
                input_variables={"prompt": prompt},
                parse_json=False
            )

            content = response if isinstance(response, str) else response.get("content", str(response))
        except Exception as e:
            raise RuntimeError(f"AI provider failed: {str(e)}")

        # turn gpt response into message
        assistant_message = ChatMessage(
            user_id=user_id,
            role = "assistant",
            content= content
        )

        await self.chat_repo.add_message(
            conversation_id,
            assistant_message.model_dump()
        )

        return {"response":content}
    
    async def get_user_history(self, user_id: str):
        return await self.chat_repo.get_user_conversations( user_id)
    
    async def get_messages(self, conversation_id: str):
        return await self.chat_repo.get_messages(conversation_id)
 