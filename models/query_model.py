from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import uuid
import redis
import json

# instantiating redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


class QueryModel(BaseModel):
    user_input: str = Field(min_length=1, max_length=2000)
    model: str = "gpt-4"  # Default model


class FeedbackModel(BaseModel):
    responseId: str
    feedback: str


class GitHubFile(BaseModel):
    content: str
    filename: str
    repository: str
    token: str  # consider a more secure way to handle tokens


class RedisSessionMiddleware(BaseHTTPMiddleware):
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
