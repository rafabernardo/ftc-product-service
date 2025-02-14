import abc

from db.mongodb.interfaces.base import BaseRepositoryInterface
from models.user import User


class UserRepositoryInterface(BaseRepositoryInterface[User]):
    @abc.abstractmethod
    def add(self, user: User) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def exists_by_cpf(self, cpf: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_cpf(self, cpf: str) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def list_entities(
        self,
    ) -> list[User]:
        raise NotImplementedError
