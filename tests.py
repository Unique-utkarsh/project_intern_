"""
Unit tests for serializers and APIs.
Run with: python manage.py test
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from vendor.models import Vendor
from product.models import Product
from course.models import Course
from certification.models import Certification
from vendor_product_mapping.models import VendorProductMapping


# ─── Serializer Tests ─────────────────────────────────────────────────────────

class VendorSerializerTest(TestCase):
    def test_valid_vendor(self):
        from vendor.serializers import VendorSerializer
        data = {'name': 'TestVendor', 'code': 'TV001', 'description': 'Test'}
        s = VendorSerializer(data=data)
        self.assertTrue(s.is_valid(), s.errors)

    def test_duplicate_code_rejected(self):
        from vendor.serializers import VendorSerializer
        Vendor.objects.create(name='V1', code='DUP001')
        s = VendorSerializer(data={'name': 'V2', 'code': 'DUP001'})
        self.assertFalse(s.is_valid())
        self.assertIn('code', s.errors)

    def test_missing_required_fields(self):
        from vendor.serializers import VendorSerializer
        s = VendorSerializer(data={})
        self.assertFalse(s.is_valid())
        self.assertIn('name', s.errors)
        self.assertIn('code', s.errors)


class MappingSerializerTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name='V1', code='V001')
        self.product = Product.objects.create(name='P1', code='P001')

    def test_duplicate_mapping_rejected(self):
        from vendor_product_mapping.serializers import VendorProductMappingSerializer
        VendorProductMapping.objects.create(vendor=self.vendor, product=self.product)
        s = VendorProductMappingSerializer(data={'vendor': self.vendor.pk, 'product': self.product.pk})
        self.assertFalse(s.is_valid())

    def test_dual_primary_mapping_rejected(self):
        from vendor_product_mapping.serializers import VendorProductMappingSerializer
        p2 = Product.objects.create(name='P2', code='P002')
        VendorProductMapping.objects.create(vendor=self.vendor, product=self.product, primary_mapping=True)
        s = VendorProductMappingSerializer(data={'vendor': self.vendor.pk, 'product': p2.pk, 'primary_mapping': True})
        self.assertFalse(s.is_valid())


# ─── API Tests ────────────────────────────────────────────────────────────────

class VendorAPITest(APITestCase):
    def test_create_vendor(self):
        res = self.client.post('/api/vendors/', {'name': 'NewVendor', 'code': 'NV001'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], 'NewVendor')

    def test_list_vendors(self):
        Vendor.objects.create(name='V1', code='LV001')
        res = self.client.get('/api/vendors/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)

    def test_retrieve_vendor(self):
        v = Vendor.objects.create(name='V1', code='RV001')
        res = self.client.get(f'/api/vendors/{v.pk}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['code'], 'RV001')

    def test_soft_delete(self):
        v = Vendor.objects.create(name='V1', code='DV001')
        res = self.client.delete(f'/api/vendors/{v.pk}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        v.refresh_from_db()
        self.assertFalse(v.is_active)

    def test_404_on_missing(self):
        res = self.client.get('/api/vendors/9999/')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_by_is_active(self):
        Vendor.objects.create(name='Active', code='ACT01', is_active=True)
        Vendor.objects.create(name='Inactive', code='INA01', is_active=False)
        res = self.client.get('/api/vendors/?is_active=true')
        for item in res.data:
            self.assertTrue(item['is_active'])


class MappingAPITest(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name='V1', code='MV001')
        self.product = Product.objects.create(name='P1', code='MP001')

    def test_create_mapping(self):
        res = self.client.post('/api/vendor-product-mappings/', {
            'vendor': self.vendor.pk, 'product': self.product.pk
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_duplicate_mapping_rejected(self):
        VendorProductMapping.objects.create(vendor=self.vendor, product=self.product)
        res = self.client.post('/api/vendor-product-mappings/', {
            'vendor': self.vendor.pk, 'product': self.product.pk
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_by_vendor_id(self):
        VendorProductMapping.objects.create(vendor=self.vendor, product=self.product)
        res = self.client.get(f'/api/vendor-product-mappings/?vendor_id={self.vendor.pk}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)
