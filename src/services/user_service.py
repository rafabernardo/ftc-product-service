from core.exceptions.commons_exceptions import NoDocumentsFoundException
from core.exceptions.user_exceptions import (
    UserAlreadyExistsError,
    UserInvalidFormatDataError,
)
from core.validators.user import validate_cpf, validate_email
from db.mongodb.interfaces.user import UserRepositoryInterface
from models.user import User
from services.utils import clean_cpf_to_db


class UserService:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def register_user(self, user: User) -> User:
        valid_email = validate_email(user.email)
        valid_cpf = validate_cpf(user.cpf)

        if not valid_email:
            raise UserInvalidFormatDataError("Invalid email format")
        if user.cpf:
            if not valid_cpf:
                raise UserInvalidFormatDataError("Invalid CPF format")
            if self.repository.exists_by_cpf(user.cpf):
                raise UserAlreadyExistsError(
                    "A user with this CPF already exists"
                )

            user.cpf = clean_cpf_to_db(user.cpf)

        return self.repository.add(user)

    def list_users(self) -> list[User]:
        paginated_orders = self.repository.list_entities()
        return paginated_orders

    def get_user_by_cpf(self, cpf: str) -> User:
        valid_cpf = validate_cpf(cpf)
        if not valid_cpf:
            raise UserInvalidFormatDataError("Invalid CPF format")

        clean_cpf = clean_cpf_to_db(cpf)
        return self.repository.get_by_cpf(clean_cpf)

    def get_user_by_id(self, user_id: str) -> User | None:
        user = self.repository.get_by_id(entity_id=user_id)
        return user

    def delete_user(self, user_id: str) -> bool:
        user_exists = self.repository.exists_by_id(user_id)
        if not user_exists:
            raise NoDocumentsFoundException()

        return self.repository.delete_entity(user_id)

    def identify_user(self, user_id: str, cpf: str) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NoDocumentsFoundException()

        if user.cpf is not None:
            raise UserAlreadyExistsError("User already has a CPF")

        valid_cpf = validate_cpf(cpf)
        if valid_cpf:
            clean_cpf = clean_cpf_to_db(cpf)
            return self.repository.update_entity(user_id, cpf=clean_cpf)

        raise UserInvalidFormatDataError("Invalid CPF format")
