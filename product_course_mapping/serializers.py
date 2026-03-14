from rest_framework import serializers
from .models import ProductCourseMapping


class ProductCourseMappingSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = ProductCourseMapping
        fields = ['id', 'product', 'product_name', 'course', 'course_name',
                  'primary_mapping', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        product = data.get('product', getattr(self.instance, 'product', None))
        course = data.get('course', getattr(self.instance, 'course', None))
        primary_mapping = data.get('primary_mapping', getattr(self.instance, 'primary_mapping', False))

        qs = ProductCourseMapping.objects.filter(product=product, course=course)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This product-course mapping already exists.")

        if primary_mapping:
            primary_qs = ProductCourseMapping.objects.filter(product=product, primary_mapping=True)
            if self.instance:
                primary_qs = primary_qs.exclude(pk=self.instance.pk)
            if primary_qs.exists():
                raise serializers.ValidationError("This product already has a primary course mapping.")

        return data
