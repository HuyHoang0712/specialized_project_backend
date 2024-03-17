import math
import random
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from ...views.backend import *
import requests
import math

END_TIME = 960
START_TIME = 240
AVAILABLE_TIME = 480

TIME_MATRIX = []

DISTANCE_MATRIX = []

TIME_WINDOWS = []


class SVRPSolution:
    def __init__(
        self,
        num_vehicles: int,
        num_customers: int,
        vehicle_capacity: list[int],
        customer_demands: list[(int, int)],
    ):
        self.num_vehicles = num_vehicles
        self.num_customers = num_customers
        self.vehicle_capacity = vehicle_capacity
        self.customer_demands = customer_demands
        self.split_deliveries = [[0] * num_customers for _ in range(num_vehicles)]
        self.routes = [[0] for _ in range(num_vehicles)]
        self.vehicle_use = [0 for _ in range(num_vehicles)]
        self.cost = 0

    def initialize_solution(self):
        self.vehicle_capacity.sort(reverse=True)
        self.customer_demands.sort(reverse=True, key=lambda a: a[0])
        max_vehicle_capacity = max(self.vehicle_capacity)
        for customer in self.customer_demands:
            if customer[0] > max_vehicle_capacity:
                self.split_order(customer)

    def split_order(self, customer):
        cur_demand = customer[0]
        cur_order_idx = self.customer_demands.index(customer)
        for vehicle_idx in range(self.num_vehicles):
            vehicle_cap = self.vehicle_capacity[vehicle_idx]
            if cur_demand >= vehicle_cap:
                cur_demand -= vehicle_cap
                self.split_deliveries[vehicle_idx][customer[1]] = vehicle_cap
                self.vehicle_use[vehicle_idx] += math.floor(
                    TIME_MATRIX[0][customer[1]] * 2.2
                )
            elif cur_demand / vehicle_cap >= 0.9:
                self.split_deliveries[vehicle_idx][customer[1]] = cur_demand
                self.customer_demands[cur_order_idx] = (0, customer[1])
                self.vehicle_use[vehicle_idx] += math.floor(
                    TIME_MATRIX[0][customer[1]] * 2.2
                )
                return
            else:
                self.customer_demands[cur_order_idx] = (cur_demand, customer[1])
                return

    def get_solution(self):
        for vehicle_idx in range(self.num_vehicles):
            for customer_demand_idx in range(self.num_customers):
                if self.split_deliveries[vehicle_idx][customer_demand_idx] > 0:
                    self.routes[vehicle_idx].append(customer_demand_idx)
                    self.routes[vehicle_idx].append(0)
        print(self.vehicle_use)
        print(self.split_deliveries)
        print(self.customer_demands)
        return self.routes


# def generate_neighbor_solutions(current_solution):
#     # Generate neighbor solutions based on the defined moves
#     pass
#
#
def tabu_search(initial_solution):
    initial_solution.customer_demands.sort(reverse=False, key=lambda a: a[1])
    manager = pywrapcp.RoutingIndexManager(
        initial_solution.num_customers, initial_solution.num_vehicles, 0
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return math.floor(TIME_MATRIX[from_node][to_node] * 1.1) + math.floor(
            initial_solution.customer_demands[to_node][0] * 0.02
        )

    time_callback_index = routing.RegisterTransitCallback(time_callback)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return DISTANCE_MATRIX[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # # Define cost of each arc.
    # routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Time Windows constraint.
    time = "Time"
    routing.AddDimension(
        time_callback_index,
        0,  # allow waiting time
        16 * 60,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time,
    )
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(TIME_WINDOWS):
        if location_idx == 0:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(
            time_window[0] * 60, time_window[1] * 60
        )
    # Add time window constraints for each vehicle start node.
    depot_idx = 0
    for vehicle_id in range(initial_solution.num_vehicles):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            initial_solution.vehicle_use[vehicle_id] + 240,
            TIME_WINDOWS[depot_idx][1] * 60,
        )

    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return initial_solution.customer_demands[from_node][0]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        initial_solution.vehicle_capacity,  # vehicle maximum capacities
        True,  # start cumul to zero
        "Capacity",
    )
    # Instantiate route start and end times to produce feasible times.
    for i in range(initial_solution.num_vehicles):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i))
        )
        routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(routing.End(i)))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH
    )
    search_parameters.solution_limit = 150
    # search_parameters.log_search = True
    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    print_solution(initial_solution, manager, routing, solution)


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    time_dimension = routing.GetDimensionOrDie("Time")
    total_time = 0
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data.num_vehicles):
        index = routing.Start(vehicle_id)
        plan_output = (
            f"Route for vehicle {vehicle_id} - {data.vehicle_capacity[vehicle_id]} :\n"
        )
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data.customer_demands[node_index][0]
            time_var = time_dimension.CumulVar(index)
            plan_output += (
                f"{node_index}"
                f" Load({route_load})"
                f" Time({solution.Min(time_var)},{solution.Max(time_var)})"
                " -> "
            )
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        time_var = time_dimension.CumulVar(index)
        plan_output += (
            f"{manager.IndexToNode(index)} Load(0)"
            f" Time({solution.Min(time_var)},{solution.Max(time_var)})\n"
        )
        plan_output += f"Time of the route: {round((solution.Min(time_var) - 240) / 60, 2)} hours\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        plan_output += f"Load of the route: {route_load}\n"
        print(plan_output)
        total_time += solution.Min(time_var)
    print(f"Total time of all routes: {total_time}min")


def main(self, customers):
    # Get the active vehicle
    active_vehicles = Vehicle.objects.filter(status=0).values()

    # Define the data for the SVRP
    num_vehicles = len(active_vehicles)
    num_customers = len(customers)
    print(num_vehicles, num_customers)

    # Get the capacity of each vehicle
    vehicle_capacity = []
    for vehicle in active_vehicles:
        vehicle_capacity.append(vehicle["capacity"])

    # Get the customer demand base on the data of excel file
    customer_demands = []
    set_of_location = ""  # Set of location to call API Matrix MapBox
    for customer in customers:
        customer_demands.append((customer["total_tons"], customer["customer_id"]))
        set_of_location += customer["longtitude"] + "," + customer["latitude"] + ";"

    set_of_location = set_of_location[:-1]  # Remove the semi-colon

    api_url = (
        "https://api.mapbox.com/directions-matrix/v1/mapbox/driving/" + set_of_location
    )
    params = {
        "access_token": "pk.eyJ1IjoidnV2aWV0aHVuZyIsImEiOiJjbHR2YXhjcmQxZmRkMm5vYWxkdjdjYWphIn0.2ZI2ANcvhekAUGxMkX-aew",
        "annotations": "duration,distance",  # Get duration matrix and distance matrix
    }
    response = requests.get(api_url, params=params)
    response = response.json()

    global DISTANCE_MATRIX  # Meters
    global TIME_MATRIX  # Minutes
    global TIME_WINDOWS
    for i in response["distances"]:
        res = []
        for x in i:
            res.append(math.ceil(x))
        DISTANCE_MATRIX.append(res)
    # DISTANCE_MATRIX = response["distances"]

    for i in response["durations"]:
        res = []
        for x in i:
            res.append(math.ceil(x / 60))
        TIME_MATRIX.append(res)
    # TIME_MATRIX = response["durations"]

    print("Distance matrix: ", DISTANCE_MATRIX)
    print("Time Matrix: ", TIME_MATRIX)
    print("-----------------------------")
    for i in range(1, len(active_vehicles)):
        TIME_WINDOWS.append((4, 16))

    # Create the OR-Tools routing model
    manager = pywrapcp.RoutingIndexManager(len(customer_demands), num_vehicles, 0)
    routing_model = pywrapcp.RoutingModel(manager)

    # Set up the OR-Tools routing model with necessary callbacks and constraints

    # Create an initial solution
    initial_solution = SVRPSolution(
        num_vehicles, num_customers, vehicle_capacity, customer_demands
    )
    initial_solution.initialize_solution()
    routes = initial_solution.get_solution()
    print("routes:", routes)
    # Run the Tabu Search algorithm
    best_solution = tabu_search(initial_solution)

    # Print the best solution found


if __name__ == "__main__":
    main()
