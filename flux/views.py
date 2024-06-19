
from itertools import chain

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from flux.models import Ticket, Review, UserFollows
from flux.forms import (TicketForm,
                        ReviewForm,
                        ReviewTicketForm,
                        DeleteTicketForm)
from authentication.forms import AccountForm


@login_required()
def home(request):
    users = User.objects.all()
    total_reviews = Review.objects.all()

    top_users_list = []

    for user in users:
        review_count = total_reviews.filter(user=user).count()
        top_users_list.append({
            'user': user,
            'count': review_count
        })

    sorted_top_users = sorted(
        top_users_list,
        key=lambda item: item['count'],
        reverse=True
    )

    followings = (UserFollows.objects.filter(
        user=request.user).values_list('followed_user')
                  )

    tickets = Ticket.objects.filter(
        Q(user__in=followings) | Q(user=request.user)).annotate(
        content_type=Value('TICKET', CharField())
    )
    reviews = (
        Review.objects.filter(
            Q(user__in=followings) |
            Q(user=request.user) |
            Q(ticket__user=request.user)
        ).annotate(content_type=Value('REVIEW', CharField()))
    )

    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created, reverse=True
    )

    unreviewed = Ticket.objects.filter(reviewed=False)

    paginator = Paginator(posts, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'flux/home.html', {
        'users': users,
        'page_obj': page_obj,
        'unreviewed': unreviewed,
        'sorted_top_users': sorted_top_users,
    })


@login_required()
def account(request):
    tickets = (
        Ticket.objects.filter(user=request.user)
        .annotate(content_type=Value('TICKET', CharField()))
    )
    reviews = (
        Review.objects.filter(user=request.user)
        .annotate(content_type=Value('REVIEW', CharField()))
    )

    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created, reverse=True
    )

    prefered_books = (
        Review.objects.filter(user=request.user).order_by('-rating')
    )

    tickets_count = tickets.count()
    reviews_count = reviews.count()

    followings = UserFollows.objects.filter(user=request.user).count
    followers = UserFollows.objects.filter(followed_user=request.user).count

    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(
                request, 'flux/account.html', {'form': form}
            )
    else:
        form = AccountForm(instance=request.user)
        return render(request, 'flux/account.html', {
            'form': form,
            'posts': posts,
            'tickets_count': tickets_count,
            'reviews_count': reviews_count,
            'prefered_books': prefered_books,
            'followings': followings,
            'followers': followers
        })


@login_required()
def posts(request):
    tickets = (
        Ticket.objects.filter(user=request.user)
        .annotate(content_type=Value('TICKET', CharField()))
    )
    reviews = (
        Review.objects.filter(user=request.user)
        .annotate(content_type=Value('REVIEW', CharField()))
    )

    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created, reverse=True
    )

    paginator = Paginator(posts, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'flux/own_posts.html',
                  {'page_obj': page_obj})


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
                request, 'flux/create_ticket.html', {'form': form}
            )
    else:
        form = TicketForm()
    return render(
        request, 'flux/create_ticket.html', {'form': form}
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
            return render(request, 'flux/create_review.html', {
                'ticket_form': ticket_form,
                'review_form': review_form
            })
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()
        return render(request, 'flux/create_review.html', {
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
                request, 'flux/create_ticket_review.html',
                {'form': form, 'ticket': ticket}
            )
    else:
        form = ReviewTicketForm()
        return render(
            request, 'flux/create_ticket_review.html',
            {'form': form, 'ticket': ticket}
        )


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    edit_form = TicketForm(instance=ticket)
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = TicketForm(request.POST, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
    return render(
        request, 'flux/edit_ticket.html',
        context={'edit_form': edit_form}
    )


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    edit_form = ReviewForm(instance=review)
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = ReviewForm(request.POST, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
    return render(
        request, 'flux/edit_review.html',
        context={'edit_form': edit_form}
    )


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
    return render(request, 'flux/delete_ticket.html', context={
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
    return render(request, 'flux/delete_review.html', context={
        'delete_form': delete_form,
        'review': review
    })


User = get_user_model()


@login_required()
def user_page(request, user_id):
    user = get_object_or_404(User, id=user_id)

    tickets = (
        Ticket.objects.filter(user=user)
        .annotate(content_type=Value('TICKET', CharField()))
    )

    reviews = (
        Review.objects.filter(user=user)
        .annotate(content_type=Value('REVIEW', CharField()))
    )

    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created, reverse=True
    )

    prefered_books = Review.objects.filter(user=user).order_by('-rating')

    tickets_count = tickets.count()
    reviews_count = reviews.count()

    followings = UserFollows.objects.filter(user=user).count
    followers = UserFollows.objects.filter(followed_user=user).count

    is_following = UserFollows.objects.filter(
        user=request.user, followed_user=user
    ).exists()

    if request.method == 'POST':
        if 'follow' in request.POST:
            if not is_following:
                follow = UserFollows(user=request.user, followed_user=user)
                follow.save()
        elif 'unfollow' in request.POST:
            if is_following:
                UserFollows.objects.filter(
                    user=request.user, followed_user=user
                ).delete()
        return redirect('user', user_id=user_id)

    return render(request, 'flux/user.html', {
        'user': user,
        'is_following': is_following,
        'posts': posts,
        'tickets_count': tickets_count,
        'reviews_count': reviews_count,
        'prefered_books': prefered_books,
        'followings': followings,
        'followers': followers
    })


@login_required()
def subs(request):
    user = request.user
    followings = UserFollows.objects.filter(user=user)
    followers = UserFollows.objects.filter(followed_user=user)

    search_performed = False

    query = request.GET.get('q')
    results = None

    if query:
        results = User.objects.filter(username__icontains=query)
        search_performed = True

    if request.method == 'POST':
        follow_user_id = request.POST.get('user_id')
        follow_user = User.objects.get(id=follow_user_id)
        is_following = UserFollows.objects.filter(
            user=request.user, followed_user=follow_user
        ).exists()

        if 'follow' in request.POST:
            if not is_following:
                follow = UserFollows(
                    user=request.user, followed_user=follow_user
                )
                follow.save()
        elif 'unfollow' in request.POST:
            if is_following:
                UserFollows.objects.filter(
                    user=request.user, followed_user=follow_user
                ).delete()
        return redirect('subs')

    followings_with_status = [
        {
            'user': follow.followed_user,
            'is_following': UserFollows.objects.filter(
                user=request.user, followed_user=follow.followed_user
            ).exists()
        }
        for follow in followings
    ]

    return render(request, 'flux/subscriptions.html', {
        'followings': followings_with_status,
        'followers': followers,
        'results': results,
        'query': query,
        'search_performed': search_performed
    })


@login_required()
def search(request):
    search_performed = False

    query = request.GET.get('q')
    results = None

    if query:
        results = Review.objects.filter(ticket__title__icontains=query)
        search_performed = True

    return render(request, 'flux/search.html', {
        'results': results,
        'query': query,
        'search_performed': search_performed
    })
