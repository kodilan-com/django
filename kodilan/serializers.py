from .models import Post, Company, Tag
from rest_framework import serializers


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'slug', 'logo', 'www', 'twitter', 'linkedin']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'slug']


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    company = CompanySerializer()

    class Meta:
        model = Post
        fields = ['slug', 'position', 'description', 'apply_url', 'apply_email', 'location', 'type', 'status',
                  'is_featured', 'pub_date', 'post_url', 'company', 'tags']
