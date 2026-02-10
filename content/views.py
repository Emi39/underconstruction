from django.shortcuts import render, get_object_or_404
from .models import Article

def article_detail(request, slug):
    article = get_object_or_404(
        Article,
        slug=slug,
        is_published=True
    )
    return render(request, 'article_detail.html', {
        'article': article
    })