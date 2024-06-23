from itertools import chain

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Value, CharField
from django.shortcuts import render, redirect, get_object_or_404

from authentication.forms import AccountForm
from post.models import Ticket, Review
from accounts.models import UserFollows

User = get_user_model()


@login_required()
def account(request):

    # Get logged user's tickets, add TICKET content_type value
    tickets = (
        Ticket.objects.filter(user=request.user)
        .annotate(content_type=Value('TICKET', CharField()))
    )

    # Get logged user's reviewa, add REVIEW content_type value
    reviews = (
        Review.objects.filter(user=request.user)
        .annotate(content_type=Value('REVIEW', CharField()))
    )

    # Combine tickets and reviews, sort them by time_created
    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created, reverse=True
    )

    # Get all user's reviews and sort them by rating
    prefered_books = (
        Review.objects.filter(user=request.user).order_by('-rating')
    )

    # Get user's following/followers counts
    followings = UserFollows.objects.filter(user=request.user).count
    followers = UserFollows.objects.filter(followed_user=request.user).count

    # If request.method is POST, update account information
    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account')
        else:
            return render(
                request, 'accounts/account.html', {'form': form}
            )
    # If request.method is not POST, display current account information
    else:
        form = AccountForm(instance=request.user)
        # Render account page template
        return render(request, 'accounts/account.html', {
            'form': form,
            'posts': posts,
            'tickets_count': tickets.count(),
            'reviews_count': reviews.count(),
            'prefered_books': prefered_books,
            'followings': followings,
            'followers': followers
        })


@login_required()
def user_page(request, user_id):
    # Get user object with user_id
    user = get_object_or_404(User, id=user_id)

    # Get logged user's own tickets, add TICKET content_type value
    tickets = (
        Ticket.objects.filter(user=user)
        .annotate(content_type=Value('TICKET', CharField()))
    )

    # Get logged user's own reviews, add REVIEW content_type value
    reviews = (
        Review.objects.filter(user=user)
        .annotate(content_type=Value('REVIEW', CharField()))
    )

    # Combine tickets and reviews, sort them by time_created
    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created, reverse=True
    )

    # Get all user's reviews and sort them by rating
    prefered_books = Review.objects.filter(user=user).order_by('-rating')

    # Get user's following/followers counts
    followings = UserFollows.objects.filter(user=user).count
    followers = UserFollows.objects.filter(followed_user=user).count

    # Check if logged user is following target user
    is_following = UserFollows.objects.filter(
        user=request.user, followed_user=user
    ).exists()

    # Follow/unfollow if request.method is POST
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

    # Render user page template
    return render(request, 'accounts/user.html', {
        'user': user,
        'is_following': is_following,
        'posts': posts,
        'tickets_count': tickets.count(),
        'reviews_count': reviews.count(),
        'prefered_books': prefered_books,
        'followings': followings,
        'followers': followers
    })


@login_required()
def subs(request):
    user = request.user

    followings = UserFollows.objects.filter(user=user)
    followers = UserFollows.objects.filter(followed_user=user)

    # Ensure if serach is performed or not
    search_performed = False

    # Get search query from the GET request
    query = request.GET.get('q')
    results = None

    # If there is a search query, perform the search
    if query:
        results = User.objects.filter(username__icontains=query)
        search_performed = True

    # Follow/unfollow if request.method is POST
    if request.method == 'POST':
        follow_user_id = request.POST.get('user_id')
        follow_user = User.objects.get(id=follow_user_id)

        # Check if the current user is already following the target user
        is_following = UserFollows.objects.filter(
            user=request.user, followed_user=follow_user
        ).exists()

        if 'follow' in request.POST:
            if not is_following:
                # Create follow relationship if not already following
                follow = UserFollows(
                    user=request.user, followed_user=follow_user
                )
                follow.save()
        elif 'unfollow' in request.POST:
            if is_following:
                # Remove the follow relationship if currently following
                UserFollows.objects.filter(
                    user=request.user, followed_user=follow_user
                ).delete()
        return redirect('subs')

    # Get all following users
    followings_with_status = [
        {
            'user': follow.followed_user,
            'is_following': UserFollows.objects.filter(
                user=request.user, followed_user=follow.followed_user
            ).exists()
        }
        for follow in followings
    ]

    return render(request, 'accounts/subscriptions.html', {
        'followings': followings_with_status,
        'followers': followers,
        'results': results,
        'query': query,
        'search_performed': search_performed
    })
