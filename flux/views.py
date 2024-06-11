from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from flux.models import Ticket, Review
from flux.forms import TicketForm, ReviewForm, ReviewTicketForm, DeleteTicketForm


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


@login_required()
def create_ticket_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = ReviewTicketForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('home')
        else:
            return render(request, 'flux/create_ticket_review.html', {'form': form, 'ticket': ticket})
    else:
        form = ReviewTicketForm()
        return render(request, 'flux/create_ticket_review.html', {'form': form, 'ticket': ticket})


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    edit_form = TicketForm(instance=ticket)
    delete_form = DeleteTicketForm()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = TicketForm(request.POST, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')

        if 'delete_ticket' in request.POST:
            delete_form = DeleteTicketForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('home')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'flux/edit_ticket.html', context=context)
