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
