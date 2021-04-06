from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path("", views.index, name="index"),
    # path("group/<str:slug>/", views.group_posts, name="group"),
    path("group/<slug>/", views.group_posts, name="group"),
    path("new/", views.new_post, name="new_post"),
    path('<username>/', views.profile, name='profile'),
    path('<str:username>/<int:post_id>/', views.post_view, name='post_view'),
    # path(
    #      '<str:username>/<int:post_id>/edit/',
    #      views.post_edit,
    #      name='post_edit'
    #     ),
    path(
         '<username>/<post_id>/edit/',
         views.post_edit,
         name='post_edit'
        ),
]
