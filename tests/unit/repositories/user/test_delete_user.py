from unittest.mock import MagicMock

from pymongo.results import DeleteResult

from repositories.user_repository import UserMongoRepository


def test_delete_user_by_id_found(mock_mongo_collection):
    user_id = "67a77edeaf970c68f41cc3d3"

    mock_collection = MagicMock()
    mock_collection.delete_one.return_value = DeleteResult(
        raw_result={"n": 1}, acknowledged=True
    )

    mock_db = MagicMock()
    mock_db.__getitem__.return_value = (
        mock_collection  # Simulate db["collection_name"]
    )

    repo = UserMongoRepository(database=mock_db)

    result = repo.delete_entity(user_id)

    assert result is not None
    assert result is True


def test_delete_user_by_id_not_found(mock_mongo_collection):
    user_id = "67a77edeaf970c68f41cc3d3"

    mock_collection = MagicMock()
    mock_collection.delete_one.return_value = DeleteResult(
        raw_result={"n": 0}, acknowledged=True
    )

    mock_db = MagicMock()
    mock_db.__getitem__.return_value = (
        mock_collection  # Simulate db["collection_name"]
    )

    repo = UserMongoRepository(database=mock_db)

    result = repo.delete_entity(user_id)

    assert result is not None
    assert result is False
