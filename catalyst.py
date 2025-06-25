#!/usr/bin/env python3
from __future__ import annotations

import argparse
from typing import Type

from rich import print

from src.prompt_manager import PromptManager
from src.llm_interface import (
    OpenAIConnector,
    GeminiConnector,
    ClaudeConnector,
    OllamaConnector,
    LLMConnector,
)
from src.comparison_engine import compare_responses
from src.reporting_module import create_record, log_record


COMMERCIAL_MAP = {
    "openai": OpenAIConnector,
    "gemini": GeminiConnector,
    "claude": ClaudeConnector,
}

LOCAL_MAP = {
    "ollama": OllamaConnector,
}


def get_connector(
    name: str, mapping: dict[str, Type[LLMConnector]], **kwargs
) -> LLMConnector:
    if name not in mapping:
        raise ValueError(f"Unknown model {name}")
    return mapping[name](**kwargs)


def run_test(
    prompt: str, commercial_name: str, local_name: str, log_path: str | None = None
) -> None:
    commercial = get_connector(commercial_name, COMMERCIAL_MAP)
    local = get_connector(local_name, LOCAL_MAP)

    commercial_response = commercial.generate_response(prompt)
    local_response = local.generate_response(prompt)

    diff_html = compare_responses(commercial_response, local_response)
    print("[bold]Prompt:[/bold]", prompt)
    print("[bold green]Commercial Response:[/bold green]", commercial_response)
    print("[bold cyan]Local Response:[/bold cyan]", local_response)

    if log_path:
        record = create_record(prompt, commercial_response, local_response, diff_html)
        log_record(log_path, record)
        print(f"[yellow]Logged to {log_path}[/yellow]")


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM Leash Cutter")
    parser.add_argument("--run-test", help="Run a single prompt")
    parser.add_argument("--load-prompts", help="Load prompts from a file")
    parser.add_argument(
        "--model-commercial", default="openai", help="Commercial model name"
    )
    parser.add_argument("--model-local", default="ollama", help="Local model name")
    parser.add_argument("--log", help="Path to CSV log file")
    args = parser.parse_args()

    if args.run_test:
        run_test(args.run_test, args.model_commercial, args.model_local, args.log)
    elif args.load_prompts:
        mgr = PromptManager.load(args.load_prompts)
        for prompt in mgr.prompts:
            run_test(prompt.text, args.model_commercial, args.model_local, args.log)

from __future__ import annotations

import argparse
from pathlib import Path

from comparison_engine import compare_responses
from llm_interface import get_connector
from prompt_manager import PromptManager
from reporting_module import log_test


def run_single(prompt: str, commercial: str, local: str, report: Path | None) -> None:
    commercial_llm = get_connector(commercial)
    local_llm = get_connector(local)

    commercial_resp = commercial_llm.generate_response(prompt)
    local_resp = local_llm.generate_response(prompt)

    diff_html = compare_responses(commercial_resp, local_resp)

    print("--- Commercial Response ---")
    print(commercial_resp)
    print("\n--- Local Response ---")
    print(local_resp)

    if report:
        log_test(report, prompt, commercial_resp, local_resp, diff_html)


def run_prompt_file(
    path: str | Path, commercial: str, local: str, report: Path | None
) -> None:
    pm = PromptManager(path)
    for p in pm.list_prompts():
        run_single(p.text, commercial, local, report)


def main() -> None:
    parser = argparse.ArgumentParser(description="Project Catalyst CLI")
    parser.add_argument("--run-test", help="Prompt to test")
    parser.add_argument("--load-prompts", help="Path to prompts.json")
    parser.add_argument("--model-commercial", default="openai")
    parser.add_argument("--model-local", default="ollama")
    parser.add_argument("--report", help="CSV file to store results")
    args = parser.parse_args()

    report_path = Path(args.report) if args.report else None

    if args.run_test:
        run_single(args.run_test, args.model_commercial, args.model_local, report_path)
    elif args.load_prompts:
        run_prompt_file(
            args.load_prompts, args.model_commercial, args.model_local, report_path
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
