import random
import json

from pprint import pprint

from locust import HttpUser, task
from janaushadi.settings import SERVER_URL

class UserTests(HttpUser):
    @task
    def create_order(self):
        token = "B9ftk4xbm6gvrxITIN28xOw0Wp7XXW"
        # token = "jT5ISC5p0IXDN7DDXOPq2TU8oO1zSl"
        
        user_id_kr = [
            {"id": 8, "shop_id": 7},
            {"id": 10, "shop_id": 9},
            {"id": 11, "shop_id": 10},
            {"id": 12, "shop_id": 11},
            {"id": 4, "shop_id": 4},
            {"id": 14, "shop_id": 13},
            {"id": 17, "shop_id": 16},
            {"id": 13, "shop_id": 12},
            {"id": 3, "shop_id": 1},
            {"id": 15, "shop_id": 14},
        ]

        user_id_kl = [
            {"id": 7, "shop_id": 6},
            {"id": 16, "shop_id": 15},
        ]

        random_choices_kr = random.choices(user_id_kr, k=1)
        random_choices_kl = random.choices(user_id_kl, k=1)

        data_kr = [
            {
                "commodityId": 3488,
                "batches": [
                {
                    "id": 7588,
                    "qty": 10,
                }
                ]
            },
            {
                "commodityId": 3406,
                "batches": [
                {
                    "id": 7396,
                    "qty": 10,
                }
                ]
            },
            {
                "commodityId": 3719,
                "batches": [
                {
                    "id": 8252,
                    "qty": 5,
                }
                ]
            },
            {
                "commodityId": 3435,
                "batches": [
                {
                    "id": 8184,
                    "qty": 1,
                }
                ]
            },
            {
                "commodityId": 3247,
                "batches": [
                {
                    "id": 7109,
                    "qty": 1,
                }
                ]
            },
            {
                "commodityId": 3242,
                "batches": [
                {
                    "id": 7177,
                    "qty": 3,
                }
                ]
            },
            {
                "commodityId": 3324,
                "batches": [
                {
                    "id": 7238,
                    "qty": 10,
                }
                ]
            }
        ]

        random_kr = random.randint(1,8)
        data_obj_kr = {
            "cartObj":{
                "items": random.choices(data_kr, k=random_kr),
            },
            "retailerId": random_choices_kr[0]['id'],
            "retailerShopId": random_choices_kr[0]['shop_id']
        }

        data_kl = [
            {
                "commodityId": 4261,
                "batches": [
                    {
                        "id": 9227,
                        "qty": 10,
                    }
                ]
            },
            {
                "commodityId": 4069,
                "batches": [
                    {
                        "id": 8892,
                        "qty": 10,
                    }
                ]
            },
            {
                "commodityId": 4421,
                "batches": [
                    {
                        "id": 9475,
                        "qty": 2,
                    }
                ]
            },
            {
                "commodityId": 4167,
                "batches": [
                    {
                        "id": 9061,
                        "qty": 1,
                    }
                ]
            },
            {
                "commodityId": 4040,
                "batches": [
                    {
                        "id": 8844,
                        "qty": 10,
                    }
                ]
            },
            {
                "commodityId": 4042,
                "batches": [
                    {
                        "id": 8847,
                        "qty": 10,
                    }
                ]
            },
            {
                "commodityId": 4191,
                "batches": [
                    {
                        "id": 9107,
                        "qty": 10,
                    }
                ]
            },
            {
                "commodityId": 4193,
                "batches": [
                    {
                        "id": 9109,
                        "qty": 1,
                    }
                ]
            }
        ]

        random_kl = random.randint(1,8)
        data_obj_kl = {
            "cartObj":{
                "items": random.choices(data_kl, k=random_kl)
            },
            "retailerId": random_choices_kl[0]['id'],
            "retailerShopId": random_choices_kl[0]['shop_id']
        }

        data_joint = [data_obj_kl, data_obj_kr]
        data = random.choices(data_joint, k=1)
        pprint(data[0])

        with self.client.post(
            url=f"{SERVER_URL}/api/order/confirm-retailer-order",
            headers={"authorization": f"Bearer {token}", "Content-Type": "application/json"},
            name = f"{SERVER_URL}/api/order/confirm-retailer-order",
            data=json.dumps(data[0])
        ) as respose:
            print(respose.status, respose.status_text)


