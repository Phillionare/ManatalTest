from django.contrib import admin

from .models import Student
from .models import School

admin.site.register(Student)
admin.site.register(School)

# Register your models here.
