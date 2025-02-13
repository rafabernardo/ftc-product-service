from unittest.mock import MagicMock

from repositories.user_repository import UserMongoRepository


def test_get_user_by_id_found():
    user_id = "67a77edeaf970c68f41cc3d3"

    mock_collection = MagicMock()
    mock_collection.count_documents.return_value = 1

    mock_db = MagicMock()
    mock_db.__getitem__.return_value = (
        mock_collection  # Simulate db["collection_name"]
    )

    repo = UserMongoRepository(database=mock_db)

    result = repo.exists_by_id(user_id)

    assert result is not None
    assert result is True
