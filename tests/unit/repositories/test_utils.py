from api.v1.models.page import PageV1Response
from src.repositories.utils import clean_up_dict, get_pagination_info


def test_clean_up_dict_removes_none_values():
    data = {"a": 1, "b": None, "c": 3}
    expected = {"a": 1, "c": 3}
    assert clean_up_dict(data) == expected


def test_clean_up_dict_keeps_non_none_values():
    data = {"a": 1, "b": 2, "c": 3}
    expected = {"a": 1, "b": 2, "c": 3}
    assert clean_up_dict(data) == expected


def test_clean_up_dict_empty_dict():
    data = {}
    expected = {}
    assert clean_up_dict(data) == expected


def test_clean_up_dict_all_none_values():
    data = {"a": None, "b": None, "c": None}
    expected = {}
    assert clean_up_dict(data) == expected


def test_clean_up_dict_mixed_values():
    data = {"a": 1, "b": None, "c": 3, "d": None, "e": 5}
    expected = {"a": 1, "c": 3, "e": 5}
    assert clean_up_dict(data) == expected


def test_get_pagination_info():
    total_results = 50
    page = 2
    page_size = 10
    expected = PageV1Response(
        total_results=total_results,
        page=page,
        page_size=page_size,
        total_pages=5,
        has_next=True,
        has_previous=True,
    )
    assert get_pagination_info(total_results, page, page_size) == expected


def test_get_pagination_info_first_page():
    total_results = 50
    page = 1
    page_size = 10
    expected = PageV1Response(
        total_results=total_results,
        page=page,
        page_size=page_size,
        total_pages=5,
        has_next=True,
        has_previous=False,
    )
    assert get_pagination_info(total_results, page, page_size) == expected


def test_get_pagination_info_last_page():
    total_results = 50
    page = 5
    page_size = 10
    expected = PageV1Response(
        total_results=total_results,
        page=page,
        page_size=page_size,
        total_pages=5,
        has_next=False,
        has_previous=True,
    )
    assert get_pagination_info(total_results, page, page_size) == expected


def test_get_pagination_info_single_page():
    total_results = 5
    page = 1
    page_size = 10
    expected = PageV1Response(
        total_results=total_results,
        page=page,
        page_size=page_size,
        total_pages=1,
        has_next=False,
        has_previous=False,
    )
    assert get_pagination_info(total_results, page, page_size) == expected
