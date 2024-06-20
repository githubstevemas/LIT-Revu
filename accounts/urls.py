from django.urls import path

import accounts.views

urlpatterns = [
    path('account/', accounts.views.account, name='account'),
    path('user/<int:user_id>/', accounts.views.user_page, name='user'),
    path('subs/', accounts.views.subs, name='subs'),
]
