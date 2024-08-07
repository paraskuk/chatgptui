[![Python application Setup - Chat GPT](https://github.com/paraskuk/chatgptui/actions/workflows/python-app.yml/badge.svg)](https://github.com/paraskuk/chatgptui/actions/workflows/python-app.yml)
# AskGPT

AskGPT is a simple web application that uses the OpenAI API to generate responses to user queries using GPT-4 language model. 
This application is built using FastAPI for the API and JavaScript ,HTML and CSS for the frontend.

## Requirements

- Python 3.11 or higher
- OpenAI API key
- FastAPI
- JavaScript
- Redis Server
- HTML, CSS
- Chrome Browser
- Install packages as outlined in the requirements.txt file
- Get GitHub Client ID for your OAuth App
- Get GitHub Client Secret for your OAuth App
- Get Secret Session Key for your OAuth App

## Installation

1. Clone the repository
2. Install the required packages using `pip install -r requirements.txt`
3. Set the `OPEN_AI_KEY` environment variable with your OpenAI API key.
4. Setup Redis server on your machine as outlined here https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-windows/


## Usage
1. Start Redis server with `sudo service redis-server start`
2. On PyCharm Professional IDE, create a FastAPI configuration and run the application using the app.py script.
3. The above configuration needs to have the OpenAI API key as well as the GitHub keys outlined in the requirements section.
2. Navigate to `http://localhost:8000/` on your Google Chrome browser to access the application.
3. Login to GitHub using the `Login with GitHub` button.
4. Enter your query in the input field and click on the `Submit` button to generate a response.
5. Click on the Mic button to use the speech-to-text feature and get a code completion from GPT-4.

## Testing the Application with Curl
`curl -X POST http://127.0.0.1:8000/ask_gpt4/ -H "Content-Type: application/json" -d "{\"user_input\": \"Create a function that adds 2 numbers\", \"model\": \"gpt-4\"}"`

## Note

Make sure to set the `OPEN_AI_KEY` environment variable before running the application, as this is required for the OpenAI API to function properly.

## License

This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
This project is not licensed for commercial use.

## Disclaimer

This project is for demonstration of GPT capabilities and should not be used wholly or partly in 
any commercial project. 

