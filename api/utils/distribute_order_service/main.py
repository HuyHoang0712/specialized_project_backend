from .customSVRP import SVRPSolution
from api.models import *
from api.utils.mapbox_service.mapbox import *
import functools
<<<<<<< Updated upstream

DEPOT = "LF_VSIP_INV_F01"

=======
>>>>>>> Stashed changes

def main(customers):
    # Get the active vehicles
    active_vehicles = Vehicle.objects.filter(status=0).values()
    active_vehicles = [vehicle for vehicle in active_vehicles]
    active_vehicles.sort(reverse=True, key=lambda a: a["capacity"])
    depot = Customer.objects.filter(name=DEPOT).values()
    depot = [
        {
            "contact_name": depot[0]["name"],
            "ship_code": 0,
            "order_type": "DAILY",
            "total_tons": 0,
            "customer_id": depot[0]["id"],
            "latitude": depot[0]["latitude"],
            "longitude": depot[0]["longitude"],
        }
    ]

    # Get the customer demand base on the data of Excel file

    # Set of location to call API Matrix MapBox
    customers.sort(reverse=True, key=lambda a: a["total_tons"])
    customers = depot + customers
    set_of_location = functools.reduce(
        lambda x, y: x + y["longitude"] + "," + y["latitude"] + ";", customers, ""
    )

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
