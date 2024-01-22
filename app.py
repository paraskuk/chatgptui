import openai
import os
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

#######################end of imports#######################################

#####Object Instantiation##################################################


# instantiate FastAPI
app = FastAPI()
secret_session_key = os.getenv("SECRET_SESSION_KEY")
# this is the old middleware solution with secret key from github

# First, add the Redis middleware
app.add_middleware(RedisSessionMiddleware)

# Then, add Starlette's SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_SESSION_KEY"))

##app.add_middleware(RedisSessionMiddleware)

# Connect to Redis server
# redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


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


#########################GITHUB ROUTES#######################################


@app.get("/login/github")
async def login_via_github(request: Request):
    if 'auth_token' in request.state.session:
        log.debug("User already authenticated, redirecting to home.")
        return RedirectResponse(url='/')

    state = secrets.token_urlsafe(32)
    request.state.session['oauth_state'] = state
    log.debug(f"Generated OAuth state: {state}")

    session_id = request.cookies.get('session_id') or str(uuid.uuid4())
    redis_client.set(session_id, json.dumps(request.state.session), ex=3600)
    log.debug(f"Session data saved to Redis: {request.state.session} with session_id: {session_id}")

    try:
        redirect_uri = request.url_for('authorize')
        auth_url = await oauth.github.authorize_redirect(request, redirect_uri, state=state)
    except Exception as e:
        log.error(f"Error generating authorization URL: {e}")
        return RedirectResponse(url='/login-error?message=Error generating authorization URL')

    response = RedirectResponse(url=auth_url)
    response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=3600)
    log.debug(f"Redirecting to GitHub for authentication with session_id: {session_id}")

    return response


@app.route('/auth/github/callback', methods=['GET'], name='authorize')
async def authorize(request: Request):
    # Retrieve the session ID from the cookie
    session_id = request.cookies.get('session_id')
    log.debug(f"Callback received with session_id: {session_id}")

    if not session_id:
        log.error("Session ID is None. Possible cookie issue.")
        return RedirectResponse(url='/login-error?message=Session ID not found')

    # Retrieve the session data from Redis
    session_data_json = redis_client.get(session_id)
    if not session_data_json:
        log.error("Session data not found in Redis.")
        return RedirectResponse(url='/login-error?message=Session data not found')

    request.state.session = json.loads(session_data_json)
    log.debug(f"Retrieved session data from Redis: {session_data_json}")

    # Compare the OAuth state
    session_state = request.state.session.get('oauth_state')
    callback_state = request.query_params.get('state')
    log.debug(f"Session State: {session_state}, Callback State: {callback_state}")

    if session_state != callback_state:
        log.error("State mismatch error.")
        return RedirectResponse(url='/login-error?message=State mismatch')

    try:
        # Exchange the code for a token
        token = await oauth.github.authorize_access_token(request)
        request.state.session['auth_token'] = token['access_token']

        # Update the session data in Redis
        redis_client.set(session_id, json.dumps(request.state.session), ex=3600)

        log.debug("Authorization successful, redirecting to authenticated page.")
        return RedirectResponse(url='/authenticated')
    except Exception as e:
        log.error(f"Error during authorization: {e}")
        return RedirectResponse(url='/login-error?message=Authorization failure')


@app.get("/login-error")
async def login_error(request: Request, message: str):
    # Display an error message or render a template with the error
    return JSONResponse(content={"error": message}, status_code=400)


@app.get("/logout")
async def logout(request: Request):
    # Clear Redis session data
    log.debug("Performing logout.")
    session_id = request.cookies.get('session_id')
    if session_id:
        redis_client.delete(session_id)

    # Clear default session data
    request.session.clear()

    # Redirect to the home page or login page after logout
    return RedirectResponse(url='/')


@app.get("/authenticated")
async def authenticated(request: Request):
    # Implement the logic for authenticated users
    return JSONResponse({'message': 'Successfully authenticated with GitHub'})


def create_or_update_github_file(file: GitHubFile):
    url = f"https://api.github.com/repos/{file.repository}/contents/{file.filename}"
    data = {
        "message": f"Update {file.filename}",
        "content": base64.b64encode(file.content.encode()).decode("utf-8")
    }
    headers = {
        "Authorization": f"token {file.token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.put(url, json=data, headers=headers)
    if response.status_code not in [200, 201]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response.json())
    return response.json()


@router.post("/save-to-github")
async def save_to_github(file: GitHubFile):
    return create_or_update_github_file(file)


# Add this router to your FastAPI app
app.include_router(router)


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
            "You are a helpful assistant that answers only questions regarding programming.",
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
