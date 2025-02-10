#!/usr/bin/env python
"""
Development entrypoint for `c-block-store` project.

This script runs the FastAPI application using Uvicorn with automatic
reload enabled for development purposes.
"""

import uvicorn


def main() -> None:
    uvicorn.run(
        app="core.fastapi.asgi:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_delay=5.0,
        use_colors=True,
    )


if __name__ == "__main__":
    main()
