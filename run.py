import uvicorn


if __name__ == "__main__":
    config = uvicorn.Config("app:app", host="127.0.0.1", port=8000, reload=False)
    server = uvicorn.Server(config)
    server.run()
