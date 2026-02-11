from django.shortcuts import render, get_object_or_404
from django.db.models import Q  # Correct import for search OR
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Article, Category, Comment, CommentLike, CommentReply
from django.http import JsonResponse


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
    
    # Handle comment submission
    if request.method == 'POST' and 'comment_submit' in request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        text = request.POST.get('text')
        
        if name and text:
            Comment.objects.create(
                article=article,
                name=name,
                email=email or '',
                text=text,
                is_approved=False
            )
            messages.success(request, 'Comment submitted — awaiting approval.')
        else:
            messages.error(request, 'Name and comment required.')
    
    # Handle reply submission
    if request.method == 'POST' and 'reply_submit' in request.POST:
        comment_id = request.POST.get('comment_id')
        name = request.POST.get('reply_name')
        email = request.POST.get('reply_email')
        text = request.POST.get('reply_text')
        
        if comment_id and name and text:
            parent_comment = get_object_or_404(Comment, id=comment_id)
            CommentReply.objects.create(
                comment=parent_comment,
                name=name,
                email=email or '',
                text=text,
                is_approved=False
            )
            messages.success(request, 'Reply submitted — awaiting approval.')
    
    # Handle like (AJAX)
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        comment_id = request.POST.get('comment_id')
        if comment_id:
            comment = get_object_or_404(Comment, id=comment_id)
            ip = request.META.get('REMOTE_ADDR')
            # Check if already liked from this IP
            if not CommentLike.objects.filter(comment=comment, ip_address=ip).exists():
                CommentLike.objects.create(comment=comment, ip_address=ip)
                return JsonResponse({'likes': comment.likes.count(), 'liked': True})
            return JsonResponse({'likes': comment.likes.count(), 'liked': False})
    
    approved_comments = article.comments.filter(is_approved=True).order_by('created_at')
    
    context = {
        'article': article,
        'comments': approved_comments,
        'from_category': request.GET.get('from_category', ''),
        'from_search': request.GET.get('from_search', ''),
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