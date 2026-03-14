from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Course
from .serializers import CourseSerializer
from core.utils import get_object_or_404_response


class CourseListView(APIView):
    """List all courses or create a new one."""

    @swagger_auto_schema(
        operation_description="Retrieve a list of all courses. Filter by is_active using query param.",
        manual_parameters=[
            openapi.Parameter('is_active', openapi.IN_QUERY, description="Filter by active status", type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: CourseSerializer(many=True)}
    )
    def get(self, request):
        queryset = Course.objects.all()
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new course.",
        request_body=CourseSerializer,
        responses={201: CourseSerializer, 400: "Validation Error"}
    )
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    """Retrieve, update, or delete a course."""

    @swagger_auto_schema(
        operation_description="Retrieve a course by ID.",
        responses={200: CourseSerializer, 404: "Not Found"}
    )
    def get(self, request, pk):
        obj, err = get_object_or_404_response(Course, pk=pk)
        if err:
            return err
        serializer = CourseSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Fully update a course by ID.",
        request_body=CourseSerializer,
        responses={200: CourseSerializer, 400: "Validation Error", 404: "Not Found"}
    )
    def put(self, request, pk):
        obj, err = get_object_or_404_response(Course, pk=pk)
        if err:
            return err
        serializer = CourseSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a course by ID.",
        request_body=CourseSerializer,
        responses={200: CourseSerializer, 400: "Validation Error", 404: "Not Found"}
    )
    def patch(self, request, pk):
        obj, err = get_object_or_404_response(Course, pk=pk)
        if err:
            return err
        serializer = CourseSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Soft-delete a course by setting is_active=False.",
        responses={200: "Deleted (soft)", 404: "Not Found"}
    )
    def delete(self, request, pk):
        obj, err = get_object_or_404_response(Course, pk=pk)
        if err:
            return err
        obj.is_active = False
        obj.save()
        return Response({"message": "Course deactivated successfully."}, status=status.HTTP_200_OK)
