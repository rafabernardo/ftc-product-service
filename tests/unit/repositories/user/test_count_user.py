from unittest.mock import MagicMock

from repositories.user_repository import UserMongoRepository


def test_count_user():

    mock_collection = MagicMock()
    mock_collection.count_documents.return_value = 1

    mock_db = MagicMock()
    mock_db.__getitem__.return_value = (
        mock_collection  # Simulate db["collection_name"]
    )

    repo = UserMongoRepository(database=mock_db)

    result = repo.count_entities({})

    assert result is not None
