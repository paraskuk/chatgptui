import openai
import os
from openai import OpenAI
from exceptions.GPTException import GPTException
from logging_api import *
from models.query_model import QueryModel
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# instantiate FastAPI
app = FastAPI()
# instantiate OpenAI
client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

# logging instantiation
LoggerConfiguration.close_loggers()
logger_config = LoggerConfiguration("askgpt.log", logging.DEBUG)
log = logger_config.get_logger()

# Set up the templates directory for HTML templates
templates_directory = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=templates_directory)
app.mount("/templates", StaticFiles(directory=templates_directory), name="templates")


@app.get("/")
async def index(request: Request):
    """
    Function to return HTML template
    :param request:
    :return: HTML template
    """
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except HTTPException as exc:
        log.exception("An HTTPException occurred: %s", exc.detail)
        return http_exception_handler(exc)



@app.post("/ask_gpt4/")
async def ask_gpt4(query_params: QueryModel) -> JSONResponse:
    """
    Endpoint to receive a query and return a response using OpenAI's Chat Completions API
    :param query_params: User input
    :return: JSONResponse containing the response
    """
    try:

        # Using the Chat Completions API
        response = client.chat.completions.create(
            model=query_params.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for coding completions in Python using version of at least 3.11."},
                {"role": "user", "content": query_params.user_input}
            ]
        )

        # Adding Moderation API tracking
        moderation_input = client.moderations.create(
            input=query_params.user_input
        )

        # Extracting the response
        if response.choices and len(response.choices) > 0 and response.choices[0].message:
            return JSONResponse(content={"response": response.choices[0].message.content})
        else:
            raise HTTPException(status_code=500, detail="No response from the model.")
    except Exception as e:
        log.error(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Function for HTTP exception handling.
    :param request: the request that caused the exception
    :param exc: the relevant exception raised
    :return: JSONResponse with error detail and status code.
    """
    log.debug("Calling http_exception_handler")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(GPTException)
async def gpt_exception_handler(request: Request, exc: GPTException):
    """
    Function for GPT exception handling.
    :param request: request object
    :param exc: exception
    :return: JSONResponse with error detail and status code.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": str(exc)},
    )
