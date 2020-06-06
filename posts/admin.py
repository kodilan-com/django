from django.contrib import admin

from .models import Company, Post, Tag
from django.utils.html import format_html
from django.urls import reverse


def make_published(modeladmin, request, queryset):
    queryset.update(status=1)


def make_unpublished(modeladmin, request, queryset):
    queryset.update(status=2)


def make_disapproved(modeladmin, request, queryset):
    queryset.update(status=0)


make_unpublished.short_description = "Mark posts stories as unpublished"
make_published.short_description = "Mark posts stories as published"
make_disapproved.short_description = "Mark posts stories as disapproved"


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'position', 'detail', 'location', 'status', 'pub_date')
    list_filter = ('status', 'position')
    actions = [make_published, make_unpublished, make_disapproved]


admin.site.register(Company)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
