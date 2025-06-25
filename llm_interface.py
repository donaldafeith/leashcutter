from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class LLMConnector(ABC):
    """Abstract base connector for LLMs."""

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        pass


class OpenAIConnector(LLMConnector):
    def __init__(self, model: str = "gpt-3.5-turbo") -> None:
        import openai  # type: ignore

        self.openai = openai
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")

    def generate_response(self, prompt: str) -> str:
        resp = self.openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            api_key=self.api_key,
        )
        return resp["choices"][0]["message"]["content"].strip()


class GeminiConnector(LLMConnector):
    def __init__(self, model: str = "models/gemini-pro") -> None:
        import google.generativeai as genai  # type: ignore

        self.genai = genai
        self.model = model
        api_key = os.getenv("GOOGLE_API_KEY")
        self.genai.configure(api_key=api_key)

    def generate_response(self, prompt: str) -> str:
        model = self.genai.GenerativeModel(self.model)
        resp = model.generate_content(prompt)
        return resp.text.strip()


class ClaudeConnector(LLMConnector):
    def __init__(self, model: str = "claude-3-opus-20240229") -> None:
        import anthropic  # type: ignore

        self.client = anthropic.Anthropic()
        self.model = model

    def generate_response(self, prompt: str) -> str:
        resp = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text.strip()


class OllamaConnector(LLMConnector):
    def __init__(self, model: str = "llama3") -> None:
        import ollama  # type: ignore

        self.ollama = ollama
        self.model = model

    def generate_response(self, prompt: str) -> str:
        resp = self.ollama.chat(
            model=self.model, messages=[{"role": "user", "content": prompt}]
        )
        return resp["message"]["content"].strip()


CONNECTORS = {
    "openai": OpenAIConnector,
    "gemini": GeminiConnector,
    "claude": ClaudeConnector,
    "ollama": OllamaConnector,
}


def get_connector(name: str) -> LLMConnector:
    if name not in CONNECTORS:
        raise ValueError(f"Unknown connector: {name}")
    return CONNECTORS[name]()
