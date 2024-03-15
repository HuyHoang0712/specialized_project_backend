import math
import random
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

END_TIME = 960
START_TIME = 240
AVAILABLE_TIME = 480

TIME_MATRIX = [
    [0, 32, 36, 50, 32, 21, 37, 42, 32, 32, 28],
    [32, 0, 42, 62, 45, 22, 46, 49, 48, 48, 42],
    [36, 42, 0, 21, 3, 22, 5, 10, 10, 10, 12],
    [50, 62, 21, 0, 19, 43, 16, 18, 18, 18, 23],
    [32, 45, 3, 19, 0, 25, 3, 7, 12, 12, 12],
    [21, 22, 22, 43, 25, 0, 25, 28, 30, 30, 25],
    [37, 46, 5, 16, 3, 25, 0, 4, 8, 8, 12],
    [42, 49, 10, 18, 7, 28, 4, 0, 15, 15, 16],
    [32, 48, 10, 18, 10, 30, 8, 15, 0, 0, 16],
    [32, 48, 10, 18, 10, 30, 8, 15, 0, 0, 5],
    [28, 42, 12, 23, 12, 25, 12, 16, 16, 5, 0]
]

DISTANCE_MATRIX = [
    [0, 27000, 30000, 42000, 27000, 18000, 31000, 35000, 27000, 27000, 24000],
    [27000, 0, 35100, 52200, 37400, 18900, 38600, 41600, 40300, 40300, 35400],
    [30000, 35100, 0, 18000, 2900, 18900, 4500, 8700, 9100, 9100, 10700],
    [42000, 52200, 18000, 0, 15900, 36400, 13700, 15600, 15700, 15700, 19600],
    [27000, 37400, 2900, 15900, 0, 21700, 2600, 6000, 9900, 9900, 10500],
    [18000, 18900, 18900, 36400, 21700, 0, 20800, 23900, 25700, 25700, 21500],
    [31000, 38600, 4500, 13700, 2600, 20800, 0, 3800, 6800, 6800, 10100],
    [35000, 41600, 8700, 15600, 6000, 23900, 3800, 0, 12300, 12300, 13900],
    [27000, 40300, 9100, 15700, 9000, 25700, 6800, 12300, 0, 500, 13900],
    [27000, 40300, 9100, 15700, 9000, 25700, 6800, 12300, 500, 0, 4300],
    [24000, 35400, 10700, 19600, 10500, 21500, 10100, 13900, 13900, 4300, 0]
]

TIME_WINDOWS = [
    (4, 16),
    (4, 16),
    (4, 16),
    (4, 16),
    (4, 16),
    (4, 16),
    (4, 16),
    (4, 16),
    (4, 16),
    (4, 16),
    (4, 16),
]


class SVRPSolution:
    def __init__(self, num_vehicles: int, num_customers: int, vehicle_capacity: list[int],
                 customer_demands: list[(int, int)]):
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
                self.vehicle_use[vehicle_idx] += math.floor(TIME_MATRIX[0][customer[1]] * 2.2)
            elif cur_demand / vehicle_cap >= 0.9:
                self.split_deliveries[vehicle_idx][customer[1]] = cur_demand
                self.customer_demands[cur_order_idx] = (0, customer[1])
                self.vehicle_use[vehicle_idx] += math.floor(TIME_MATRIX[0][customer[1]] * 2.2)
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
            initial_solution.customer_demands[to_node][0] * 0.02)

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
        time_dimension.CumulVar(index).SetRange(time_window[0] * 60, time_window[1] * 60)
    # Add time window constraints for each vehicle start node.
    depot_idx = 0
    for vehicle_id in range(initial_solution.num_vehicles):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            initial_solution.vehicle_use[vehicle_id] + 240, TIME_WINDOWS[depot_idx][1] * 60
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
        plan_output = f"Route for vehicle {vehicle_id} - {data.vehicle_capacity[vehicle_id]} :\n"
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


def main():
    # Define the data for the SVRP
    num_vehicles = 6
    num_customers = 11
    vehicle_list = [(7500, 22), (5000, 20), (9300, 22), (9300, 22), (7000, 22), (7000, 22)]
    vehicle_capacity = [7500, 5000, 9300, 9300, 7000, 7000]
    customer_demands = [(0, 0), (10000, 1), (29000, 2), (8750, 3), (8750, 4), (5000, 5), (5000, 6), (2300, 7),
                        (2300, 8), (1900, 9), (500, 10)]

    # Create the OR-Tools routing model
    manager = pywrapcp.RoutingIndexManager(len(customer_demands), num_vehicles, 0)
    routing_model = pywrapcp.RoutingModel(manager)

    # Set up the OR-Tools routing model with necessary callbacks and constraints

    # Create an initial solution
    initial_solution = SVRPSolution(num_vehicles, num_customers, vehicle_capacity, customer_demands)
    initial_solution.initialize_solution()
    routes = initial_solution.get_solution()
    print(routes)
    # Run the Tabu Search algorithm
    best_solution = tabu_search(initial_solution)

    # Print the best solution found


if __name__ == '__main__':
    main()
