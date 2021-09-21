from rest_framework import mixins, viewsets


class ListRetrievModel(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass
