from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from geopy.geocoders import Nominatim

# Initialize FastAPI app
app = FastAPI()

# Define request model
class Coordinates(BaseModel):
    latitude: float
    longitude: float

# Function to get country code
def get_country_code(latitude: float, longitude: float) -> str:
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse((latitude, longitude), language='en')
    
    if location and location.raw.get('address', {}).get('country_code'):
        return location.raw['address']['country_code']
    else:
        return "Country code not found"

# Define endpoint to get country code
@app.post("/get-country-code/")
async def get_country_code_endpoint(coords: Coordinates):
    try:
        country_code = get_country_code(coords.latitude, coords.longitude)
        return {"country_code": country_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

