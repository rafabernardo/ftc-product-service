from dependency_injector import containers, providers

from db.mongodb.database import get_mongo_client, get_mongo_database
from repositories.order_repository import OrderMongoRepository
from repositories.product_repository import ProductMongoRepository
from repositories.user_repository import UserMongoRepository
from services.order_service import OrderService
from services.product_service import ProductService
from services.user_service import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.v1.orders",
            "api.v1.payments",
            "api.v1.products",
            "api.v1.users",
        ]
    )
    db = providers.Singleton(get_mongo_client)
    mongo_database = providers.Factory(get_mongo_database)

    order_repository = providers.Factory(OrderMongoRepository, mongo_database)
    order_service = providers.Factory(OrderService, order_repository)

    product_repository = providers.Factory(
        ProductMongoRepository, mongo_database
    )
    product_service = providers.Factory(ProductService, product_repository)

    user_repository = providers.Factory(UserMongoRepository, mongo_database)
    user_service = providers.Factory(UserService, user_repository)
