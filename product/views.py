from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Product
from .serializers import ProductSerializer
from core.utils import get_object_or_404_response


class ProductListView(APIView):
    """List all products or create a new one."""

    @swagger_auto_schema(
        operation_description="Retrieve a list of all products. Filter by is_active using query param.",
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, description="Filter by active status", type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: ProductSerializer(many=True)}
    )
    def get(self, request):
        queryset = Product.objects.all()
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new product.",
        request_body=ProductSerializer,
        responses={201: ProductSerializer, 400: "Validation Error"}
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    """Retrieve, update, or delete a product."""

    @swagger_auto_schema(
        operation_description="Retrieve a product by ID.",
        responses={200: ProductSerializer, 404: "Not Found"}
    )
    def get(self, request, pk):
        obj, err = get_object_or_404_response(Product, pk=pk)
        if err:
            return err
        serializer = ProductSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Fully update a product by ID.",
        request_body=ProductSerializer,
        responses={200: ProductSerializer, 400: "Validation Error", 404: "Not Found"}
    )
    def put(self, request, pk):
        obj, err = get_object_or_404_response(Product, pk=pk)
        if err:
            return err
        serializer = ProductSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a product by ID.",
        request_body=ProductSerializer,
        responses={200: ProductSerializer, 400: "Validation Error", 404: "Not Found"}
    )
    def patch(self, request, pk):
        obj, err = get_object_or_404_response(Product, pk=pk)
        if err:
            return err
        serializer = ProductSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Soft-delete a product by setting is_active=False.",
        responses={200: "Deleted (soft)", 404: "Not Found"}
    )
    def delete(self, request, pk):
        obj, err = get_object_or_404_response(Product, pk=pk)
        if err:
            return err
        obj.is_active = False
        obj.save()
        return Response({"message": "Product deactivated successfully."}, status=status.HTTP_200_OK)
