from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_query_param = 'pageNum'
    page_size_query_param = 'pageSize'
