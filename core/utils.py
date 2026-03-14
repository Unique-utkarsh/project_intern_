from rest_framework.response import Response
from rest_framework import status


def get_object_or_404_response(model, **kwargs):
    """Utility to fetch object or return 404 response."""
    try:
        return model.objects.get(**kwargs), None
    except model.DoesNotExist:
        return None, Response(
            {"error": f"{model.__name__} not found."},
            status=status.HTTP_404_NOT_FOUND
        )
