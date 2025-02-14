from unittest.mock import MagicMock

from models.user import User
from repositories.user_repository import UserMongoRepository


def test_get_users(mock_mongo_collection):
    # Mock data
    mock_users = [
        {
            "_id": "67a77edeaf970c68f41cc3d3",
            "name": "Rafaela",
            "email": "email@email.com",
            "cpf": "44713529036",
            "created_at": "2025-02-08T12:57:18.267Z",
            "updated_at": "2025-02-08T12:57:18.267Z",
        }
    ]

    # Create the chain of mocks

    mock_mongo_collection.find.return_value = mock_users

    mock_db = MagicMock()
    mock_db.__getitem__.return_value = (
        mock_mongo_collection  # Simulate db["collection_name"]
    )

    repo = UserMongoRepository(database=mock_db)

    result = repo.list_entities()

    assert result is not None
    assert len(result) == 1
    mock_mongo_collection.find.assert_called_once()
    assert isinstance(result[0], User)
