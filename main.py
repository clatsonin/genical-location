from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

class Coordinates(BaseModel):
    latitude: float
    longitude: float

def get_country_code(latitude: float, longitude: float) -> str:
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        location = geolocator.reverse((latitude, longitude), language='en')
    except GeocoderServiceError as e:
        raise HTTPException(status_code=500, detail=f"Geocoding service error: {str(e)}")
    if location and location.raw.get('address', {}).get('country_code'):
        return location.raw['address']['country_code']
    else:
        return "Country code not found"

@app.post("/get-country-code/")
async def get_country_code_endpoint(coords: Coordinates):
    try:
        country_code = get_country_code(coords.latitude, coords.longitude)
        return {"country_code": country_code}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
