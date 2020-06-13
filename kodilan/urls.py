"""kodilancom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from posts import views
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework.renderers import JSONOpenAPIRenderer

router = routers.DefaultRouter()

urlpatterns = [
    path('tags', views.TagsView.as_view()),
    path('companies', views.CompaniesView.as_view()),
    path('posts', views.PostsView.as_view()),
    path('posts/slug/<slug:slug>', views.PostView.as_view()),
    path('posts/activation/<slug:activation_code>', views.ActivatePostView.as_view()),
    path('locations', views.FindLocationAction.as_view()),
    path('', include(router.urls)),
    path('schema', get_schema_view(
        title="Kodilan",
        description="API for all things …",
        version="0.0.0",
        renderer_classes=[JSONOpenAPIRenderer]
    ), name='docs-schema'),
    path('redoc', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url': 'docs-schema'}
    ), name='docs-redoc'),
    path('admin/', admin.site.urls),
]

admin.site.site_header = "Kodilan Admin"
admin.site.site_title = "Kodilan Api"
admin.site.index_title = "Welcome to Kodilan Researcher Admin"