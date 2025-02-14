from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.collection import Collection
from pymongo.database import Database

from db.mongodb.interfaces.order import OrderRepositoryInterface
from models.order import Order, OrderFilter, OrderItem
from repositories.utils import prepare_document_to_db, replace_id_key


class OrderMongoRepository(OrderRepositoryInterface):
    def __init__(self, database: Database):
        self.database: Database = database
        self.collection: Collection = self.database["Orders"]
        super().__init__()

    def add(self, order: Order) -> Order:
        order_data = order.model_dump()
        order_to_db = prepare_document_to_db(order_data)
        self.collection.insert_one(order_to_db)

        final_order = order_to_db
        final_order = replace_id_key(final_order)
        return Order(**final_order)

    def get_by_id(self, entity_id: str) -> Order | None:
        query = self.get_order_by_id_query(order_id=entity_id)
        order: dict = self.collection.find_one(query)
        if not order:
            return None

        order = replace_id_key(order)
        return Order(**order)

    def exists_by_id(self, entity_id: str) -> bool:
        query = self.get_order_by_id_query(order_id=entity_id)
        return self.collection.count_documents(query) > 0

    def update_entity(self, entity_id, **kwargs) -> Order:
        id_query = self.get_order_by_id_query(order_id=entity_id)
        order_to_update = prepare_document_to_db(kwargs, skip_created_at=True)
        order_update_data = self.get_order_update_data(order_to_update)
        updated_order = self.collection.find_one_and_update(
            filter=id_query,
            update=order_update_data,
            return_document=ReturnDocument.AFTER,
        )
        updated_order = replace_id_key(updated_order)
        return Order(**updated_order)

    def list_entities(
        self, filter_params: OrderFilter, page: int, page_size: int, sort: dict
    ) -> list[Order]:
        query = self.parse_order_filter_to_query(filter_params)
        skip = (page - 1) * page_size
        orders = []

        if sort:
            pipeline = self.create_list_pipeline(query, sort, skip, page_size)
            orders.extend(self.collection.aggregate(pipeline))
        else:
            orders.extend(
                self.collection.find(query).skip(skip).limit(page_size)
            )

        return [Order(**replace_id_key(order)) for order in orders]

    def count_entities(self, filter_params: OrderFilter) -> int:
        query = self.parse_order_filter_to_query(filter_params)
        return self.collection.count_documents(query)

    def delete_entity(self, entity_id: str) -> bool:
        query = self.get_order_by_id_query(order_id=entity_id)
        result = self.collection.delete_one(query)
        was_order_deleted = result.deleted_count > 0
        return was_order_deleted

    def add_order_item(self, order_id, order_item: OrderItem) -> None:
        raise NotImplementedError

    def list_order_items_by_order_id(self, order_id) -> list[OrderItem]:
        raise NotImplementedError

    @staticmethod
    def get_order_by_id_query(order_id: str) -> dict:
        query = {"_id": ObjectId(order_id)}
        return query

    @staticmethod
    def get_order_update_data(data: dict) -> dict:
        order_update_data = {"$set": data}
        return order_update_data

    @staticmethod
    def get_list_orders_query() -> dict:
        query = {}
        return query

    @staticmethod
    def parse_order_filter_to_query(order_filter: OrderFilter) -> dict:
        query = {
            **(
                {"status": {"$in": order_filter.status}}
                if order_filter.status
                else {}
            )
        }
        return query

    @staticmethod
    def prepare_order_sort_aggregate(sort: dict) -> list[dict]:
        aggregate = []
        if "status" in sort:
            aggregate.append(
                {
                    "$addFields": {
                        "statusOrder": {
                            "$indexOfArray": [sort["status"], "$status"]
                        }
                    }
                }
            )
            aggregate.append({"$sort": {"statusOrder": 1}})

        if "created_at" in sort:
            sort_stage = next(
                (item for item in aggregate if "$sort" in item), None
            )
            if sort_stage:
                sort_stage["$sort"]["created_at"] = sort["created_at"]
            else:
                aggregate.append({"$sort": {"created_at": sort["created_at"]}})

        return aggregate

    def create_list_pipeline(
        self, query: dict, sort: dict, skip: int, limit: int
    ) -> dict:
        aggregate_sort = self.prepare_order_sort_aggregate(sort)
        pipeline = [
            {"$match": query},
        ]
        pipeline.extend(aggregate_sort)
        pipeline.append({"$skip": skip})
        pipeline.append({"$limit": limit})
        return pipeline
