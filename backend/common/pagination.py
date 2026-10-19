from rest_framework.pagination import PageNumberPagination


class SentriPagination(PageNumberPagination):
    page_size = 0
    page_size_query_param = "page"
    max_page_size = 1
