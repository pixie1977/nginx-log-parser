import uvicorn

from config import Settings

settings = Settings()

def main() -> None:
    """Entrypoint for running the FastAPI application with uvicorn."""
    uvicorn.run(
        "nginx_log_stats.api:app",
        host="0.0.0.0",
        port=8000,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()