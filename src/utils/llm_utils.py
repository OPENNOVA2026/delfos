import json
from typing import Any

from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel

from core.logger import logger
from core.settings import settings


class UsageModel(BaseModel):
    input_tokens: int
    output_tokens: int


class ResponseModel(BaseModel):
    content: str | dict[Any, Any]
    usage: UsageModel


class LLMManager:
    def __init__(
        self, model: str = "gpt-4.1-mini", temperature: int = 0, seed: int = 42
    ):
        self.llm = AzureChatOpenAI(
            azure_deployment=model,
            api_key=settings.openai.azure_openai_api_key,
            api_version=settings.openai.openai_api_version,
            azure_endpoint=settings.openai.azure_openai_endpoint,
            temperature=temperature,
            seed=seed,
        )

        self.json_llm = AzureChatOpenAI(
            azure_deployment=model,
            api_key=settings.openai.azure_openai_api_key,
            api_version=settings.openai.openai_api_version,
            azure_endpoint=settings.openai.azure_openai_endpoint,
            temperature=temperature,
            seed=seed,
        ).bind(response_format={"type": "json_object"})

    def invoke(self, prompt: str, json_mode: bool = False) -> ResponseModel:
        try:
            if json_mode:
                response = self.json_llm.invoke(prompt)
                usage = response.usage_metadata
                content = json.loads(response.content)
            else:
                response = self.llm.invoke(prompt)
                usage = response.usage_metadata
                content = response.content
        except Exception:
            logger.error("LLM invoking failed", stack_info=True, exc_info=True)
            usage = {"input_tokens": 0, "output_tokens": 0}
            content = {}

        usage = UsageModel(
            input_tokens=usage["input_tokens"], output_tokens=usage["output_tokens"]
        )
        return ResponseModel(content=content, usage=usage)
