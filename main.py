"""
Vercel deployment entrypoint.

Vercel's Python/FastAPI framework preset looks for a FastAPI `app` instance
in a root-level entrypoint file (main.py / app.py / index.py). All actual
application code lives in the `domainx` package (see domainx/server.py) --
this file only re-exports it so `uvicorn domainx.server:app` (local dev,
Docker, Helm) and the Vercel deployment both run the exact same app.
"""
from domainx.server import app

__all__ = ["app"]
