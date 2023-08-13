import pickle
from copy import copy

from pydantic import BaseModel

from src.database import Base


def object_to_str(
        data: list[type[Base]] | list[type[Base]]
) -> bytes:
    dict_data = []
    for item in copy(data):
        if isinstance(item, Base):
            instance_dict = item.__dict__
            del instance_dict['_sa_instance_state']
            dict_data.append(instance_dict)
        else:
            dict_data.append(item.model_dump())

    return pickle.dumps(dict_data)


def str_to_object(
        data: bytes,
        model: type[BaseModel]
) -> list[BaseModel]:
    result = []
    json_data = pickle.loads(data)
    for item in json_data:
        result.append(model(**item))

    return result
