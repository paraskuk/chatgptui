import pytest
from fastapi.testclient import TestClient
from app import ask_gpt4, app

client = TestClient(app)


@pytest.mark.parametrize("query_params, model, expected_output", [
    (
        {"user_input": "What is the capital of France?Please answer with one word only"},
        "text-davinci-003",
        "Paris."
    ),
    (
        {"user_input": "Which is the capital of UK? Please answer with one word only"},
        "text-davinci-003",
        "London."
    ),
    # Add more test cases here
])
def test_ask_gpt4(query_params, model, expected_output):
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
