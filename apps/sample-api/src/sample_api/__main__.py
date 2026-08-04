"""Command-line entry point for local execution."""

import uvicorn


def main() -> None:
    """Run the API with production-style defaults."""
    uvicorn.run(
        "sample_api.main:app",
        host="0.0.0.0",
        port=8080,
        log_config=None,
        access_log=False,
    )


if __name__ == "__main__":
    main()
