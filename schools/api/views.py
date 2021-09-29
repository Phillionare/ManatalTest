from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from faker import Faker

from schools.models import Student, School
from .serializers import StudentSerializer, SchoolSerializer

class ResponsePagination(PageNumberPagination):
    page_query_param = 'p'
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5

class SchoolViewSet(viewsets.ModelViewSet):
    
    serializer_class  = SchoolSerializer
    queryset    = School.objects.filter()

    def list(self, request):
        if 'search' in request.GET:
            self.queryset = self.queryset.filter(name__contains=request.GET['search'])
        if 'order' in request.GET and bool(request.GET['order']):
            if 'DESC' in request.GET or 'desc' in request.GET:
                self.queryset = self.queryset.order_by('-'+request.GET['order'])
            else:
                self.queryset = self.queryset.order_by(request.GET['order'])

        paginator = ResponsePagination()
        results = paginator.paginate_queryset(self.queryset, request)
        return paginator.get_paginated_response(self.serializer_class(results, many=True).data)
    
    def retrieve(self, request, pk=None):
        school     = get_object_or_404(self.queryset, pk=pk)
        return Response(self.serializer_class(school).data)

class StudentViewSet(viewsets.ModelViewSet):

    serializer_class    = StudentSerializer
    queryset            = Student.objects.filter()
    
    def list(self, request, school_pk=None):
        if school_pk != None:
            self.queryset = self.queryset.filter(school=school_pk)
        if 'search' in request.GET:
            self.queryset = self.queryset.filter(Q(firstName__contains=request.GET['search']) | Q(lastName__contains=request.GET['search']) )
        if 'order' in request.GET and bool(request.GET['order']):
            if 'DESC' in request.GET or 'desc' in request.GET:
                self.queryset = self.queryset.order_by('-'+request.GET['order'])
            else:
                self.queryset = self.queryset.order_by(request.GET['order'])

        paginator = ResponsePagination()
        results = paginator.paginate_queryset(self.queryset, request)
        return paginator.get_paginated_response(self.serializer_class(results, many=True).data)
    
    def create(self, request, school_pk=None, *args, **kwargs):
        data = request.data
    
        if school_pk != None:
            #Override Data if School is set
            _mutable = data._mutable
            data._mutable = True
            data['school'] = school_pk
            data._mutable = _mutable
        
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)