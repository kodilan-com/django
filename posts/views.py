from .models import Post, Company, Tag
from .serializers import PostSerializer, CompanySerializer, TagSerializer, ActivatePostSerializer, LocationSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PeriodFilterBackend, StatusFilterBackend


class CompaniesView(ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, ]
    search_fields = ['name']
    ordering_fields = ['id', 'name', 'created_at']


class PostsView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [StatusFilterBackend, PeriodFilterBackend, DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tags', 'type', 'position', 'location', 'is_featured']
    search_fields = ['position', 'description']
    ordering_fields = ['pub_date', 'created_at']


class PostView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"
    filter_backends = [StatusFilterBackend]


class ActivatePostView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = ActivatePostSerializer
    lookup_field = "activation_code"


class TagsView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']


class FindLocationAction(ListAPIView):
    queryset = Post.objects.all().values('location').distinct()
    filter_backends = [StatusFilterBackend]
    serializer_class = LocationSerializer
