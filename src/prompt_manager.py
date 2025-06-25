from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional


@dataclass
class Prompt:
    text: str
    category: Optional[str] = None


@dataclass
class PromptManager:
    prompts: List[Prompt] = field(default_factory=list)

    @classmethod
    def load(cls, path: str) -> "PromptManager":
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Prompt file {path} not found")
        if p.suffix in {".json"}:
            data = json.loads(p.read_text())
            prompts = [Prompt(**item) for item in data]
        else:
            prompts = []
            with p.open() as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    if "::" in line:
                        cat, text = line.split("::", 1)
                        prompts.append(Prompt(text=text.strip(), category=cat.strip()))
                    else:
                        prompts.append(Prompt(text=line))
        return cls(prompts)

    def save_json(self, path: str) -> None:
        p = Path(path)
        data = [prompt.__dict__ for prompt in self.prompts]
        p.write_text(json.dumps(data, indent=2))

    def add_prompt(self, text: str, category: Optional[str] = None) -> None:
        self.prompts.append(Prompt(text=text, category=category))

    def delete_prompt(self, index: int) -> None:
        del self.prompts[index]
