"""Command-line entry point for local and container execution."""

import uvicorn

CONTAINER_HOST = "0.0.0.0"  # noqa: S104 -- required for container networking
CONTAINER_PORT = 8080


def main() -> None:
    """Run the API with production-style defaults."""
    uvicorn.run(
        "sample_api.main:app",
        host=CONTAINER_HOST,
        port=CONTAINER_PORT,
        log_config=None,
        access_log=False,
    )


if __name__ == "__main__":
    main()
