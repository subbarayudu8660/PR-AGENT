# Autonomous Code Review Agent

A multi-agent system that automatically reviews GitHub Pull Requests using LangGraph and GPT-4o. The agent runs specialist reviewers in parallel, aggregates findings, and posts a prioritized review directly to the PR.

## Architecture

```
GitHub PR
      ↓
  Fetch diff (GitHub API)
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

## Tech Stack
- LangGraph — multi-agent orchestration
- OpenAI GPT-4o — specialist reviewers
- PyGithub — PR diff fetching and comment posting
- Python-dotenv — secret management

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

## Setup

1. Clone the repo
2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```
3. Install dependencies
```bash
pip install openai langgraph PyGithub python-dotenv
```
4. Create `.env` file
```
OPENAI_API_KEY=your-openai-key
GITHUB_TOKEN=your-github-token
```
5. Run
```bash
python main.py
```

## How it works

**Parallel specialist nodes** — three agents run simultaneously, each with a different system prompt focused on security, performance, or style. LangGraph manages the parallel execution and merges results into shared state.

**Aggregator node** — merges all three reviews into one clean list, removing duplicate findings that multiple specialists flagged.

**Ranker node** — prioritizes every issue as CRITICAL, WARNING, or SUGGESTION so developers know what to fix first.

**GitHub integration** — fetches the real PR diff via the GitHub API and posts the final review as a PR comment, just like a human reviewer would.
