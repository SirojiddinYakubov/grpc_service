import logging
from datetime import datetime, date
from typing import Union


class BaseHelper:
    @classmethod
    def make_error_response(cls, model, e):
        logging.error(e)
        if len(e.args) == 2:
            status_code, message = e.args
        else:
            status_code, message = 500, "Internal server error"
        response = model(
            error_payload=message,
            status_code=status_code
        )
        return response

    @classmethod
    def make_response(cls, model, obj, fields, other=None):
        return model(**{f: getattr(obj, f) for f in fields}, **other if other else {})

    @classmethod
    def convert_to_timestamp(cls, value: Union[datetime, date]) -> int:
        return int(value.strftime("%s"))