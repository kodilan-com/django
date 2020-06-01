from django.contrib import admin

from .models import Company, Post, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'detail', 'location', 'status', 'pub_date')


admin.site.register(Company)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
