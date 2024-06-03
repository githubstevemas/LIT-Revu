from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from flux.models import Review, Ticket


@login_required()
def home(request):
    tickets = Ticket.objects.all()
    # reviews = Review.objects.all()
    return render(request, 'flux/home.html', {'tickets': tickets})


@login_required()
def subs(request):
    return render(request, 'flux/subscriptions.html')


@login_required()
def posts(request):
    return render(request, 'flux/posts.html')
