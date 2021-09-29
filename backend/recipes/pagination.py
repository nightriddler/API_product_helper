from rest_framework.pagination import PageNumberPagination


class CustomRecipePagination(PageNumberPagination):
    page_size_query_param = 'limit'
