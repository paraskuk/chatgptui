import json
import uuid

import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from typing import Union, Any
from app import ask_gpt4, app, http_exception_handler
from exceptions.GPTException import GPTException
from models.query_model import QueryModel, RedisSessionMiddleware
from unittest.mock import patch, Mock
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from unittest.mock import patch, AsyncMock
import pytest
from starlette.responses import RedirectResponse, JSONResponse, Response
from httpx import AsyncClient

client = TestClient(app)

from unittest.mock import patch, MagicMock


class MockGPTResponse:
    def __init__(self, code_completion, user_level_estimation, sentiment_estimation):
        self.code_completion = code_completion
        self.user_level_estimation = user_level_estimation
        self.sentiment_estimation = sentiment_estimation


class MockModerationResponse:
    def __init__(self, flagged=False):
        self._flagged = flagged

    def json(self):
        return {
            "flagged": self._flagged
        }


@pytest.mark.asyncio
async def test_login_via_github():
    """
    Test the login via GitHub endpoint with AsyncClient
    :return: boolean, True if the test passes with 302 code for redirect
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/login/github")
        assert response.status_code == 302
        assert "location" in response.headers
        assert response.headers["location"].startswith("https://github.com/login/oauth/authorize")


@pytest.mark.asyncio
async def test_gpt_exception_handler():
    """
    Function to test the GPT exception handler
    :return: boolean, True if the test passes with 400, 404 code for bad request
    """
    client = TestClient(app)
    response = client.get("/trigger-exception")

    assert response.status_code == 400 or response.status_code == 404


@pytest.mark.asyncio
async def test_authorize():
    """
    Test the authorize endpoint with AsyncClient
    :return: boolean, True if the test passes with 307 or 302 code for redirect
    """
    with patch('app.oauth.github.authorize_access_token', new_callable=AsyncMock) as mock_oauth:
        mock_oauth.return_value = {'access_token': 'test_token'}
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get('/auth/github/callback?code=testcode')

            assert response.status_code == 307 or response.status_code == 302


def test_index_page():
    """
    Function to test the index page where the user can input a query
    :return: boolean    True if the test passes
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"


def test_login_error():
    """
    Function to test the login error message
    :return: boolean to check if the test passes
    """
    test_message = "Test error message"
    response = client.get(f"/login-error?message={test_message}")
    assert response.status_code == 400
    assert response.headers["content-type"] == "application/json"
    response_data = response.json()
    assert response_data == {"error": test_message}


def test_logout_redirects_to_index():
    """
    Function to test the logout endpoint
    :return: boolean, True if the test passes with 307 code for redirect after logout to index
    """
    response = client.get("/logout", allow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/"


@pytest.mark.asyncio
async def test_redis_session_middleware():
    """
    Function to test the redis session middleware
    :return: boolean, True if the test passes with 200 code
    """
    with patch('models.query_model.redis_client.get', MagicMock(return_value=None)), \
            patch('models.query_model.redis_client.set', MagicMock()) as mock_set, \
            patch('uuid.uuid4', MagicMock(return_value=uuid.UUID('12345678-4567-5678-9888-567812345678'))):
        response = client.get("/")

        assert response.status_code == 200

        assert 'session_id' in response.cookies

        assert mock_set.called


@pytest.mark.asyncio
async def test_ask_gpt4_endpoint_gpt4():
    """
    Function to test the ask_gpt4 endpoint with AsyncClient
    :return: boolean, True if the expected response is returned and matches the actual response from GPT-4
    response is not necessary deterministic so the test might fail
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/ask_gpt4/", json={
            "model": "gpt-4",
            "user_input": "What is the result of the python function sum([3,5])? Provide only the result with a "
                          "single number only.For user level estimation and sentiment analysis estimation use only "
                          "one word starting with a capital letter."
        })

    assert response.status_code == 200
    response_data = response.json()

    expected_response = (
        "8\n\nUser Level Estimation: Beginner\n\nSentiment Analysis: Neutral"
    )


    assert response_data["response"] in expected_response



