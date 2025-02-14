from unittest.mock import MagicMock

from bson import ObjectId

from repositories.order_repository import OrderMongoRepository


def test_exist_order_by_id_found():

    mock_order = {
        "id": str(ObjectId()),
    }

    mock_collection = MagicMock()
    mock_collection.count_documents.return_value = 1

    mock_db = MagicMock()
    mock_db.__getitem__.return_value = (
        mock_collection  # Simulate db["collection_name"]
    )

    repo = OrderMongoRepository(database=mock_db)

    result = repo.exists_by_id(mock_order["id"])

    assert result is not None
