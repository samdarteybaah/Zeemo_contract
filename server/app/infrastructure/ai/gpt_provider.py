#gpt provider
from abc import ABC, abstractmethod
from typing import Any, Dict


class GPTProvider(ABC):
    # this is an abstract GPT Provider
    @abstractmethod
    async def generate(
        self,
        prompt : str,
        temperature : float = 0.7,
        max_token : int = 512,
        **kwargs     
    ) -> Dict[str, Any]:
        
        # this generates a properly structured JSON response
        
        raise NotImplementedError