from rest_framework import serializers
from schools.models import Student, School

from pprint import pprint

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'pk',
            'firstName',
            'lastName',
            'studentId',
            'school'
        ]
        extra_kwargs = {'firstName': {'required': False}, 'lastName': {'required': False}} 
        read_only_fields = ['pk']

    def validate_school(self,school_obj):
        if school_obj.maxStudent-1 < Student.objects.filter(school_id=school_obj.pk).count():
            raise serializers.ValidationError('Maximum number of student reached')
        return school_obj

class SchoolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = School
        fields = [
            'pk',
            'name',
            'maxStudent']
        extra_kwargs = {'name': {'required': False}, 'maxStudent': {'required': False}} 