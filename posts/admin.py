from django.contrib import admin

from .models import Company, Post, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'position', 'detail', 'location', 'status', 'pub_date')
    list_filter = ('status', 'position')


admin.site.register(Company)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
