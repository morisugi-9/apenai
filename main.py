import openai
import os
from fastapi import FastAPI, Form, Request
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

chat_log = [{'role': 'system', 'content': 'You are a Python tutor AI, completely dedicated to teach users learn '
                                          'Python from scratch.'}]

# openai.api_key = os.getenv("OPENAI_API_KEY")

chat_responses = []

image_log = []


@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})


@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, user_input: Annotated[str, Form()]):
    chat_log.append({'role': 'user', 'content': user_input})
    chat_responses.append(user_input)
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=chat_log,
        temperature=0.6
    )
    bot_response = response['choices'][0]['message']['content']
    chat_log.append({'role': 'assistant', 'content': bot_response})
    chat_responses.append(bot_response)
    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})


@app.get("/image", response_class=HTMLResponse)
async def image_page(request: Request):
    return templates.TemplateResponse("image.html", {"request": request})


@app.post("/image", response_class=HTMLResponse)
async def image_page2(request: Request, user_input: Annotated[str, Form()]):
    image_log.append(user_input)
    response = openai.Image.create(
        prompt=user_input,
        n=1,
        size="256x256"
    )

    image_url = response['data'][0]['url']
    return templates.TemplateResponse("image.html", {"request": request, "image_url": image_url})

# while True:
#     user_input = input()
#     if user_input.lower() == 'stop':
#         break
#
#     chat_log.append({'role': 'user', 'content': user_input})
#
#     response = openai.ChatCompletion.create(
#         model='gpt-3.5-turbo',
#         # messages=[{
#         #     'role': 'system',
#         #     'content': 'You are a helpful assistant'
#         # }, {
#         #     'role': 'user',
#         #     'content': 'Write me a 3 paragraph bio'
#         # }],
#         messages=chat_log,
#         temperature=0.6
#     )
#
#     bot_response = response['choices'][0]['message']['content']
#     chat_log.append({'role': 'assistant', 'content': bot_response})
#     print(bot_response)
