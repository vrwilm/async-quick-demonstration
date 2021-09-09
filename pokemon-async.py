#!/usr/bin/env python
# coding: utf-8

# In[3]:


from asyncio import gather, run
from httpx import AsyncClient
import time
import requests
from pprint import pprint


base_url = 'https://pokeapi.co/api/v2/pokemon/{number}'


async def download(number):
    print(f'Start:{number}')
    async with AsyncClient() as client:
        response = await client.get(
            base_url.format(number=number),
            timeout=None
        )
        print(f'end: {number}')
        return number, response.json()['name']


async def coroutine(start, stop):
    return await gather(
        *[download(number) for number in range(start, stop)]
    )

def run_coroutine():
    start_time = time.time()
    result = run(coroutine(1, 25))
    end_time = time.time() - start_time
    pprint(result)
    print(f'It took {round(end_time,2)} seconds to gather pokemons information asynchronously')
    return end_time
    
def serial_requests():
    dictionary = {}
    start_time = time.time()
    for number in range(1,25):
        r = requests.get(base_url.format(number=number))
        name = r.json()['name']
        dictionary[number] = name
        print((number,name))
    pprint(dictionary)
    end_time = time.time() - start_time
    print(f'It took {round(end_time,2)} seconds to gather pokemons information serialized')
    return end_time

def compare_methods():
    async_endtime = run_coroutine()
    serial_endtime = serial_requests()
    print(f'The time difference between the async and serialized functions is {round(serial_endtime - async_endtime,2)} seconds, it was {round(serial_endtime/async_endtime,2)} times faster. Now imagine a similar scenario for larger applications, like an API receiving multiple requests at the same time.')
    print("Also scroll up and take a look at the 'end:' outputs. See how the numbers are not ordered? That is because of the nature of coroutines: whatever result comes first from our request to the pokemon api will be printed to the console first, as we don't need to wait for other tasks to finish in order to proccess other tasks.")
    
# run_coroutine()
# serial_requests()
compare_methods()
