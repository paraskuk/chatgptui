import openai
import os
from openai import OpenAI
from exceptions.GPTException import GPTException
from logging_api import *
from models.query_model import QueryModel, FeedbackModel
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


def create_gpt4_completion(model: str, system_message: str, user_input: str) -> None or Optional[str]:
    """
    Function to create a GPT-4 completion request
    :param model: str, type of OpenAI model
    :param system_message: str, system message to be sent to the model
    :param user_input: str, user input to be sent to the model
    :return: None or String, completion response from the model
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_input}
            ]
        )

        if response.choices and len(response.choices) > 0 and response.choices[0].message:
            return response.choices[0].message.content
        else:
            return None

    except Exception as e:
        log.error(f"Error in GPT-4 completion request: {e}")
        return None


@app.post("/ask_gpt4/")
async def ask_gpt4(query_params: QueryModel) -> JSONResponse:
    """
    Function to receive a query and return a response using OpenAI's Chat Completions API
    :param query_params: QueryModel object containing the user input and model type
    :return: JSONResponse object containing the response
    """
    try:
        # Code completion
        code_completion = create_gpt4_completion(
            query_params.model,
            "You are a helpful assistant.",
            query_params.user_input
        )

        # Moderation API to evaluate the query
        moderation_result = client.moderations.create(
            input=query_params.user_input
        )

        if not code_completion:
            raise HTTPException(status_code=500, detail="No response from the model for code completion.")

        # User level estimation
        user_level_estimation = create_gpt4_completion(
            query_params.model,
            "Please evaluate and categorize the user's programming expertise level based on their previous query. Is the user a beginner, intermediate, or advanced programmer?",
            query_params.user_input
        )

        # Sentiment analysis
        sentiment_estimation = create_gpt4_completion(
            query_params.model,
            "Analyze the sentiment of the user's previous query. Is the sentiment positive, negative, or neutral?",
            query_params.user_input
        )

        # Formatting the final response
        final_response = code_completion
        if user_level_estimation:
            final_response += "\n\nUser Level Estimation: " + user_level_estimation
        if sentiment_estimation:
            final_response += "\n\nSentiment Analysis: " + sentiment_estimation

        return JSONResponse(content={"response": final_response})

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


@app.post("/send_feedback/")
async def send_feedback(feedback_data: FeedbackModel):
    # Log feedback
    log.info(f"Received feedback: {feedback_data.feedback} for response ID: {feedback_data.responseId}")

    # Here you can add logic to analyze feedback or store it for future improvements
    # Note: GPT-4 doesn't have a direct mechanism to improve based on this feedback

    return {"message": "Feedback received"}
