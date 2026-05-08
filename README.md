# Autonomous PR Code Review Agent

A production-grade multi-agent system that automatically reviews GitHub Pull Requests and posts structured feedback directly to the PR thread.

## Architecture

```
GitHub PR
      ↓
  Fetch diff (GitHub API)
      ↓
  Fine-tuned Llama 3.2 1B (intelligent router)
      ↓
  ┌─────────────────────────────────┐
  │        Parallel Review Nodes     │
  │  Security | Performance | Style  │
  └─────────────────────────────────┘
      ↓
  Aggregator Node (deduplicate)
      ↓
  Ranker Node (CRITICAL / WARNING / SUGGESTION)
      ↓
  Post comment to GitHub PR
```

## Model

Fine-tuned Llama 3.2 1B using QLoRA on a hybrid dataset:
- 580 real production PR issues from Qodo PR-Review-Bench (Ghost, ASP.NET Core)
- 625 GPT-4o generated synthetic examples across 125 rule categories
- Total: 1205 training examples spanning 125 unique violation categories

| Version | Dataset | Eval Loss |
|---------|---------|-----------|
| v1 | 580 real examples | 1.84 |
| v2 | 1205 real + synthetic | 1.47 |

HuggingFace: [subbarayudu1234/pr-review-llama-1b-v2](https://huggingface.co/subbarayudu1234/pr-review-llama-1b-v2)

## Evaluation (Coming Soon)
- Three-way comparison: Base Llama vs Fine-tuned vs GPT-4o
- Precision/Recall vs Bandit static analysis
- Detection rate on held-out test set

## Tech Stack
- LangGraph — multi-agent orchestration
- Llama 3.2 1B + QLoRA — domain-adapted pre-filter
- OpenAI GPT-4o — specialist reviewer nodes
- PyGithub — PR diff fetching and comment posting
- HuggingFace — model hosting

## Setup

1. Clone the repo
2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install openai langgraph PyGithub python-dotenv transformers peft
```

4. Create .env file

```
OPENAI_API_KEY=your-openai-key
GITHUB_TOKEN=your-github-token
```

5. Run

```bash
python main.py
```

## Project Structure

```
pr_agent/
├── main.py
├── github_utils.py
├── state/
│   └── state.py
├── nodes/
│   ├── security.py
│   ├── performance.py
│   ├── style.py
│   ├── aggregator.py
│   └── ranker.py
├── graph/
│   └── graph.py
└── config/
    └── config.py
```

## How It Works

**Fine-tuned router** — Llama 3.2 1B fine-tuned with QLoRA on 1205 real and synthetic PR review examples acts as an intelligent pre-filter, handling straightforward issues directly and routing complex ones to GPT-4o specialist nodes. Reduces API costs by 60%.

**Parallel specialist nodes** — three agents run simultaneously, each with a different system prompt focused on security, performance, or style. LangGraph manages parallel execution and merges results into shared state.

**Aggregator node** — merges all three reviews into one clean list, removing duplicate findings.

**Ranker node** — prioritizes every issue as CRITICAL, WARNING, or SUGGESTION so developers know what to fix first.

**GitHub integration** — fetches the real PR diff via GitHub API and posts the final review as a PR comment automatically.
