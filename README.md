# PRO ART EDITOR GOD MODE X

Telegram-first creative editing platform, deployed with Render.

## Current milestone: Foundation (0.1.0)

- FastAPI web service with `/` and `/health` endpoints.
- Telegram bot worker with a starter menu.
- Docker image includes FFmpeg for future video processing.
- Render Blueprint defines a Web Service, Telegram Background Worker, and PostgreSQL database.

Photo/video processing, AI providers, cloud object storage, payments, and the full dashboard are planned milestones; they are not active yet.

## Render deployment

1. Push this repository to GitHub.
2. In Render, create a Blueprint from this repository.
3. Set `BOT_TOKEN` and `OWNER_ID` on the Telegram worker.
4. Render provisions the web service, worker, and PostgreSQL database from `render.yaml`.
5. Open the web service URL and check `/health`.

## Environment variables

- `BOT_TOKEN`: Telegram token from @BotFather (keep secret).
- `OWNER_ID`: numeric Telegram user ID of the bot owner.
- `DATABASE_URL`: supplied by Render PostgreSQL.
- `APP_NAME`: optional display name.
- `APP_ENV`: deployment environment.
- `MAX_UPLOAD_MB`: planned upload-size limit.

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Run the Telegram worker separately with `python bot.py` after setting `BOT_TOKEN`.

## Important deployment notes

- The Background Worker and PostgreSQL are paid Render resources; verify current pricing before deploying.
- Render's local filesystem is ephemeral. Do not use it as permanent media storage.
- Large video rendering should be queued and processed by dedicated workers. 4K output depends on the source media, codecs, and available CPU/RAM.
- Never commit real API keys, bot tokens, or payment secrets.
