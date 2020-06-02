from .models import Post, Company
from rest_framework import viewsets
from .serializers import PostSerializer, CompanySerializer
from datetime import timedelta, datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import filters
from rest_framework import pagination


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 20


class CompaniesView(ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['id', 'name', 'created_at']
    pagination_class = StandardResultsSetPagination


class FindLocationAction(APIView):
    def get(self, request):
        locations = Post.objects.all().distinct('location')

        data = {}

        for location in locations:
            data[location.id] = location.location

        return Response(data)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-pub_date')
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-pub_date')

        period = self.request.query_params.get('period')
        is_featured = self.request.query_params.get('is_featured')

        if is_featured:
            queryset = self.queryset.filter(is_featured=1)

        if period == 'daily':
            queryset = self.queryset.filter(pub_date__day=datetime.today())
        elif period == 'weekly':
            queryset = self.queryset.filter(pub_date__gt=datetime.today() - timedelta(days=7))
        else:
            queryset = self.queryset.filter(pub_date__gt=datetime.today() - timedelta(days=30))

        return queryset
