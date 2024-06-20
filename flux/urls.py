from django.urls import path

import flux.views

urlpatterns = [
    path('home/', flux.views.home, name='home'),
    path('search/', flux.views.search, name='search'),
    path('own_posts/', flux.views.posts, name='own_posts')
]
