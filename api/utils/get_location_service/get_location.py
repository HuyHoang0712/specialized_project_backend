import requests

GOOGLE_API = "https://maps.googleapis.com/maps/api/geocode/json"
GOOGLE_API_ACCESS_TOKEN = "AIzaSyBzAZayxcyaDFCAy_3608RgV1UJy9nX9dQ"


def get_coordinate(address):
    params = {
        "address": address,  # quote address
        "key": GOOGLE_API_ACCESS_TOKEN,
    }
    response = requests.get(GOOGLE_API, params=params)
    response = response.json()
    print(response)
    if response["status"] == "OK":
        result = {
            "coordinate": response["results"][0]["geometry"]["location"],
            "status": response["status"],
        }
    else:
        result = {
            "coordinate": "",
            "status": response["status"],
        }
    return result
