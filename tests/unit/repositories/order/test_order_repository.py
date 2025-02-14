import unittest

from bson import ObjectId

from models.order import OrderFilter
from repositories.order_repository import OrderMongoRepository


class TestOrderMongoRepository(unittest.TestCase):

    def test_get_order_by_id_query(self):
        order_id = "507f1f77bcf86cd799439011"
        expected_query = {"_id": ObjectId(order_id)}
        query = OrderMongoRepository.get_order_by_id_query(order_id)
        self.assertEqual(query, expected_query)

    def test_get_order_update_data(self):
        data = {"status": "shipped"}
        expected_update_data = {"$set": data}
        update_data = OrderMongoRepository.get_order_update_data(data)
        self.assertEqual(update_data, expected_update_data)

    def test_get_list_orders_query(self):
        expected_query = {}
        query = OrderMongoRepository.get_list_orders_query()
        self.assertEqual(query, expected_query)

    def test_parse_order_filter_to_query(self):
        order_filter = OrderFilter(status=["shipped", "delivered"])
        expected_query = {"status": {"$in": ["shipped", "delivered"]}}
        query = OrderMongoRepository.parse_order_filter_to_query(order_filter)
        self.assertEqual(query, expected_query)

        order_filter = OrderFilter(status=[])
        expected_query = {}
        query = OrderMongoRepository.parse_order_filter_to_query(order_filter)
        self.assertEqual(query, expected_query)

    def test_prepare_order_sort_aggregate(self):
        sort = {"status": ["shipped", "delivered"], "created_at": 1}
        expected_aggregate = [
            {
                "$addFields": {
                    "statusOrder": {
                        "$indexOfArray": [["shipped", "delivered"], "$status"]
                    }
                }
            },
            {"$sort": {"statusOrder": 1, "created_at": 1}},
        ]
        aggregate = OrderMongoRepository.prepare_order_sort_aggregate(sort)
        self.assertEqual(aggregate, expected_aggregate)
