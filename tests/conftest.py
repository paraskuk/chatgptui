# conftest.py
import os
import sys
from fastapi.testclient import TestClient
import pytest
from functools import lru_cache
from fastapi import FastAPI
import httpx

# Add the path to your source code directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Create an instance of FASTAPI to use
app = FastAPI()


@lru_cache()  # Load once by using the lru_cache
@pytest.fixture(scope="module")
def test_client() -> TestClient:
    """
    Function to create a test client instance to use for testing.
    Uses a generator to potentially improve performance of a large number of tests.
    :return: a Test client object.
    """
    with TestClient(app) as client:
        yield client