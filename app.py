import openai
import os
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
        # The model used is not gpt4 to use gpt4 as a model a different API has to be used and
        # in specific the openai.ChatCompletion.create(.....)
        response = openai.Completion.create(
                    engine=model,
                    prompt=query_params.user_input,
                    max_tokens=1000,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )
        # response = openai.ChatCompletion.create(
        #     model=model,
        #     messages=[{"role": "system", "content": "You are a helpful assistant."},
        #         {"role": "user", "content": query_params.user_input}],
        #     max_tokens=1000,
        #     n=1,
        #     stop=None,
        #     temperature=0.5,
        # )

        if len(response.choices) > 0 and hasattr(response.choices[0], "text"):
            answer = response.choices[0].text.strip()
            return {"response": answer}
        else:
            return {"error": "ChatGPT response does not contain text attribute."}

    except Exception as e:
        return {"error": str(e)}

    except Exception as e:
        return {"error": str(e)}

# @app.post("/ask_gpt4/")
# async def ask_gpt4(query_params: QueryModel, model: Optional[str] = "text-davinci-003"):
#     try:
#         # Call the OpenAI API
#         response = openai.Completion.create(
#             engine=model,
#             prompt=query_params.user_input,
#             max_tokens=1000,
#             n=1,
#             stop=None,
#             temperature=0.5,
#         )
#
#         if len(response.choices) > 0 and hasattr(response.choices[0], "text"):
#             answer = response.choices[0].text.strip()
#             return {"response": answer}
#         else:
#             return {"error": "ChatGPT response does not contain text attribute."}
#
#     except Exception as e:
#         return {"error": str(e)}
#
#     except Exception as e:
#         return {"error": str(e)}
