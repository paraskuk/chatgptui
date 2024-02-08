####################### START OF IMPORTS SECTION #############
import openai
import os
import time
from datetime import datetime, timedelta
from starlette.responses import Response
from openai import OpenAI
from exceptions.GPTException import GPTException
from logging_api import *
from models.query_model import QueryModel, FeedbackModel, GitHubFile, redis_client
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse
from models.query_model import RedisSessionMiddleware
import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import requests
import base64
from fastapi import FastAPI, Request, HTTPException
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
import redis
from starlette.requests import Request
import uuid
import json

#######################END OF IMPORTS SECTION#######################################

#####Object Instantiation##################################################

# instantiate FastAPI
app = FastAPI()
secret_session_key = os.getenv("SECRET_SESSION_KEY")
# this is the old middleware solution with secret key from github

# First, add the Redis middleware
app.add_middleware(RedisSessionMiddleware)

# Then, add Starlette's SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_SESSION_KEY"))

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

##################################GITHUB AUTHENTICATION#######################
oauth = OAuth()
oauth.register(
    name='github',
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'public_repo'}
)

router = APIRouter()


#########################GITHUB ROUTES#######################################

@app.get("/login/github")
async def login_via_github(request: Request):
    """
    Function to handle github login once user press the login button
    :param request:
    :return:
    """
    # Generate the OAuth state
    state = secrets.token_urlsafe(32)
    request.session['oauth_state'] = state

    # Define the redirect URI for OAuth callback
    redirect_uri = request.url_for('authorize')

    # Generate the authorization URL and redirect the user to GitHub for authentication
    try:
        # Ensure `authorize_redirect` is properly awaited
        return await oauth.github.authorize_redirect(request, redirect_uri, state=state)
    except Exception as e:
        # Log error and return a JSON response indicating the failure
        log.debug(f"Error during GitHub authorization redirect: {e}")  # Consider using a proper logging mechanism
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})


@app.route('/auth/github/callback')
async def authorize(request: Request):
    """
    Function to handle the OAuth callback and exchange the code for a token
    :param request:
    :return:
    """
    # Handle the OAuth callback and exchange the code for a token
    try:
        token = await oauth.github.authorize_access_token(request)
        request.state.session['auth_token'] = token['access_token']
        # Process the token (e.g., create a user session)
        # Redirect the user to a target page after successful authentication
        log.info("Successfully authenticated with GitHub redirecting to home page")
        return RedirectResponse(url='/')
    except Exception as e:
        # Log error and handle the failure (e.g., redirect to an error page)
        log.error(f"Error in OAuth callback: {e}")
        return RedirectResponse(url='/error-page')


@app.get("/login-error")
async def login_error(request: Request, message: str):
    """
    Function to handle errors with logins
    :param request:
    :param message:
    :return:
    """
    # Display an error message or render a template with the error
    log.error(f"Login error: {message}")
    return JSONResponse(content={"error": message}, status_code=400)


@app.get("/logout")
async def logout(request: Request):
    """
    Function to logout from Github
    :param request:
    :return:
    """
    # Clear Redis session data
    log.info("Performing logout.")
    session_id = request.cookies.get('session_id')
    if session_id:
        log.info(f"Deleting session data for session ID")
        redis_client.delete(session_id)

    # Clear default session data
    request.session.clear()
    log.info(f"cleared default session data")
    # Redirect to the home page or login page after logout
    log.info("Redirecting to home page after logout.")
    return RedirectResponse(url='/')


@app.get("/authenticated")
async def authenticated(request: Request):
    # Implement the logic for authenticated users
    log.info("Successfully authenticated with GitHub")
    return JSONResponse({'message': 'Successfully authenticated with GitHub'})


@app.post("/save-to-github/{username}/{repository}")
async def save_to_github(repository: str, request: Request, file: GitHubFile):
    log.info("Starting save to github route")

    if 'auth_token' not in request.state.session:
        log.info("auth token not in session, raising exception")
        raise HTTPException(status_code=401, detail="Not authenticated with GitHub")

    log.info("Retrieving access token from the session")
    access_token = request.state.session['auth_token']

    full_repo = f"{file.username}/{repository}"
    url = f"https://api.github.com/repos/{full_repo}/contents/{file.filename}"

    # Log the received file object
    log.debug(f"Received file object: filename={file.filename}, content preview={file.content[:30]}...")

    # encoded_content = base64.b64encode(file.content.encode()).decode("utf-8")
    # data = {
    #     "message": file.message,
    #     "content": encoded_content,
    # }

    decoded_content = base64.b64decode(file.content.encode()).decode("utf-8")
    data = {
        "message": file.message,
        "content": base64.b64encode(decoded_content.encode()).decode("utf-8"),
    }

    if file.committer:  # If committer info is provided, include it
        data["committer"] = file.committer

    # Log the prepared data dictionary
    log.debug(f"Prepared data for GitHub API call: {data}")

    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    log.info(f"Making a PUT request to the GitHub API for {url}")
    response = requests.put(url, json=data, headers=headers)

    if response.status_code not in [200, 201]:
        log.error(f"GitHub API call failed: status_code={response.status_code}, detail={response.json()}")
        raise HTTPException(status_code=response.status_code, detail=response.json())

    log.info("Successfully saved to GitHub")
    return response.json()


# Add this router to your FastAPI app
app.include_router(router)


@app.get("/debug/session")
async def debug_session(request: Request):
    """
    Function to debug the session data
    :param request: request object
    :return:  dictionary of session data
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        session_data = redis_client.get(session_id)
        return {"session_id": session_id, "session_data": session_data}
    return {"error": "No session ID found"}


######################################## Standard Routes for UI #############
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
            "You are a helpful assistant that answers only questions regarding programming in Python.",
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
    """
    Function to receive feedback from the user and log it.
    :param feedback_data: Instance of FeedbackModel
    :return: Dictionary with message indicating feedback received
    """
    # Log feedback
    log.info(f"Received feedback: {feedback_data.feedback} for response ID: {feedback_data.responseId}")

    # Here you can add logic to analyze feedback or store it for future improvements
    # Note: GPT-4 doesn't have a direct mechanism to improve based on this feedback

    return {"message": "Feedback received"}
