# Slack Archive (Postgres + SQLAlchemy + Alembic)


Capture Slack messages in realtime (Socket Mode) into Postgres. Designed for free-tier workspaces to preserve content before the 90‑day window.


## Quick start
1. **Create Slack app** → add required scopes → install → get `xoxb` & `xapp` tokens.
2. **Enable Socket Mode** & subscribe to:
- `message.channels`, `message.groups`, `message.im`, `message.mpim`
- `reaction_added`, `reaction_removed`
3. `cp .env.example .env` and fill values (no quotes).
4. Start Postgres: `docker compose up -d`
5. Install deps: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
6. Create DB tables:
```bash
alembic upgrade head # after init+revision below