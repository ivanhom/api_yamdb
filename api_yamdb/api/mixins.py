from rest_framework import mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination


class CreateListViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pagination_class = LimitOffsetPagination


class NoPutModelViewSet(viewsets.ModelViewSet):
    """Вьюсет, запрещающий метод PUT."""
    http_method_names = ('get', 'patch', 'post', 'delete')
