from .models import Post, Company, Tag
from rest_framework import serializers
from django.template.defaultfilters import slugify


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(required=True, max_length=190)
    slug = serializers.CharField(read_only=True)
    logo = serializers.CharField(required=True, max_length=190)
    www = serializers.URLField(required=True, max_length=190)
    twitter = serializers.CharField(required=True, max_length=190)
    linkedin = serializers.CharField(required=True, max_length=190)

    class Meta:
        model = Company
        fields = ['name', 'slug', 'logo', 'www', 'twitter', 'linkedin']


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, max_length=190)
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Tag
        fields = ['name', 'slug']


class CreatePostSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    pub_date = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    position = serializers.CharField(required=True, max_length=190)
    description = serializers.CharField(required=True, min_length=4, max_length=100000)
    apply_url = serializers.URLField(required=True, max_length=190)
    apply_email = serializers.EmailField(required=True, max_length=190)
    location = serializers.CharField(required=True, max_length=190)
    type = serializers.ChoiceField(required=True, choices=Post.TypeEnum)

    company = CompanySerializer()

    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ('slug', 'position', 'description', 'apply_url', 'apply_email', 'location', 'type', 'status',
                  'is_featured', 'pub_date', 'post_url', 'company', 'tags')

    def create(self, validated_data):

        company_serializer = validated_data['company']
        company_slug = slugify(company_serializer['name'])
        validated_data['company'] = Company.objects.create(slug=company_slug, **company_serializer)

        tags_serializer = validated_data['tags']
        del validated_data['tags']

        slug = slugify("%s-%s" % ("company", validated_data['position']))
        post = Post.objects.create(status=0, slug=slug, **validated_data)
        for item in tags_serializer:
            tags_slug = slugify(item['name'])
            tag = Tag.objects.create(slug=tags_slug, **item)
            post.tags.add(tag)
        # todo mail gönderimi yapıalcak
        return post


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    company = CompanySerializer()

    class Meta:
        model = Post
        fields = ['slug', 'position', 'description', 'apply_url', 'apply_email', 'location', 'type', 'status',
                  'is_featured', 'pub_date', 'post_url', 'company', 'tags']
