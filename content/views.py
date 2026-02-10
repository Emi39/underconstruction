from django.shortcuts import render

def home(request):
    context = {
        'message': "Something great is coming soon – now powered by Django!",
        'instagram': "Follow us on Instagram"  # or make dynamic later
    }
    return render(request, 'index.html', context)