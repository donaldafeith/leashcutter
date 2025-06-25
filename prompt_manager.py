import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any


@dataclass
class Prompt:
    text: str
    category: str = "general"


class PromptManager:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.prompts: List[Prompt] = []
        if self.path.exists():
            self.load()

    def load(self) -> None:
        if not self.path.exists():
            self.prompts = []
            return
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.prompts = [Prompt(**p) for p in data]

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([p.__dict__ for p in self.prompts], f, indent=2)

    def add(self, prompt: str, category: str = "general") -> None:
        self.prompts.append(Prompt(prompt, category))
        self.save()

    def delete(self, index: int) -> None:
        if 0 <= index < len(self.prompts):
            del self.prompts[index]
            self.save()

    def list_prompts(self) -> List[Prompt]:
        return self.prompts
