from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


class CustomException(Exception):

    default_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = '服务器出错'

    def __init__(self,
                 message=default_message,
                 code=default_code,
                 data=None,
                 status_code=default_code):
        self.code = code
        self.message = message
        self.status = status_code

        if data is not None:
            self.data = data

    def __str__(self):
        return self.message


def custom_exception_handler(exc, context):
    if isinstance(exc, CustomException):
        return Response(data=exc.data, status=exc.status)
    return exception_handler(exc, context)
