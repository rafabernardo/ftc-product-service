import abc
from typing import Generic, TypeVar

T = TypeVar("T")  # Generic type for repository models


class BaseRepositoryInterface(abc.ABC, Generic[T]):
    @abc.abstractmethod
    def get_by_id(self, entity_id: str) -> T | None:
        raise NotImplementedError

    @abc.abstractmethod
    def count_entities(self, filter_params: dict) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_entity(self, entity_id: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def exists_by_id(self, entity_id: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def update_entity(self, entity_id: str, **kwargs) -> T:
        raise NotImplementedError
