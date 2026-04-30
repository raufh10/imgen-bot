# 🤖 posting-agent

A personal Telegram bot that curates Reddit news, generates LinkedIn-ready content using AI, and posts it — all through a guided chat interface.

## ✨ What It Does

1. 📥 Fetches unprocessed news posts from a PostgreSQL database (sourced from Reddit)
2. 👀 Presents them one by one for review — keep or drop
3. ✍️ Generates up to 3 LinkedIn draft variations per post using an AI content agent
4. 🎨 Generates a matching image for the chosen draft using an AI image agent
5. ✅ Allows image approval or regeneration before posting
6. 🚀 Posts approved content to LinkedIn with a random delay between each post (1–5 min)

State is managed per-session in Redis. All interaction happens through Telegram inline buttons.

## 🛠 Stack

| Library | Purpose |
|---|---|
| **fastapi** | Webhook server for Telegram updates |
| **uvicorn** | ASGI server |
| **python-telegram-bot** | Telegram bot integration |
| **openai** | Text and image generation via Responses API |
| **openai-agents** | Agent runner for designer and artist agents |
| **pydantic / pydantic-settings** | Data models and env config |
| **asyncpg** | Async PostgreSQL client |
| **redis[asyncio]** | Session and state caching |
| **httpx** | Async HTTP client for LinkedIn API |

## 📁 Project Layout

```
src/bot/
├── api/          # 🌐 FastAPI webhook endpoint and auth dependency
├── bot/          # 💬 Telegram handlers, keyboards, states, guards, runner, session
├── cache/        # ⚡ Redis client, session state, temp session storage, models
├── core/         # ⚙️  App config (pydantic-settings) and logging
├── db/           # 🗄  PostgreSQL client, CRUD, and Pydantic models
├── export/       # 📤 LinkedIn API client, image uploader, post publisher, service
├── llm/          # 🧠 AI agents, prompts, models, image gen tool
└── main.py       # 🚪 App entrypoint — FastAPI + bot lifecycle
```

## 🔄 Flow

```
/start
  └── 📥 Load yesterday's news from DB
        └── 👀 Review one by one (Keep / Drop)
              └── ✍️  Generate 3 drafts per kept item (AI Designer Agent)
                    └── 🖊  Pick a draft
                          └── 🎨 Generate image (AI Artist Agent)
                                └── ✅ Approve or 🔄 Redo
                                      └── 🚀 Confirm → Post to LinkedIn
                                                    ⏱ (1–5 min delay between posts)
```

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `ENVIRONMENT` | `development` or `production` |
| `TELEGRAM_BOT_TOKEN` | 🤖 From @BotFather |
| `WEBHOOK_URL` | 🌐 Public HTTPS domain, no trailing slash |
| `WEBHOOK_SECRET` | 🔑 Random secret for webhook auth |
| `ADMIN_USER_ID` | 👤 Your Telegram user ID |
| `LINKEDIN_CLIENT_ID` | 💼 LinkedIn app client ID |
| `LINKEDIN_CLIENT_SECRET` | 🔒 LinkedIn app client secret |
| `LINKEDIN_PERSON_ID` | 🪪 Your LinkedIn person ID |
| `LINKEDIN_TOKEN` | 🎫 OAuth access token |
| `OPENAI_API_KEY` | 🧠 OpenAI API key |
| `DEFAULT_MODEL` | e.g. `gpt-4o` |
| `IMAGE_MODEL` | e.g. `gpt-image-1` |
| `DATABASE_URL` | 🗄 PostgreSQL connection string |
| `REDIS_URL` | ⚡ Redis connection string |

> 💡 In `development` mode the bot runs in polling — no webhook or HTTPS needed.
