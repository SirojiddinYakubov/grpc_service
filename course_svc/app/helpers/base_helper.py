import datetime

from google.protobuf.timestamp_pb2 import (
    Timestamp
)


class BaseHelper:
    @classmethod
    async def get_async_attr_or_none(cls, obj, attr):
        if not hasattr(obj, attr) or not getattr(obj, attr):
            return None
        return await getattr(obj, attr)

    @classmethod
    def get_timestamp_or_none(cls, obj, attr):
        if not hasattr(obj, attr) or not getattr(obj, attr):
            return None
        if not isinstance(getattr(obj, attr), datetime.datetime) or not isinstance(getattr(obj, attr), datetime.date):
            return None
        return Timestamp(seconds=int(getattr(obj, attr).timestamp()))




