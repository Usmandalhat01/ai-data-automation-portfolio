# Customer Support Assistant

A lightweight command-line assistant for common customer questions. It searches a small JSON knowledge base, returns the closest supported answer, assigns a category, and escalates requests it cannot handle confidently.

## Run

```bash
python app.py
```

The project deliberately uses transparent rule-based matching. It can later be connected to an LLM, help-desk API, Slack, email, or an n8n workflow without changing the basic escalation approach.
