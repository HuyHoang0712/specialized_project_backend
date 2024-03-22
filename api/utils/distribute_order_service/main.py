from .customSVRP import SVRPSolution
from api.models import *
from api.utils.mapbox_service.mapbox import *





def main(customers):
    # Get the active vehicles
    active_vehicles = Vehicle.objects.filter(status=0).values()

    # Get the capacity of each vehicle
    vehicle_capacity = [vehicle["capacity"] for vehicle in active_vehicles]

    # Get the customer demand base on the data of Excel file
    customer_demands = []
    set_of_location = ""  # Set of location to call API Matrix MapBox
    for customer in customers:
        customer_demands.append((customer["total_tons"], customer["customer_id"]))
        set_of_location += customer["longtitude"] + "," + customer["latitude"] + ";"

    set_of_location = set_of_location[:-1]  # Remove the semi-colon
    distance_matrix, time_matrix = create_distance_duration_matrix(set_of_location, active_vehicles)
    time_windows = [(4, 16)] * len(customer_demands)

    # Set up the OR-Tools routing model with necessary callbacks and constraints

    # Create an initial solution
    solution = SVRPSolution(
        vehicle_capacity, customer_demands, distance_matrix, time_matrix, time_windows
    )
    solution.initialize_solution()
    routes = solution.get_solution()
    print("routes:", routes)
    # Run the Tabu Search algorithm
    solution.tabu_search()
    # Print the best solution found


# if __name__ == "__main__":
#     main()
