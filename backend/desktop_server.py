import argparse

import uvicorn


def main() -> None:
    parser = argparse.ArgumentParser(description="JUBA LISAN desktop backend")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        workers=1,
        log_level="info",
    )


if __name__ == "__main__":
    main()
