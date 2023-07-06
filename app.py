import openai
import os

from exceptions.GPTException import GPTException
from models.query_model import QueryModel
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import logging


app = FastAPI()

# logging
log = logging.getLogger("uvicorn")
openai.api_key = os.getenv("OPEN_AI_KEY")

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
async def ask_gpt4(query_params: QueryModel, model: Optional[str] = "text-davinci-003") -> dict:
    """
    Post Route receive a query and return a response with OpenAIAPI for chat GPT
    :param query_params: User input in the form of questions to chat GPT
    :param model: type of model as per OpenAIAPI specifications.
    :return: Json in the form of a JSONResponse FastAPi instance
    """
    try:
        # Call the OpenAI API
        # The model used is not gpt4 to use gpt4 as a model a different API has to be used and
        # in specific the openai.ChatCompletion.create(.....)
        response = openai.Completion.create(
            engine=model,
            prompt=query_params.user_input,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.5,
        )

        if len(response.choices) > 0 and hasattr(response.choices[0], "text"):
            answer = response.choices[0].text.strip()
            return {"response": answer}
        else:
            error_msg = "ChatGPT response does not contain text attribute."
            log.error(error_msg)
            raise GPTException(error_msg)

            # return {"error": "ChatGPT response does not contain text attribute."}
    except GPTException as e:
        raise e
    except Exception as e:
        log.error(f"Exception occurred: {str(e)}")
        if not query_params.user_input:  # Empty user_input case
            raise GPTException("Empty user_input", status_code=400)
        else:
            raise GPTException(str(e))
    # except Exception as e:
    #     return {"error": str(e)}

    # Exception handling


@app.exception_handler(HTTPException)
async def http_exception_handler(exc: HTTPException) -> dict:
    """
        Function for exception handling.
        :param exc: the relevant exception raised
        :return: dictionary, key , value a pair of status code and error detail.
        """

    log.debug("Calling http_exception_handler")
    return {"detail": exc.detail, "status_code": exc.status_code}


@app.exception_handler(GPTException)
async def gpt_exception_handler(request: Request, exc: GPTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": str(exc)},
    )
