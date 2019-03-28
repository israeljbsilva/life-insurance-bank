from django.db.utils import DatabaseError
from django.utils.translation import ugettext
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """ Overriding Django rest framework's custom exception """
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:

        if isinstance(exc, (exceptions.NotAuthenticated, exceptions.PermissionDenied)):
            return response

        if not isinstance(exc, exceptions.APIException):
            response.data['status_code'] = response.status_code

    # Catching database error
    if exc and isinstance(exc, DatabaseError):
        raise Exception(debug_info=ugettext('Database error'))
    if exc and isinstance(exc, AssertionError):
        return Response({'message': str(exc), 'data': None},
                        status=HTTP_400_BAD_REQUEST)
    return response


class RequestUtils:

    @classmethod
    def is_admin_or_api_docs(cls, request):
        return True if cls.is_api_documentation(request) or cls.is_admin_module(request) else False

    @classmethod
    def is_api_documentation(cls, request):
        return True if '/docs' in request.path else False

    @classmethod
    def is_admin_module(cls, request):
        return True if '/admin/' in request.path else False
