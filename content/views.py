from django.shortcuts import render, get_object_or_404
from django.db.models import Q  # Correct import for search OR
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .models import Article, Category


def home(request):
    latest_articles = Article.objects.filter(is_published=True).order_by('-pub_date')[:3]
    return render(request, 'home.html', {'latest_articles': latest_articles})


def articles_list(request):
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q', '').strip()  # get search term

    articles = Article.objects.filter(is_published=True).order_by('-pub_date')
    
    # Apply category filter
    if category_slug:
        articles = articles.filter(category__slug=category_slug)
    
    # Apply search filter
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query)
        )
    
    categories = Category.objects.all()
    
    context = {
        'articles': articles,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query,  # pass back to keep input value
    }
    return render(request, 'articles_list.html', context)


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    
    # Get filters from query params (passed from articles list)
    from_category = request.GET.get('from_category', '')
    from_search = request.GET.get('from_search', '')
    
    context = {
        'article': article,
        'from_category': from_category,
        'from_search': from_search,
    }
    return render(request, 'article_detail.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        if name and email and message:
            send_mail(
                subject=f'New contact from {name} ({email})',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'Thank you! Your message has been sent.')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'contact.html')


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    
    articles = Article.objects.filter(
        is_published=True,
        category=category
    ).order_by('-pub_date')
    
    categories = Category.objects.all()
    
    context = {
        'category': category,
        'articles': articles,
        'categories': categories,
        'selected_category': slug,
    }
    return render(request, 'category_detail.html', context)