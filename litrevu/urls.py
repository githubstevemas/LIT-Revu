from django.contrib import admin
from django.urls import path

import authentication.views
import flux.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.LoginPage.as_view(), name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('home/', flux.views.home, name='home'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('subs/', flux.views.subs, name='subs'),
    path('posts/', flux.views.posts, name='posts'),
    path('create_review/', flux.views.create_review, name='create_review'),
    path('create_ticket/', flux.views.create_ticket, name='create_ticket')
]
