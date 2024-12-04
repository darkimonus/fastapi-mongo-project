from bson import ObjectId
from bson.errors import InvalidId


def convert_to_mongo_id(document_id: str):
    try:
        result = ObjectId(document_id)
    except InvalidId as e:
        raise ValueError(str(e))
    else:
        return result