from datetime import datetime
import random
from ...views.backend import *

today = datetime.today().strftime("%Y-%m-%d")
transportation_plan = today.replace("-", "")


class CreateOrder:
    def __init__(self, vehicles: list[any], customers: list[any]):
        self.vehicles = vehicles
        self.customers = customers

    def create_order_obj(self, split_deliveries):
        plan = TransportationPlan.objects.filter(id=transportation_plan).exists()
        if not plan:
            plan = TransportationPlan.objects.create(id=transportation_plan, date=today)
            plan_id = plan.pk
        else:
            plan = TransportationPlan.objects.get(id=transportation_plan)
            plan_id = plan.pk
        res = []
        for index, route in enumerate(split_deliveries):
            vehicle_license = self.vehicles[index]["license_plate"]
            for location in route:
                if location["split_demand"] != 0:
                    print(location["ship_code"], " ", type(location["ship_code"]))
                    order_obj = {
                        "ship_code": str(location["ship_code"]),
                        "date": today,
                        "time_in": datetime.strftime(
                            datetime.utcfromtimestamp(240 + location["time_in"]),
                            "%M:%S",
                        ),
                        "payload": location["split_demand"],
                        "pickup_point": 25,
                        "delivery_point": location["id"],
                        "vehicle": vehicle_license,
                        "plan": plan_id,
                    }
                    res.append(order_obj)
        serializer = CreateOrderSerializer(data=res, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return plan_id
