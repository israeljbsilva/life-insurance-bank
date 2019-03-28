from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination


class BaseLimitOffsetPagination(LimitOffsetPagination):

    def get_paginated_response(self, data):
        return Response({'offset': self.offset, 'limit': self.limit, 'count': self.count, 'results': data})


class CompanyPagination(BaseLimitOffsetPagination):
    max_limit = default_limit = 100
