import math
from collections import OrderedDict

from rest_framework import pagination
from rest_framework.response import Response


class CustomPageNumber(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                    ("current", self.page.number),
                    (
                        "pages",
                        int(math.ceil(self.page.paginator.count / self.page_size)),
                    ),
                ]
            )
        )

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "count": {
                    "type": "integer",
                    "example": 123,
                },
                "next": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": "http://api.example.org/accounts/?{page_query_param}=4".format(
                        page_query_param=self.page_query_param
                    ),
                },
                "previous": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": "http://api.example.org/accounts/?{page_query_param}=2".format(
                        page_query_param=self.page_query_param
                    ),
                },
                "results": schema,
                "current": {
                    "type": "integer",
                    "example": 123,
                },
                "pages": {
                    "type": "integer",
                    "example": 123,
                },
            },
        }
