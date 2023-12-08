import openai
import os
from openai import OpenAI
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
client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

# logging
log = logging.getLogger("uvicorn")



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

# This was the route with old completions API
# @app.post("/ask_gpt4/")
# async def ask_gpt4(query_params: QueryModel, model: Optional[str] = "text-davinci-003") -> dict:
#     """
#     Post Route receive a query and return a response with OpenAIAPI for chat GPT
#     :param query_params: User input in the form of questions to chat GPT
#     :param model: type of model as per OpenAIAPI specifications.
#     :return: Json in the form of a JSONResponse FastAPi instance
#     """
#     try:
#         # Call the OpenAI API
#         # The model used is not gpt4 to use gpt4 as a model a different API has to be used and
#         # in specific the openai.ChatCompletion.create(.....)
#         response = openai.Completion.create(
#             engine=model,
#             prompt=query_params.user_input,
#             max_tokens=1000,
#             n=1,
#             stop=None,
#             temperature=0.5,
#         )
#
#         if len(response.choices) > 0 and hasattr(response.choices[0], "text"):
#             answer = response.choices[0].text.strip()
#             return {"response": answer}
#         else:
#             error_msg = "ChatGPT response does not contain text attribute."
#             log.error(error_msg)
#             raise GPTException(error_msg)
#
#             # return {"error": "ChatGPT response does not contain text attribute."}
#     except GPTException as e:
#         raise e
#     except Exception as e:
#         log.error(f"Exception occurred: {str(e)}")
#         if not query_params.user_input:  # Empty user_input case
#             raise GPTException("Empty user_input", status_code=400)
#         else:
#             raise GPTException(str(e))
#     # except Exception as e:
#     #     return {"error": str(e)}
#
#     # Exception handling


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
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query_params.user_input}
            ]
        )

        # Extracting the response
        if response.choices and len(response.choices) > 0 and response.choices[0].message:
            return JSONResponse(content={"response": response.choices[0].message.content})
        else:
            raise HTTPException(status_code=500, detail="No response from the model.")
    except Exception as e:
        log.error(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# @app.exception_handler(HTTPException)
# async def http_exception_handler(exc: HTTPException) -> dict:
#     """
#         Function for exception handling. for old gpt
#         :param exc: the relevant exception raised
#         :return: dictionary, key , value a pair of status code and error detail.
#         """
#
#     log.debug("Calling http_exception_handler")
#     return {"detail": exc.detail, "status_code": exc.status_code}
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
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": str(exc)},
    )


