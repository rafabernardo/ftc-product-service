from unittest.mock import MagicMock

from models.user import User
from repositories.user_repository import UserMongoRepository


def test_get_user_by_id_found(mock_mongo_collection):
    user_id = "67a77edeaf970c68f41cc3d3"
    mock_product_data = {
        "_id": "67a77edeaf970c68f41cc3d3",
        "name": "Rafaela",
        "email": "email@email.com",
        "cpf": "44713529036",
        "created_at": "2025-02-08T12:57:18.267Z",
        "updated_at": "2025-02-08T12:57:18.267Z",
    }

    mock_collection = MagicMock()
    mock_collection.find_one.return_value = mock_product_data

    mock_db = MagicMock()
    mock_db.__getitem__.return_value = (
        mock_collection  # Simulate db["collection_name"]
    )

    repo = UserMongoRepository(database=mock_db)

    result = repo.get_by_id(user_id)

    assert result is not None
    assert isinstance(result, User)
    assert result.id == mock_product_data["_id"]
    assert result.name == mock_product_data["name"]
    assert result.email == mock_product_data["email"]
