import openai
import os

from starlette.staticfiles import StaticFiles

from models.query_model import QueryModel
from typing import Optional

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

openai.api_key = os.getenv("OPEN_AI_KEY")


templates = Jinja2Templates(directory="templates")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/ask_gpt4/")
async def ask_gpt4(query_params: QueryModel, model: Optional[str] = "text-davinci-003"):
    try:
        # Call the OpenAI API
        response = openai.Completion.create(
            engine=model,
            prompt=query_params.user_input,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )

        if len(response.choices) > 0 and hasattr(response.choices[0], "text"):
            answer = response.choices[0].text.strip()
            return {"response": answer}
        else:
            return {"error": "ChatGPT response does not contain text attribute."}

    except Exception as e:
        return {"error": str(e)}

    except Exception as e:
        return {"error": str(e)}
