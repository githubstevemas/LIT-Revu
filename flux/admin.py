from django.contrib import admin
from post.models import Review, Ticket
from accounts.models import UserFollows

admin.site.register(Review)
admin.site.register(Ticket)
admin.site.register(UserFollows)
