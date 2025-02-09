from datetime import datetime, timedelta

import pytest

from services.utils import clean_cpf_to_db, get_seconds_diff


def test_clean_cpf_to_db():
    assert clean_cpf_to_db("123.456.789-00") == "12345678900"
    assert clean_cpf_to_db("111.222.333-44") == "11122233344"
    assert clean_cpf_to_db("000.000.000-00") == "00000000000"


def test_get_seconds_diff():
    dt = datetime.now() - timedelta(seconds=10)
    assert get_seconds_diff(dt) == pytest.approx(10, rel=1e-2)

    dt = datetime.now() - timedelta(minutes=5)
    assert get_seconds_diff(dt) == pytest.approx(300, rel=1e-2)

    dt = datetime.now() - timedelta(hours=1)
    assert get_seconds_diff(dt) == pytest.approx(3600, rel=1e-2)
