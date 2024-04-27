import asyncio
import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")

async def rhyme_finder(word):
    url = f"https://rhyming.ir/api/rhyme-finder?api={API_KEY}&w={word}&sb=1&mfe=2&eq=1"
    response = await asyncio.get_event_loop().run_in_executor(None, requests.get, url)
    return response.json()

async def get_states():
    url = "https://iran-locations-api.vercel.app/api/v1/fa/states"
    response = await asyncio.get_event_loop().run_in_executor(None, requests.get, url)
    print("States API response:", response.text)
    return response.json()

async def get_cities(state_id):
    url = f"https://iran-locations-api.vercel.app/api/v1/fa/cities?state_id={state_id}"
    response = await asyncio.get_event_loop().run_in_executor(None, requests.get, url)
    print("Cities API response:", response.text)
    return response.json()

async def get_coordinates(state_name, city_name):
    print("Coordinates Started")
    states = await get_states()
    for state in states:
        if state["name"] == state_name:
            response = await get_cities(state["id"])
            cities = response["cities"]
            for city in cities:
                if city["name"] == city_name:
                    latitude = city["latitude"]
                    longitude = city["longitude"]
                    break
            else:
                print(f"Not found city {city_name}" )
                latitude = None
                longitude = None
            break
    else:
        print(f"Not found state {state_name}")
        latitude = None
        longitude = None

    print("Coordinates Ended")
    return latitude, longitude

async def main():
    word = "بابا"
    rhymes = await rhyme_finder(word)
    print(f"Rhymes for {word}: {rhymes}")
    
    state_name = "تهران"
    city_name = "تهران"
    latitude, longitude = await get_coordinates(state_name, city_name)
    if latitude is not None and longitude is not None:
        print(f"Coordinates for {city_name}, {state_name}: Latitude = {latitude}, Longitude = {longitude}")
    else:
        print("Coordinates not found.")

if __name__ == "__main__":
    asyncio.run(main())
