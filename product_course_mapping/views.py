from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import ProductCourseMapping
from .serializers import ProductCourseMappingSerializer
from core.utils import get_object_or_404_response


class ProductCourseMappingListView(APIView):
    @swagger_auto_schema(
        operation_description="List product-course mappings. Filter by product_id or course_id.",
        manual_parameters=[
            openapi.Parameter('product_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('course_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('is_active', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: ProductCourseMappingSerializer(many=True)}
    )
    def get(self, request):
        qs = ProductCourseMapping.objects.all()
        if product_id := request.query_params.get('product_id'):
            qs = qs.filter(product_id=product_id)
        if course_id := request.query_params.get('course_id'):
            qs = qs.filter(course_id=course_id)
        if (is_active := request.query_params.get('is_active')) is not None:
            qs = qs.filter(is_active=is_active.lower() == 'true')
        return Response(ProductCourseMappingSerializer(qs, many=True).data)

    @swagger_auto_schema(request_body=ProductCourseMappingSerializer, responses={201: ProductCourseMappingSerializer, 400: "Validation Error"})
    def post(self, request):
        serializer = ProductCourseMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCourseMappingDetailView(APIView):
    @swagger_auto_schema(responses={200: ProductCourseMappingSerializer, 404: "Not Found"})
    def get(self, request, pk):
        obj, err = get_object_or_404_response(ProductCourseMapping, pk=pk)
        if err: return err
        return Response(ProductCourseMappingSerializer(obj).data)

    @swagger_auto_schema(request_body=ProductCourseMappingSerializer, responses={200: ProductCourseMappingSerializer, 400: "Validation Error", 404: "Not Found"})
    def put(self, request, pk):
        obj, err = get_object_or_404_response(ProductCourseMapping, pk=pk)
        if err: return err
        serializer = ProductCourseMappingSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ProductCourseMappingSerializer, responses={200: ProductCourseMappingSerializer, 400: "Validation Error", 404: "Not Found"})
    def patch(self, request, pk):
        obj, err = get_object_or_404_response(ProductCourseMapping, pk=pk)
        if err: return err
        serializer = ProductCourseMappingSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: "Deactivated", 404: "Not Found"})
    def delete(self, request, pk):
        obj, err = get_object_or_404_response(ProductCourseMapping, pk=pk)
        if err: return err
        obj.is_active = False
        obj.save()
        return Response({"message": "Mapping deactivated."})
