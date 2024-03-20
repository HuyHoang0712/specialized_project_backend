from .customSVRP import SVRPSolution
from .test_data import CUSTOMER
from api.models import *
import requests
import math
import functools

MAP_BOX_API = "https://api.mapbox.com/directions-matrix/v1/mapbox/driving/"
MAP_BOX_ACCESS_TOKEN = "pk.eyJ1IjoidnV2aWV0aHVuZyIsImEiOiJjbHR2YXhjcmQxZmRkMm5vYWxkdjdjYWphIn0.2ZI2ANcvhekAUGxMkX-aew"
DEPOT = "LF_VSIP_INV_F01"


def create_distance_duration_matrix(set_of_location):
    distance_matrix = []
    time_matrix = []
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


def main(customers):
    # Get the active vehicles
    active_vehicles = Vehicle.objects.filter(status=0).values()
    active_vehicles = [vehicle for vehicle in active_vehicles]
    active_vehicles.sort(reverse=True, key=lambda a: a["capacity"])
    depot = Customer.objects.filter(name=DEPOT).values()
    depot = [{
        "contact_name": depot[0]["name"],
        "ship_code": 0,
        "order_type": "DAILY",
        "total_tons": 0,
        "customer_id": depot[0]["id"],
        "latitude": depot[0]["latitude"],
        "longitude": depot[0]["longitude"],
    }]
    # Get the capacity of each vehicle
    # vehicle_capacity = [vehicle["capacity"] for vehicle in active_vehicles]

    # Get the customer demand base on the data of Excel file

    # Set of location to call API Matrix MapBox
    customers.sort(reverse=True, key=lambda a: a["total_tons"])
    customers = depot + customers
    set_of_location = functools.reduce(lambda x, y: x + y["longitude"] + "," + y["latitude"] + ";", customers, "")
    # for customer in customers:
    #     customer_demands.append((customer["total_tons"], customer["customer_id"]))
    #     set_of_location += customer["longtitude"] + "," + customer["latitude"] + ";"

    set_of_location = set_of_location[:-1]  # Remove the semi-colon
    distance_matrix, time_matrix = create_distance_duration_matrix(set_of_location)
    # print(distance_matrix, time_matrix)
    time_windows = [(4, 16)] * len(customers)

    # Set up the OR-Tools routing model with necessary callbacks and constraints

    # Create an initial solution
    solution = SVRPSolution(
        active_vehicles, customers, distance_matrix, time_matrix, time_windows
    )
    solution.initialize_solution()
    routes = solution.get_solution()

    # Run the Tabu Search algorithm
    solution.tabu_search()
    # Print the best solution found

# if __name__ == "__main__":
#     main()
