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


class CreatePostSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=True, min_length=4, max_length=100000)
    position = serializers.CharField(required=False, allow_blank=True, max_length=190)

    apply_url = serializers.CharField(required=False, allow_blank=True, max_length=190)
    apply_email = serializers.CharField(required=False, allow_blank=True, max_length=190)

    type = serializers.CharField(required=False, allow_blank=True, max_length=190)

    # todo diğer alanlar eklenecek

    class Meta:
        model = Post
        fields = ['slug', 'position', 'description', 'apply_url', 'apply_email', 'location', 'type', 'status',
                  'is_featured', 'pub_date', 'post_url', 'company', 'tags']

    def create(self, validated_data):
        # todo mail gönderimi yapıalcak
        post = Post.objects.create(status=0, **validated_data)
        return post


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    company = CompanySerializer()

    class Meta:
        model = Post
        fields = ['slug', 'position', 'description', 'apply_url', 'apply_email', 'location', 'type', 'status',
                  'is_featured', 'pub_date', 'post_url', 'company', 'tags']
