from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Vendor
from .serializers import VendorSerializer
from core.utils import get_object_or_404_response


class VendorListView(APIView):
    """List all vendors or create a new one."""

    @swagger_auto_schema(
        operation_description="Retrieve a list of all vendors. Filter by is_active using query param.",
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, description="Filter by active status", type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: VendorSerializer(many=True)}
    )
    def get(self, request):
        queryset = Vendor.objects.all()
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        serializer = VendorSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new vendor.",
        request_body=VendorSerializer,
        responses={201: VendorSerializer, 400: "Validation Error"}
    )
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDetailView(APIView):
    """Retrieve, update, or delete a vendor."""

    @swagger_auto_schema(
        operation_description="Retrieve a vendor by ID.",
        responses={200: VendorSerializer, 404: "Not Found"}
    )
    def get(self, request, pk):
        obj, err = get_object_or_404_response(Vendor, pk=pk)
        if err:
            return err
        serializer = VendorSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Fully update a vendor by ID.",
        request_body=VendorSerializer,
        responses={200: VendorSerializer, 400: "Validation Error", 404: "Not Found"}
    )
    def put(self, request, pk):
        obj, err = get_object_or_404_response(Vendor, pk=pk)
        if err:
            return err
        serializer = VendorSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a vendor by ID.",
        request_body=VendorSerializer,
        responses={200: VendorSerializer, 400: "Validation Error", 404: "Not Found"}
    )
    def patch(self, request, pk):
        obj, err = get_object_or_404_response(Vendor, pk=pk)
        if err:
            return err
        serializer = VendorSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Soft-delete a vendor by setting is_active=False.",
        responses={200: "Deleted (soft)", 404: "Not Found"}
    )
    def delete(self, request, pk):
        obj, err = get_object_or_404_response(Vendor, pk=pk)
        if err:
            return err
        obj.is_active = False
        obj.save()
        return Response({"message": "Vendor deactivated successfully."}, status=status.HTTP_200_OK)
