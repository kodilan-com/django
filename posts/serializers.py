from .models import Post, Company, Tag
from rest_framework import serializers
from django.template.defaultfilters import slugify
from kodilan.mail import send_activation
from django.db import IntegrityError
import secrets
from django.db.models import Q


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(required=True, max_length=190)
    slug = serializers.CharField(read_only=True)
    email = serializers.EmailField(required=True, max_length=190)
    logo = serializers.CharField(required=True, max_length=190)
    www = serializers.URLField(required=True, max_length=190)
    twitter = serializers.CharField(required=False, max_length=190)
    linkedin = serializers.CharField(required=False, max_length=190)

    class Meta:
        model = Company
        fields = ['name', 'slug', 'email', 'logo', 'www', 'twitter', 'linkedin']


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, max_length=190)
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = Tag
        fields = ['name', 'slug']


class PostSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    is_featured = serializers.BooleanField(read_only=True)
    pub_date = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    position = serializers.CharField(required=True, max_length=190)
    description = serializers.CharField(required=True, min_length=4, max_length=100000)
    apply_url = serializers.URLField(required=True, max_length=190)
    apply_email = serializers.EmailField(required=True, max_length=190)
    location = serializers.CharField(required=True, max_length=190)
    type = serializers.ChoiceField(required=True, choices=Post.TypeEnum)

    company = CompanySerializer()
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ('slug', 'position', 'description', 'apply_url', 'apply_email', 'location', 'type', 'status',
                  'is_featured', 'pub_date', 'post_url', 'company', 'tags')

    def create(self, validated_data):

        company_serializer = validated_data['company']
        company_slug = slugify(company_serializer['name'])
        try:
            validated_data['company'] = Company.objects.create(slug=company_slug, **company_serializer)
        except IntegrityError:
            validated_data['company'] = Company.objects.filter(
                Q(name=company_serializer['name']) | Q(email=company_serializer['email'])).first()

        tags_serializer = []
        if 'tags' in validated_data:
            tags_serializer = validated_data['tags']
            del validated_data['tags']

        slug = slugify("%s-%s" % (company_slug, validated_data['position']))
        token = secrets.token_urlsafe(24)
        post = Post.objects.create(status=0, is_featured=False, slug=slug, activation_code=token, **validated_data)

        for item in tags_serializer:
            tags_slug = slugify(item['name'])
            try:
                tag = Tag.objects.create(slug=tags_slug, **item)
            except IntegrityError:
                tag = Tag.objects.get(name=item['name'])

            post.tags.add(tag)

        send_activation(validated_data['apply_email'], company_serializer['name'], token)

        return post


class LocationSerializer(serializers.ModelSerializer):
    location = serializers.CharField(required=True, max_length=190)

    class Meta:
        model = Post
        fields = ('location',)


class ActivatePostSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'status')

    def get_status(self, obj):
        obj.activation_code = None
        obj.save()
        # send_activation_status(obj.apply_email, obj.company.name)
        # if you want you may send activation status success
        return True
