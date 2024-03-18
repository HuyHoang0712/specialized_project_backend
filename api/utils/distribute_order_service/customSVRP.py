from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import functools
import math

END_TIME = 960
START_TIME = 240
AVAILABLE_TIME = 480


class SVRPSolution:
    def __init__(
            self,
            vehicle_capacity: list[int],
            customer_demands: list[(int, int)],
            distance_matrix: list[list[int]],
            time_matrix: list[list[int]],
            time_windows: list[(int, int)],
    ):
        self.num_vehicles = len(vehicle_capacity)
        self.num_customers = len(customer_demands)
        self.vehicle_capacity = vehicle_capacity
        self.customer_demands = customer_demands
        self.distance_matrix = distance_matrix
        self.time_matrix = time_matrix
        self.time_windows = time_windows
        self.split_deliveries = [[0] * self.num_customers for _ in range(self.num_vehicles)]
        self.routes = [[0] for _ in range(self.num_vehicles)]
        self.vehicle_use = [0 for _ in range(self.num_vehicles)]
        self.cost = 0

    def initialize_solution(self):
        self.vehicle_capacity.sort(reverse=True)
        self.customer_demands.sort(reverse=True, key=lambda a: a[0])
        idx_max_vehicle_capacity = 0
        max_vehicle_capacity = self.vehicle_capacity[idx_max_vehicle_capacity]
        for customer in self.customer_demands:
            if self.vehicle_use[idx_max_vehicle_capacity] > AVAILABLE_TIME:
                idx_max_vehicle_capacity += 1 if idx_max_vehicle_capacity < self.num_vehicles - 1 else 0
                max_vehicle_capacity = self.vehicle_capacity[idx_max_vehicle_capacity]

            if customer[0] > max_vehicle_capacity:
                self.split_order(customer)

    def split_order(self, customer):
        cur_demand = customer[0]
        cur_order_idx = self.customer_demands.index(customer)
        for vehicle_idx in range(self.num_vehicles):
            vehicle_cap = self.vehicle_capacity[vehicle_idx]
            if cur_demand >= vehicle_cap:
                cur_demand -= vehicle_cap
                self.split_deliveries[vehicle_idx][cur_order_idx] = vehicle_cap
                self.vehicle_use[vehicle_idx] += math.floor(
                    self.time_matrix[0][cur_order_idx] * 2.2
                )
            elif cur_demand / vehicle_cap >= 0.9:
                self.split_deliveries[vehicle_idx][cur_order_idx] = cur_demand
                self.customer_demands[cur_order_idx] = (0, cur_order_idx)
                self.vehicle_use[vehicle_idx] += math.floor(
                    self.time_matrix[0][cur_order_idx] * 2.2
                )
                return
            else:
                self.customer_demands[cur_order_idx] = (cur_demand, self.customer_demands[cur_order_idx][1])
                return

    def get_solution(self):

        for vehicle_idx, vehicle_route in enumerate(self.split_deliveries):
            self.routes[vehicle_idx] = functools.reduce(
                lambda x, y: x + [self.customer_demands[y[0]][1], 0] if y[1] > 0 else x,
                enumerate(vehicle_route), self.routes[vehicle_idx])
        print(self.vehicle_use)
        print(self.split_deliveries)
        print(self.customer_demands)
        return self.routes

    def tabu_search(self):
        self.customer_demands.sort(reverse=False, key=lambda a: a[1])
        manager = pywrapcp.RoutingIndexManager(
            self.num_customers, self.num_vehicles, 0
        )

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)

        # Create and register a transit callback.
        def time_callback(from_index, to_index):
            """Returns the travel time between the two nodes."""
            # Convert from routing variable Index to time matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return math.floor(self.time_matrix[from_node][to_node] * 1.1) + math.floor(
                self.customer_demands[to_node][0] * 0.02
            )

        time_callback_index = routing.RegisterTransitCallback(time_callback)

        # Create and register a transit callback.
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return self.distance_matrix[from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

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
        for location_idx, time_window in enumerate(self.time_windows):
            if location_idx == 0:
                continue
            index = manager.NodeToIndex(location_idx)
            time_dimension.CumulVar(index).SetRange(
                time_window[0] * 60, time_window[1] * 60
            )
        # Add time window constraints for each vehicle start node.
        depot_idx = 0
        for vehicle_id in range(self.num_vehicles):
            index = routing.Start(vehicle_id)
            time_dimension.CumulVar(index).SetRange(
                self.vehicle_use[vehicle_id] + 240,
                self.time_windows[depot_idx][1] * 60,
            )

        def demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            from_node = manager.IndexToNode(from_index)
            return self.customer_demands[from_node][0]

        demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            self.vehicle_capacity,  # vehicle maximum capacities
            True,  # start cumul to zero
            "Capacity",
        )
        # Instantiate route start and end times to produce feasible times.
        for i in range(self.num_vehicles):
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
        search_parameters.log_search = True
        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)
        if solution:
            self.print_solution(manager, routing, solution)
        else:
            print("No solution found !")


    def print_solution(self, manager, routing, solution):
        print("print_solution")
        """Prints solution on console."""
        print(f"Objective: {solution.ObjectiveValue()}")
        time_dimension = routing.GetDimensionOrDie("Time")
        total_time = 0
        total_distance = 0
        total_load = 0
        for vehicle_id in range(self.num_vehicles):
            index = routing.Start(vehicle_id)
            plan_output = (
                f"Route for vehicle {vehicle_id} - {self.vehicle_capacity[vehicle_id]} :\n"
            )
            route_distance = 0
            route_load = 0
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                route_load += self.customer_demands[node_index][0]
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
