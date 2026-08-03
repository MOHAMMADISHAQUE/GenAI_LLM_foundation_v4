# Phase 1.5 — Token Management + Cost

Building on phase 1.4's streaming chatbot: counting tokens before sending, trimming conversation history to stay under a token budget, choosing the right model tier, and tracking real per-turn cost.

## What this covers
- `client.messages.count_tokens(...)` — a separate call that only counts, doesn't generate; useful for cost estimation and catching context-window overflow before it happens
- What actually happens when you exceed the context window (a hard rejection at the API layer, not silent truncation)
- Input vs. output token pricing — output costs roughly 3-5x more, so shortening responses is a bigger cost lever than trimming input history
- Choosing between Haiku / Sonnet / Opus based on task difficulty, not perceived importance
- Trimming history by popping oldest `user`/`assistant` pairs together (to preserve strict role alternation), recomputing the token count every loop iteration
- Tracking real per-turn and running-total cost from `final_message.usage`

## Project structure
.
├── main.py             # streaming multi-turn chat + token counting + history trimming + cost tracking
├── requirements.txt
├── src/
│   └── client.py        # builds and returns an authenticated Anthropic client

