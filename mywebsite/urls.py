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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ListView.as_view(
        model=Article,
        template_name='index.html',
        context_object_name='articles',
        queryset=Article.objects.filter(is_published=True).order_by('-pub_date')[:6]
    ), name='home'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml")),
    path('contact/', contact, name='contact'),
    path('article/<slug:slug>/', article_detail, name='article_detail'),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)