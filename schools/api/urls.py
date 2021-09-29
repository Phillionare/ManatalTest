from django.urls import include, path
from rest_framework_nested import routers
from .views import SchoolViewSet, StudentViewSet

schools = routers.DefaultRouter()
schools.register(r'schools', SchoolViewSet, basename='schools')

student = routers.DefaultRouter()
student.register(r'students', StudentViewSet, basename='students')

school_router = routers.NestedSimpleRouter(schools, r'schools', lookup='school')
school_router.register(r'students', StudentViewSet, basename='students')

urlpatterns = [
    path('', include(schools.urls)),
    path('', include(student.urls)),
    path('', include(school_router.urls)),
]