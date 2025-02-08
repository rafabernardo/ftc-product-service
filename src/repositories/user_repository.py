from datetime import datetime

from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.collection import Collection
from pymongo.database import Database

from db.mongodb.interfaces.user import UserRepositoryInterface
from models.user import User
from repositories.utils import prepare_document_to_db, replace_id_key


class UserMongoRepository(UserRepositoryInterface):
    def __init__(self, database: Database):
        self.database: Database = database
        self.collection: Collection = self.database["Users"]

    def add(self, user: User) -> User:
        user_data = user.model_dump()
        user_to_db = prepare_document_to_db(user_data)
        self.collection.insert_one(user_to_db)
        final_user = replace_id_key(user_to_db)

        return User(**final_user)

    def get_by_id(self, entity_id: str) -> User | None:
        query = self.get_user_by_id_query(user_id=entity_id)
        user = self.collection.find_one(query)
        if user:
            final_user = replace_id_key(user)
            return User(**final_user)
        return None

    def list_entities(
        self,
    ) -> list[User] | None:
        query = self.get_list_users_query()
        users = self.collection.find(query)
        if users:
            return [User(**replace_id_key(user)) for user in users]

        return None

    def exists_by_cpf(self, cpf: str) -> bool:
        return self.collection.count_documents({"cpf": cpf}) > 0

    def exists_by_id(self, entity_id: str) -> bool:
        query = self.get_user_by_id_query(user_id=entity_id)
        return self.collection.count_documents(query) > 0

    def get_by_cpf(self, cpf: str) -> User | None:
        query = self.get_user_by_cpf_query(cpf=cpf)
        user = self.collection.find_one(query)
        if user:
            final_user = replace_id_key(user)
            return User(**final_user)
        return None

    def delete_entity(self, entity_id: str) -> bool:
        query = self.get_user_by_id_query(user_id=entity_id)
        result = self.collection.delete_one(query)
        was_user_deleted = result.deleted_count > 0
        return was_user_deleted

    def update_entity(self, entity_id, **kwargs) -> User:
        id_query = self.get_user_by_id_query(user_id=entity_id)
        user_to_db = prepare_document_to_db(kwargs, skip_created_at=True)
        user_update_data = self.get_user_update_query(user_to_db)
        updated_user = self.collection.find_one_and_update(
            filter=id_query,
            update=user_update_data,
            return_document=ReturnDocument.AFTER,
        )

        updated_user = replace_id_key(updated_user)
        return User(**updated_user)

    def count_entities(self, filter_params: dict) -> int:
        return self.collection.count_documents(filter_params)

    @staticmethod
    def get_user_by_id_query(user_id: str) -> dict:
        query = {"_id": ObjectId(user_id)}
        return query

    @staticmethod
    def get_user_by_cpf_query(cpf: str) -> dict:
        query = {"cpf": cpf}
        return query

    @staticmethod
    def get_list_users_query() -> dict:
        query = {}
        return query

    @staticmethod
    def get_user_update_query(data: dict) -> dict:
        now = datetime.now()
        data["updated_at"] = now
        query = {"$set": data}
        return query
