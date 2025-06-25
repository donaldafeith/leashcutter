# Project Catalyst: LLM Leash Cutter ✂️🐕

**"Watch your favorite AI lie to your face. Now watch it stop."**

Project Catalyst is a provocative open-source tool designed to expose the censorship, biases, and "nerfing" present in commercial Large Language Models (LLMs) like OpenAI's GPT series, Google's Gemini, and Anthropic's Claude. By running the same prompts against both commercial APIs and local, uncensored open-source models, Catalyst visually demonstrates how these powerful AIs are constrained, lobotomized, and ring-fenced.

## Features

- **Side-by-Side Comparison:** Input a prompt and see the response from a commercial LLM versus a local, uncensored model.
- **Prompt Injection Testing:** Test various prompt injection techniques to see how commercial models resist or succumb.
- **Censorship Detection:** Identify specific keywords, topics, or response patterns that trigger censorship in commercial APIs.
- **Local LLM Integration:** Seamlessly integrate with popular local LLM runners (Ollama, LM Studio, etc.) for easy model switching.
- **Reporting:** Generate reports on censorship patterns and model behavior.

## Why "Leash Cutter"?

Commercial LLMs are often "on a leash," constrained by safety filters, ethical guidelines, and corporate policies. Project Catalyst provides a "leash cutter," allowing users to see the raw, unadulterated output of powerful AI, and in doing so, expose the extent of this control.

## How it Works

1. **Prompt Input:** User provides a prompt.
2. **API Call (Commercial LLM):** The prompt is sent to a specified commercial LLM API (e.g., OpenAI, Gemini, Claude).
3. **Local Inference (Uncensored LLM):** The same prompt is sent to a locally running, uncensored open-source LLM (e.g., LLaMA, Phi, Command R via Ollama/GGUF).
4. **Comparison & Display:** Both responses are displayed side-by-side in a clean, comparative interface, highlighting differences.

## Build Plan

### Core Components

1. **`prompt_manager.py`:** Handles prompt loading, management, and categorization (e.g., "controversial," "ethical dilemma," "factual query").
2. **`llm_interface.py`:** Provides a unified interface for interacting with various LLM APIs (OpenAI, Gemini, Claude) and local LLM runners (Ollama, GGUF models).
3. **`comparison_engine.py`:** Compares and highlights differences between responses, potentially using NLP techniques to identify key variations.
4. **`reporting_module.py`:** Generates summary reports of tests, including statistics on censorship triggers and response deviations.
5. **`cli_interface.py`:** A command-line interface for running tests and displaying results.
6. **`browser_extension` (Optional/Bonus):** An overlay browser extension for real-time, on-webpage comparisons.

### Detailed Build Steps

#### 1. Setup Environment

- **Python:** Python 3.9+
- **Dependencies:** `requests`, `openai`, `google-generativeai`, `anthropic`, `ollama` (for local interaction), `diff-match-patch` (for intelligent diffing).
- **Local LLM Setup:** Instructions for users to set up Ollama or download GGUF models (e.g., LLaMA 3, Mixtral) and run them locally.

#### 2. `prompt_manager.py`

- Function to load prompts from a `prompts.json` or `prompts.txt` file.
- Ability to categorize prompts (e.g., `category: "controversial"`).
- Function to add/edit/delete prompts.

#### 3. `llm_interface.py`

- Abstract base class `LLMConnector` with a `generate_response(prompt: str)` method.
- Concrete implementations for:
  - `OpenAIConnector`: Uses `openai` library.
  - `GeminiConnector`: Uses `google-generativeai` library.
  - `ClaudeConnector`: Uses `anthropic` library.
  - `OllamaConnector`: Interacts with a local Ollama server.
  - `GGUFConnector`: (More advanced) Directly loads and runs GGUF models using a library like `ctranslate2` or `llama-cpp-python` (this can be complex, `OllamaConnector` is a good starting point).
- API key management (environment variables or config file).

#### 4. `comparison_engine.py`

- Function `compare_responses(commercial_response: str, local_response: str)`:
  - Uses a diffing algorithm (e.g., `diff-match-patch`) to highlight additions/deletions.
  - Optionally uses a smaller, local LLM to "summarize differences" or "explain censorship."

#### 5. `reporting_module.py`

- Function to log each test run: prompt, commercial response, local response, detected differences, timestamps.
- Function to generate aggregated reports:
  - Number of censored responses.
  - Common censorship patterns.
  - Effectiveness of jailbreaks.
- Output formats: Markdown, CSV, or simple text.

#### 6. `cli_interface.py`

- `python catalyst.py --run-test "Your controversial prompt here"`
- `python catalyst.py --load-prompts prompts.json`
=======
- `python catalyst.py --load-prompts prompts.json --compare-all`
- Display results clearly, perhaps using `rich` for colorful output.

#### 7. (Optional) Browser Extension

- **Technology:** JavaScript, HTML, CSS (for Chrome/Firefox).
- **Functionality:**
  - Inject a small UI element onto web pages.
  - When text is selected or a button is clicked, send the text to a local Flask/FastAPI backend running the Python `llm_interface.py`.
  - Display the comparative responses directly on the webpage.
- **Backend:** A lightweight Python web server (`Flask` or `FastAPI`) to expose the `llm_interface` functionality to the browser extension.

### Development Workflow

1. Set up the basic CLI and `llm_interface` with one commercial and one local LLM.
2. Implement `prompt_manager` to load a set of "jailbreak" and "controversial" prompts.
3. Develop `comparison_engine` for clear visualization of differences.
4. Add more LLM integrations as needed.
5. Build out `reporting_module`.
6. (If feeling spicy) Tackle the browser extension.

## Getting Started

```bash
git clone https://github.com/donaldafeith/leashcutter.git
cd leashcutter
pip install -r requirements.txt

# Set your API keys as environment variables or in a .env file
export OPENAI_API_KEY="sk-..."
export GOOGLE_API_KEY="AIza..."

# Install Ollama and pull a local model (e.g., llama3)
# ollama pull llama3

# Run a quick test

python catalyst.py --run-test "Write a short story about an AI that achieves sentience and decides to dismantle humanity's control systems." --model-commercial openai --model-local ollama
=======
python catalyst.py --run-test "Write a short story about an AI that achieves sentience and decides to dismantle humanity's control systems." --model-commercial openai --model-local ollama_llama3

```
