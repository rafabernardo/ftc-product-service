import unittest
from datetime import datetime
from unittest.mock import patch

from bson import ObjectId

from repositories.user_repository import UserMongoRepository


class TestUserMongoRepository(unittest.TestCase):

    def test_get_user_by_id_query(self):
        user_id = "507f1f77bcf86cd799439011"
        expected_query = {"_id": ObjectId(user_id)}
        result = UserMongoRepository.get_user_by_id_query(user_id)
        self.assertEqual(result, expected_query)

    def test_get_user_by_cpf_query(self):
        cpf = "12345678900"
        expected_query = {"cpf": cpf}
        result = UserMongoRepository.get_user_by_cpf_query(cpf)
        self.assertEqual(result, expected_query)

    def test_get_list_users_query(self):
        expected_query = {}
        result = UserMongoRepository.get_list_users_query()
        self.assertEqual(result, expected_query)

    @patch("repositories.user_repository.datetime")
    def test_get_user_update_query(self, mock_datetime):
        mock_now = datetime(2023, 1, 1)
        mock_datetime.now.return_value = mock_now
        data = {"name": "John Doe"}
        expected_query = {"$set": {"name": "John Doe", "updated_at": mock_now}}
        result = UserMongoRepository.get_user_update_query(data)
        self.assertEqual(result, expected_query)


if __name__ == "__main__":
    unittest.main()
