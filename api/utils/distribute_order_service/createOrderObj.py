from datetime import datetime
import random
from ...views.backend import *

today = datetime.today().strftime("%Y-%m-%d")


class CreateOrder:
    def __init__(self, vehicles: list[any], customers: list[any]):
        self.vehicles = vehicles
        self.customers = customers

    def create_order_obj(self, split_deliveries):
        plan = TransportationPlan.objects.create(date=today)
        plan_id = plan.pk
        res = []
        for index, route in enumerate(split_deliveries):
            vehicle_license = self.vehicles[index]["license_plate"]
            split_code = "SPLIT" + str(index)
            for location in route:
                if location["split_demand"] != 0:
                    order_obj = {
                        "id": split_code + str(location["ship_code"]),
                        "ship_code": location["ship_code"],
                        "date": today,
                        "time_in": datetime.strftime(
                            datetime.utcfromtimestamp(240 + location["time_in"]),
                            "%M:%S",
                        ),
                        "payload": location["split_demand"],
                        "pickup_point": Customer.objects.get(id=25),
                        "delivery_point": Customer.objects.get(id=location["id"]),
                        "vehicle": Vehicle.objects.get(license_plate=vehicle_license),
                        "status": 1,
                        "plan": plan,
                    }
                    res.append(order_obj)
        order_need_create = []
        for order in res:
            create_order = Order(
                id=order["id"],
                ship_code=order["ship_code"],
                date=order["date"],
                time_in=order["time_in"],
                payload=order["payload"],
                pickup_point=order["pickup_point"],
                delivery_point=order["delivery_point"],
                vehicle=order["vehicle"],
                status=order["status"],
                plan=order["plan"],
            )
            order_need_create.append(create_order)
            # serializer = OrderSerializer(data=order)
            # if serializer.is_valid():
            #     order_need_create.append(create_order)
            # else:
            #     return plan_id
        if len(order_need_create) > 0:
            objs = Order.objects.bulk_create(order_need_create)
        return plan_id

    # How to use createOrderObj function
    # order_class = CreateOrder(
    #         vehicles=self.vehicles,
    #         customers=self.customers,
    #     )
    # order_class.create_order_obj(split_deliveries=self.split_deliveries)
