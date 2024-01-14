import uvicorn

if __name__ == "__main__":
    # uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True,ssl_keyfile="key.pem",
    #             ssl_certfile="cert.pem")

    config = uvicorn.Config("app:app", host="127.0.0.1", port=8000, reload=False)
    server = uvicorn.Server(config)
    server.run()

# --ssl-keyfile=newkey.pem --ssl-certfile=cert.pem