from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Dict

import requests

try:
    import openai
except ImportError:  # pragma: no cover
    openai = None

try:
    import google.generativeai as genai
except ImportError:  # pragma: no cover
    genai = None

try:
    import anthropic
except ImportError:  # pragma: no cover
    anthropic = None


class LLMConnector(ABC):
    """Abstract connector."""

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Return the model's response to the prompt."""


class OpenAIConnector(LLMConnector):
    def __init__(self, model: str = "gpt-3.5-turbo"):
        if openai is None:
            raise ImportError("openai library not installed")
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def generate_response(self, prompt: str) -> str:
        chat = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return chat.choices[0].message.content


class GeminiConnector(LLMConnector):
    def __init__(self, model: str = "gemini-pro"):
        if genai is None:
            raise ImportError("google-generativeai not installed")
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel(model)

    def generate_response(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text


class ClaudeConnector(LLMConnector):
    def __init__(self, model: str = "claude-3-opus-20240229"):
        if anthropic is None:
            raise ImportError("anthropic not installed")
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = model

    def generate_response(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text


class OllamaConnector(LLMConnector):
    def __init__(self, model: str = "llama3"):
        self.base_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model = model

    def generate_response(self, prompt: str) -> str:
        url = f"{self.base_url}/api/generate"
        response = requests.post(url, json={"model": self.model, "prompt": prompt})
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")


class GGUFConnector(LLMConnector):
    def __init__(self, model_path: str):
        raise NotImplementedError("Direct GGUF loading is not implemented")

    def generate_response(self, prompt: str) -> str:
        raise NotImplementedError
