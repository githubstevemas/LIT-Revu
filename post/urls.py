from django.urls import path

import post.views

urlpatterns = [
    path('create_review/', post.views.create_review,
         name='create_review'),
    path('create_review/<int:ticket_id>/',
         post.views.create_ticket_review,
         name='create_ticket_review'),
    path('create_ticket/', post.views.create_ticket,
         name='create_ticket'),
    path('edit_ticket/<int:ticket_id>/',
         post.views.edit_ticket,
         name='edit_ticket'),
    path('edit_review/<int:review_id>/',
         post.views.edit_review,
         name='edit_review'),
    path('delete_ticket/<int:ticket_id>/',
         post.views.delete_ticket,
         name='delete_ticket'),
    path('delete_review/<int:review_id>/',
         post.views.delete_review,
         name='delete_review'),
]
