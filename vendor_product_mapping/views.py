from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import VendorProductMapping
from .serializers import VendorProductMappingSerializer
from core.utils import get_object_or_404_response


class VendorProductMappingListView(APIView):
    @swagger_auto_schema(
        operation_description="List vendor-product mappings. Filter by vendor_id or product_id.",
        manual_parameters=[
            openapi.Parameter('vendor_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('product_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('is_active', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: VendorProductMappingSerializer(many=True)}
    )
    def get(self, request):
        qs = VendorProductMapping.objects.all()
        if vendor_id := request.query_params.get('vendor_id'):
            qs = qs.filter(vendor_id=vendor_id)
        if product_id := request.query_params.get('product_id'):
            qs = qs.filter(product_id=product_id)
        if (is_active := request.query_params.get('is_active')) is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')
        serializer = VendorProductMappingSerializer(qs, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a vendor-product mapping.",
        request_body=VendorProductMappingSerializer,
        responses={201: VendorProductMappingSerializer, 400: "Validation Error"}
    )
    def post(self, request):
        serializer = VendorProductMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorProductMappingDetailView(APIView):
    @swagger_auto_schema(responses={200: VendorProductMappingSerializer, 404: "Not Found"})
    def get(self, request, pk):
        obj, err = get_object_or_404_response(VendorProductMapping, pk=pk)
        if err: return err
        return Response(VendorProductMappingSerializer(obj).data)

    @swagger_auto_schema(request_body=VendorProductMappingSerializer, responses={200: VendorProductMappingSerializer, 400: "Validation Error", 404: "Not Found"})
    def put(self, request, pk):
        obj, err = get_object_or_404_response(VendorProductMapping, pk=pk)
        if err: return err
        serializer = VendorProductMappingSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=VendorProductMappingSerializer, responses={200: VendorProductMappingSerializer, 400: "Validation Error", 404: "Not Found"})
    def patch(self, request, pk):
        obj, err = get_object_or_404_response(VendorProductMapping, pk=pk)
        if err: return err
        serializer = VendorProductMappingSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: "Deactivated", 404: "Not Found"})
    def delete(self, request, pk):
        obj, err = get_object_or_404_response(VendorProductMapping, pk=pk)
        if err: return err
        obj.is_active = False
        obj.save()
        return Response({"message": "Mapping deactivated."})
