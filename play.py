# -*- coding: utf-8 -*-
# !/usr/bin/env python
import json
import re
from pprint import pprint
from typing import List

import openai

import os

import requests
from bs4 import BeautifulSoup

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.getenv("OPENAI_API_KEY")


URLS = [
    "https://www.loveandlemons.com/vegan-ramen/",
    "https://www.loveandlemons.com/mushroom-broth/",
    "https://www.loveandlemons.com/broccolini/",
    ]


def get_completion(*, prompt: str, model="gpt-3.5-turbo"):
    messages = [
        {"role": "user",
         "content": prompt}
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # The degree of randomness of
    )
    return response.choices[0].message["content"]


def get_recipe(*, url: str) -> List[str]:
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    body = soup.find('body')
    pattern = re.compile(r'^wprm-recipe-container-')
    recipe_divs = body.find_all('div', id=pattern)
    # Access the contents of the recipe_div
    recipes = [recipe_div.text.strip() for recipe_div in recipe_divs if recipe_div.text.strip()]
    return recipes


def setup_prompt(*, text: str) -> str:
    prompt = f"""
    Extract the recipe name , the ingredients and the instructions from the text delimited by triple backticks:
    ```{text}```. 
    Provide them in JSON format with the following keys: 
    the recipe name as the main key, 
    and then ingredients and instructions as the subkeys.
    """
    return prompt


if __name__ == '__main__':
    recipes = get_recipe(url=URLS[0])
    fst_recipe = recipes[0]
    prompt = setup_prompt(text=fst_recipe)
    response = get_completion(prompt=prompt)
    print(response)
    # with open('response.json', 'w') as f:
    #     json.dump(response, f, indent=4)

