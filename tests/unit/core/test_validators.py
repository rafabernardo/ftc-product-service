from src.core.validators.user import validate_cpf, validate_email


def test_validate_cpf():
    assert validate_cpf(None) is False
    assert validate_cpf("") is False
    assert validate_cpf("123456789") is False
    assert validate_cpf("306.922.380-00") is True
    assert validate_cpf("30692238000") is True  # Valid CPF
    assert validate_cpf("123456789097") is False  # Invalid CPF


def test_validate_email():
    assert validate_email(None) is False
    assert validate_email("") is False
    assert validate_email("plainaddress") is False
    assert validate_email("@missingusername.com") is False
    assert validate_email("username@.com") is False
    assert validate_email("username@domain.com") is True
    assert validate_email("user.name@domain.com") is True
    assert validate_email("user-name@domain.com") is True
    assert validate_email("user_name@domain.com") is True
    assert validate_email("username@sub.domain.com") is True
