from django.shortcuts import render, get_object_or_404
from .models import Article
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

def article_detail(request, slug):
    article = get_object_or_404(
        Article,
        slug=slug,
        is_published=True
    )
    return render(request, 'article_detail.html', {
        'article': article
    })

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        if name and email and message:
            # Send email to yourself
            send_mail(
                subject=f'New contact from {name} ({email})',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],  # your email
                fail_silently=False,
            )
            messages.success(request, 'Thank you! Your message has been sent.')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'contact.html')