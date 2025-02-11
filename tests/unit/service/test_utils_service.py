from datetime import UTC, datetime, timedelta

from freezegun import freeze_time

from services.utils import clean_cpf_to_db, get_seconds_diff


def test_clean_cpf_to_db():
    assert clean_cpf_to_db("123.456.789-00") == "12345678900"
    assert clean_cpf_to_db("111.222.333-44") == "11122233344"
    assert clean_cpf_to_db("000.000.000-00") == "00000000000"


def test_get_seconds_diff():
    with freeze_time("2023-10-01 12:00:00"):
        frozen_now = datetime.now(tz=UTC)

        dt1 = frozen_now
        assert get_seconds_diff(dt1) == 0.0  # No difference in time

        dt2 = frozen_now - timedelta(seconds=10)  # Subtrac
        assert get_seconds_diff(dt2) == 10.0  # 10 seconds difference
