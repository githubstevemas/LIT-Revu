from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from flux.models import Ticket, Review
from flux.forms import TicketForm, ReviewForm


@login_required()
def home(request):
    tickets = Ticket.objects.all().order_by('-time_created')
    reviews = Review.objects.all().order_by('-time_created')
    return render(request, 'flux/home.html', {'tickets': tickets, 'reviews': reviews})


@login_required()
def subs(request):
    return render(request, 'flux/subscriptions.html')


@login_required()
def posts(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    return render(request, 'flux/posts.html',
                  {'tickets': tickets, 'reviews': reviews, 'user': request.user})


@login_required()
def create_review(request):
    return render(request, 'flux/create_review.html')


@login_required()
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'flux/create_ticket.html', {'form': form})
    else:
        form = TicketForm()
        return render(request, 'flux/create_ticket.html', {'form': form})


@login_required()
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'flux/create_review.html', {'form': form})
    else:
        form = ReviewForm()
        return render(request, 'flux/create_review.html', {'form': form})
