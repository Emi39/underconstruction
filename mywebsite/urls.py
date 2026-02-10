from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.views.generic import TemplateView
from content.models import Article
from django.views.generic import ListView
from content.views import article_detail
from django.conf import settings
from django.conf.urls.static import static
from content.views import contact
from content.views import home
from content.views import articles_list, category_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml")),
    path('contact/', contact, name='contact'),
    path('articles/', articles_list, name='articles_list'),
    path('article/<slug:slug>/', article_detail, name='article_detail'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('category/<slug:slug>/', category_detail, name='category_detail'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)