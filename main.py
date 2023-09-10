import os

import requests

from fastapi import FastAPI
from fastapi import Request, Response

from typing import List

import json

import redis


API_KEY = '80a4796ed267b015ea14d7cecf5dde57'
URL = 'https://api.openweathermap.org/data/2.5/weather'


app = FastAPI()
rd = redis.Redis(host='redis', port=6379, db=0)

cache_lifetime = int(os.environ.get('CACHE_LIFETIME', 1000))


def get_response_from_owm(city: str) -> dict:
    try:
        cache = rd.get(city)
        if cache:
            print('with using cache')
            return json.loads(cache)
        else:
            print('without using cache')
            response = requests.get(url=URL, params={'q': city, 'appid': API_KEY})
            if response.ok:
                rd.set(city, response.text, ex=cache_lifetime)
                return response.json()
            else:
                return {'error': response.status_code}
    except redis.exceptions.ConnectionError:
        print("Redis doesn't working")
        response = requests.get(url=URL, params={'q': city, 'appid': API_KEY})
        if response.ok:
            return response.json()
        else:
            return {'error': response.status_code}


def generate_response(cities: List[str], params: List[str]):

    response = {}
    for city in cities:

        server_response = get_response_from_owm(city)
        param_dict = {}

        for param in params:
            if param == 'temperature':
                param_dict[param] = server_response['main']['temp']
            elif param == 'feels':
                param_dict[param] = server_response['main']['feels_like']
            elif param == 'wind':
                param_dict[param] = server_response['wind']
            elif param == 'visibility':
                param_dict[param] = server_response['visibility']
            elif param == 'humidity':
                param_dict[param] = server_response['main']['humidity']

            response[city] = param_dict

    return response


@app.get('/cities')
def get_response(request: Request) -> dict:

    if request.query_params.getlist('city'):
        cities = request.query_params.getlist('city')
    else:
        cities = request.query_params.getlist('cities')

    params = request.query_params.getlist('parameters')

    response = generate_response(cities, params)

    return response




