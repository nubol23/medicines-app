from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class CustomModelViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        """
        Change the original implementation to return a different serializer
        after creating the instance
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Get default serializer class as response
        response_serializer = self.serializer_class(
            instance=serializer.instance, context=self.get_serializer_context()
        )

        headers = self.get_success_headers(serializer.data)
        # Return that instead of the original
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        """
        Change the original implementation to return a different serializer
        after updating the instance
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        # Get default serializer class as response
        response_serializer = self.serializer_class(
            instance=serializer.instance, context=self.get_serializer_context()
        )
        return Response(response_serializer.data)
