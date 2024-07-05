from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")
if not OPENCAGE_API_KEY:
    raise ValueError("API key not set")

class Coordinates(BaseModel):
    latitude: float
    longitude: float

def get_country_code(latitude: float, longitude: float) -> str:
    url = f"https://api.opencagedata.com/geocode/v1/json?q={latitude}+{longitude}&key={OPENCAGE_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200 or not data['results']:
            raise HTTPException(status_code=response.status_code, detail=data.get('status', {}).get('message', 'Unknown error'))
        
        country_code = data['results'][0]['components'].get('country_code')
        if country_code:
            return country_code.upper()
        else:
            return "Country code not found"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get-country-code/")
async def get_country_code_endpoint(coords: Coordinates):
    try:
        country_code = get_country_code(coords.latitude, coords.longitude)
        return {"country_code": country_code}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

