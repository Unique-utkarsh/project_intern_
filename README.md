# Django REST Framework — Modular Entity & Mapping System

A fully modular Django backend for managing **Vendors, Products, Courses, Certifications**, and their hierarchical mappings. Built using **APIView only**, with **drf-yasg** documentation.

## Tech Stack

- Python 3.x
- Django
- Django REST Framework
- drf-yasg (Swagger / ReDoc)
- SQLite (default, swappable)

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <project-folder>
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      
```

### 3. Install dependencies

```bash
pip install django djangorestframework drf-yasg
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate

### 6. Create a superuser 

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver

## API Documentation

Once running, visit:

| URL | Description |
| `http://localhost:8000/swagger/` | Swagger UI |
| `http://localhost:8000/redoc/` | ReDoc |
| `http://localhost:8000/swagger.json` | Raw OpenAPI schema |
| `http://localhost:8000/admin/` | Django Admin |


## API Endpoints

| Method | URL | Description |
| GET | `/api/vendors/` | List all vendors |
| POST | `/api/vendors/` | Create a vendor |
| GET | `/api/vendors/<id>/` | Retrieve vendor |
| PUT | `/api/vendors/<id>/` | Full update |
| PATCH | `/api/vendors/<id>/` | Partial update |
| DELETE | `/api/vendors/<id>/` | Soft delete (is_active=False) |

Same pattern for `/api/products/`, `/api/courses/`, `/api/certifications/`


| Method | URL | Description |
| GET | `/api/vendor-product-mappings/` | List |
| POST | `/api/vendor-product-mappings/` | Create |
| GET/PUT/PATCH/DELETE | `/api/vendor-product-mappings/<id>/` | Detail |

Same pattern for `/api/product-course-mappings/` and `/api/course-certification-mappings/`

### Query Parametersd

```
GET /api/vendors/?is_active=true
GET /api/vendor-product-mappings/?vendor_id=1
GET /api/vendor-product-mappings/?product_id=2
GET /api/product-course-mappings/?product_id=1
GET /api/product-course-mappings/?course_id=2
GET /api/course-certification-mappings/?course_id=1
GET /api/course-certification-mappings/?certification_id=2

## Sample API Usage

### Create a Vendor

```bash
curl -X POST http://localhost:8000/api/vendors/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Acme Corp", "code": "ACM001", "description": "Tech company"}'

### Create a Vendor-Product Mapping

```bash
curl -X POST http://localhost:8000/api/vendor-product-mappings/ \
  -H "Content-Type: application/json" \
  -d '{"vendor": 1, "product": 1, "primary_mapping": true}'

### Filter Mappings

```bash
curl http://localhost:8000/api/vendor-product-mappings/?vendor_id=1
```


# as the assignment was strict restrict i dont use any no ViewSets, GenericAPIView, mixins,

- **APIView only** — no ViewSets, GenericAPIView, mixins, or routers used anywhere
- **Modular apps** — each entity and mapping lives in its own Django app
- **Abstract base models** — `MasterModel` and `TimeStampedModel` reduce duplication
- **Soft delete** — records are deactivated, not destroyed, preserving referential integrity
 ###
 thank you hope u will select me
 ####
 