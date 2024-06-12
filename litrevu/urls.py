from django.conf import settings
from django.conf.urls.static import static
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
    path('user_page/<int:user_id>/', authentication.views.user_page, name='user_page'),
    path('subs/', flux.views.subs, name='subs'),
    path('own_posts/', flux.views.posts, name='own_posts'),
    path('create_review/', flux.views.create_review, name='create_review'),
    path('create_review/<int:ticket_id>/', flux.views.create_ticket_review, name='create_ticket_review'),
    path('create_ticket/', flux.views.create_ticket, name='create_ticket'),
    path('edit_ticket/<int:ticket_id>/', flux.views.edit_ticket, name='edit_ticket'),
    path('delete_ticket/<int:ticket_id>/', flux.views.delete_ticket, name='delete_ticket'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
