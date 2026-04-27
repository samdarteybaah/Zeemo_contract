from fastapi import HTTPException
from datetime import datetime
from app.domain.entities.contract_analysis import ContractAnalysis
from app.domain.entities.chat import ChatMessage, ChatHistory
from app.domain.services.contract_analyser import ContractAnalyser

from app.infrastructure.repository.user_repository import UserRepository
from app.infrastructure.repository.contract_repository import ContractRepository
from app.infrastructure.repository.chat_repository import ChatRepository

class AnalyseContractUseCase:
    def __init__(
        self,
        user_repo: UserRepository,
        contract_repo: ContractRepository,
        chat_repo: ChatRepository,
        analyser: ContractAnalyser
    ):
        self.user_repo = user_repo
        self.contract_repo = contract_repo
        self.chat_repo = chat_repo
        self.analyser = analyser

    def generate_title(self, contract_text: str) -> str:
        words = contract_text.replace("\n", " ").split()
        title = " ".join(words[:8])
        return title[:80]

    async def execute(self, user_id: str, contract_text: str):
        # validate user
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # adding contract text to db
        contract = ContractAnalysis(
            user_id=str(user["_id"]), 
            contract_text=contract_text,
            created_at=datetime.now()
        )

        saved_contract = await self.contract_repo.save_analysis(contract)

        # running AI analysis on contract
        try:
            analysis_result = await self.analyser.analyze(contract_text)
        except Exception as e:
            raise RuntimeError(f"Analysis failed: {str(e)}")

        # add results to db
        await self.contract_repo.update(
            saved_contract["_id"],  
            {
                "summary": analysis_result.summary,
                "overall_score": analysis_result.overall_score
            }
        )

        # saving chat messages in a convo
        conversation = ChatHistory(
            user_id=user_id,
            title=self.generate_title(contract_text)
        )
        saved_conversation = await self.chat_repo.create_conversation(conversation.model_dump())

        # user message
        user_message = ChatMessage(
            user_id=user_id,
            role="user",
            content=contract_text
        )
        await self.chat_repo.add_message(
            saved_conversation["_id"], 
            user_message.model_dump()
        )

        # assistant response
        assistant_message = ChatMessage(
            user_id=user_id,
            role="assistant",
            content=analysis_result.summary
        )
        await self.chat_repo.add_message(
            saved_conversation["_id"],  
            assistant_message.model_dump()
        )

        return {
            "contract_id": saved_contract["_id"],
            "summary": analysis_result.summary,
            "risks": analysis_result.risks,
            "obligations": analysis_result.obligations,
            "negotiation_suggestions": analysis_result.negotiation_suggestions,
            "ambiguity_flags": analysis_result.ambiguity_flags,
            "scores": analysis_result.scores,
            "overall_score": analysis_result.overall_score
        }