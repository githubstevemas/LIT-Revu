from itertools import chain

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value, Q
from django.shortcuts import render
from django.core.paginator import Paginator

from accounts.models import UserFollows
from post.models import Ticket, Review


User = get_user_model()


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
def own_posts(request):
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
