from fastapi import Response
from fastapi.responses import JSONResponse


class ErrorMessage:
    status_code: int
    message_code: str
    message_description: str

    @classmethod
    def to_response(cls) -> Response:
        return JSONResponse(
            status_code=cls.status_code,
            content=cls.to_content(),
        )

    @classmethod
    def to_content(cls) -> dict:
        return {
            'code': cls.message_code,
            'message': cls.message_description,
        }


class InternalServerErrorMessage(ErrorMessage):
    status_code = 500
    message_code = 'INTERNAL_SERVER_ERROR'
    message_description = 'Внутренняя ошибка'
