from .models import Post, Company, Tag
from .serializers import PostSerializer, CompanySerializer, TagSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PeriodFilterBackend, StatusFilterBackend
from rest_framework import pagination
from core.customs import StandardResultsSetPagination


class CompaniesView(ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['id', 'name', 'created_at']
    pagination_class = StandardResultsSetPagination


class PostsView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [StatusFilterBackend, PeriodFilterBackend, DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    search_fields = ['is_featured', 'location', 'type', 'position', 'title', 'tags']
    ordering_fields = ['pub_date', 'created_at']
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['category', 'is_finish']


class TagsView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    pagination_class = StandardResultsSetPagination


class FindLocationAction(APIView):
    def get(self, request):
        locations = Post.objects.all().distinct('location')

        data = {}

        for location in locations:
            data[location.id] = location.location

        return Response(data)

        return queryset
