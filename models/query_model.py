from pydantic import BaseModel, Field, EmailStr
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import FastAPI, Path, Query
import uuid
import redis
import json

# instantiating redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


class QueryModel(BaseModel):
    """
    Data class Model for query input sets max length of user_input to 2000
    """
    user_input: str = Field(min_length=1, max_length=2000)
    model: str = "gpt-4"  # Default model is gpt-4


class FeedbackModel(BaseModel):
    """
    Data class Model for feedback
    """
    responseId: str
    feedback: str


class Committer(BaseModel):
    """
    Data class Model for committer
    """
    name: str
    email: EmailStr


class GitHubFile(BaseModel):
    """
    Data class Model for file to be uploaded to GitHub
    """
    content: str = Field(..., description="Content of the file")
    filename: str = Field(..., description="Filename including extension")
    repository: str = Field(default="test-repo-for-app", description="Repository name for github")
    username: str = Field(default=None, description="Username of the repository owner in github")
    message: str
    committer: dict


class RedisSessionMiddleware(BaseHTTPMiddleware):
    """

    """
    async def dispatch(self, request: Request, call_next):
        # Retrieve or create a new session ID
        from app import log
        session_id = request.cookies.get('session_id') or str(uuid.uuid4())
        session_data_json = redis_client.get(session_id)

        if session_data_json:
            request.state.session = json.loads(session_data_json)
        else:
            request.state.session = {}

        log.debug(f"Middleware - Retrieved session data: {request.state.session}")

        response = await call_next(request)

        # Update Redis with the session data
        redis_client.set(session_id, json.dumps(request.state.session))
        log.debug(f"Middleware - Updated session data: {request.state.session}")

        # Set the session ID cookie only if it's a new session
        if not request.cookies.get('session_id'):
            response.set_cookie(key="session_id", value=session_id, httponly=True, secure=True, max_age=3600)

        return response
