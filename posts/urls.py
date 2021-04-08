from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # path('400/', views.page_not_found, name='not'),
    # path('500/', views.server_error, name='err'),
    path('', views.index, name='index'),
    path('group/<slug>/', views.group_posts, name='group'),
    path('new/', views.new_post, name='new_post'),
    path('<username>/', views.profile, name='profile'),
    path('<username>/<int:post_id>/', views.post_view, name='post_view'),
    path('<username>/<post_id>/edit/', views.post_edit, name='post_edit'),

]
