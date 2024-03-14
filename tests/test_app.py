import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from typing import Union, Any
from app import ask_gpt4, app, http_exception_handler
from models.query_model import QueryModel

client = TestClient(app)


@pytest.mark.asyncio
@pytest.mark.parametrize("query_params, model, expected_output", [
    (
            {
                "user_input": "What is the capital of France?Please answer with one word only and dont add dot at the end"},
            "text-davinci-003",
            "Paris"
    ),
    (
            {"user_input": "Which is the capital of UK? Please answer with one word only and dont add dot at the end"},
            "text-davinci-003",
            "London"
    ),
    # Add more test cases here
])
async def test_ask_gpt4(query_params, model, expected_output):
    response = client.post(
        "/ask_gpt4/",
        json={"user_input": query_params["user_input"], "model": model},
    )

    assert response.status_code == 200
    json_response = response.json()

    # Check if the response contains a valid answer
    assert "response" in json_response or "error" in json_response

    # If there's an error, check if it's a known error
    if "error" in json_response:
        assert json_response["error"] in [
            "ChatGPT response does not contain text attribute.",
            # Add other known errors here
        ]
    else:
        assert json_response["response"] == expected_output


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code, detail, expected_result", [
    (404, "Not Found", {"detail": "Not Found", "status_code": 404}),
    (500, "Internal Server Error", {"detail": "Internal Server Error", "status_code": 500}),
    (401, "Unauthorized", {"detail": "Unauthorized", "status_code": 401}),
])
async def test_http_exception_handler(status_code: int, detail: Union[str, dict], expected_result: Any) -> None:
    """
    Function to test http exception handler
    :param status_code: int ,status code e.g. 400, 404 etc.
    :param detail: str or Dict , detail message
    :param expected_result:
    :return: None
    """
    exc = HTTPException(status_code=status_code, detail=detail)
    result = await http_exception_handler(exc)
    assert result == expected_result

