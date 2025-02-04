import copy
from datetime import datetime


def replace_id_key(document: dict):
    data = copy.deepcopy(document)
    if "_id" in data:
        data["id"] = str(data.pop("_id"))
    return data


def prepare_document_to_db(
    document: dict, pop_id: bool = True, skip_created_at: bool = False
):
    data = copy.deepcopy(document)
    now = datetime.now()

    if pop_id:
        data.pop("id", None)
    data["updated_at"] = now
    if data.get("created_at") is None and not skip_created_at:
        data["created_at"] = now
    return data


def clean_up_dict(data: dict) -> dict:
    data_copy = copy.deepcopy(data)
    cleaned_data = {k: v for k, v in data_copy.items() if v is not None}
    return cleaned_data
