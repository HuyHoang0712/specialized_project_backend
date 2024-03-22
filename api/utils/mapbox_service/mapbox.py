import math
import requests

MAP_BOX_API = "https://api.mapbox.com/directions-matrix/v1/mapbox/driving/"
MAP_BOX_ACCESS_TOKEN = "pk.eyJ1IjoidnV2aWV0aHVuZyIsImEiOiJjbHR2YXhjcmQxZmRkMm5vYWxkdjdjYWphIn0.2ZI2ANcvhekAUGxMkX-aew"


def create_distance_duration_matrix(set_of_location, active_vehicles):
    distance_matrix = []
    time_matrix = []
    time_windows = []
    api_url = (
            MAP_BOX_API + set_of_location
    )
    params = {
        "access_token": MAP_BOX_ACCESS_TOKEN,
        "annotations": "duration,distance",  # Get duration matrix and distance matrix
    }
    response = requests.get(api_url, params=params)
    response = response.json()

    for i in response["distances"]:
        res = []
        for x in i:
            res.append(math.ceil(x))
        distance_matrix.append(res)
    # DISTANCE_MATRIX = response["distances"]

    for i in response["durations"]:
        res = []
        for x in i:
            res.append(math.ceil(x / 60))
        time_matrix.append(res)
    # TIME_MATRIX = response["durations"]

    # print("Distance matrix: ", distance_matrix)
    # print("Time Matrix: ", time_matrix)
    # print("-----------------------------")

    return distance_matrix, time_matrix

# def get_position_by_address(address):
#     api_url =
