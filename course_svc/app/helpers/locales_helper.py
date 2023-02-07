from crud.locales import LocalesCRUD
from models import Locales
from .base_helper import BaseHelper
from app.grpc_generated_files.locales_types_pb2 import (
    LocalesResponse
)


class LocalesHelper(BaseHelper):
    @classmethod
    async def get_locales(cls, request, context):
        try:
            if not hasattr(request, 'locale_id'):
                raise Exception(400, "locale_id required!")

            status_code, locale_or_error = await LocalesCRUD.get(id=request.locale_id)
            if not status_code == 200:
                raise Exception(status_code, locale_or_error)

            locales_resp = await cls.make_response(Locales, locale_or_error,
                                                   ['id', 'name', 'code', 'is_main'])
            get_locales_resp = LocalesResponse(
                success_payload=locales_resp,
                status_code=status_code
            )
            return get_locales_resp
        except Exception as e:
            return cls.make_error_response(LocalesResponse, e)

