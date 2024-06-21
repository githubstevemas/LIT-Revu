from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from post.forms import TicketForm, ReviewForm, ReviewTicketForm, DeleteTicketForm
from post.models import Ticket, Review


def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
        else:
            return render(
                request, 'post/create_ticket.html', {'form': form}
            )
    else:
        form = TicketForm()
    return render(
        request, 'post/create_ticket.html', {'form': form}
    )


@login_required
def create_review(request):
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()

            ticket.reviewed = True
            ticket.save()

            return redirect('home')
        else:
            return render(request, 'post/create_review.html', {
                'ticket_form': ticket_form,
                'review_form': review_form
            })
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()
        return render(request, 'post/create_review.html', {
            'ticket_form': ticket_form,
            'review_form': review_form
        })


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
            ticket.reviewed = True
            ticket.save()
            return redirect('home')
        else:
            return render(
                request, 'post/create_ticket_review.html',
                {'form': form, 'ticket': ticket}
            )
    else:
        form = ReviewTicketForm()
        return render(
            request, 'post/create_ticket_review.html',
            {'form': form, 'ticket': ticket}
        )


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    edit_form = TicketForm(instance=ticket)
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = TicketForm(request.POST, request.FILES, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
    return render(
        request, 'post/edit_ticket.html',
        context={'edit_form': edit_form}
    )


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        edit_form = ReviewForm(request.POST, request.FILES, instance=review)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('home')
    else:
        edit_form = ReviewForm(instance=review)

    return render(request, 'post/edit_review.html', context={'edit_form': edit_form})


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    delete_form = DeleteTicketForm()
    if request.method == 'POST':
        if 'delete_ticket' in request.POST:
            delete_form = DeleteTicketForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('home')
    return render(request, 'post/delete_ticket.html', context={
        'delete_form': delete_form,
        'ticket': ticket
    })


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    delete_form = DeleteTicketForm()
    if request.method == 'POST':
        if 'delete_review' in request.POST:
            delete_form = DeleteTicketForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect('home')
    return render(request, 'post/delete_review.html', context={
        'delete_form': delete_form,
        'review': review
    })
