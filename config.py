"""Environment-backed configuration for PRO ART EDITOR GOD MODE X."""
from __future__ import annotations

import os


def _int_env(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default


APP_NAME = os.getenv("APP_NAME", "PRO ART EDITOR GOD MODE X")
APP_ENV = os.getenv("APP_ENV", "development")
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
OWNER_ID = _int_env("OWNER_ID", 0)
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
MAX_UPLOAD_MB = max(1, _int_env("MAX_UPLOAD_MB", 50))
