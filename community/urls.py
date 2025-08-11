from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('discussions/', views.discussion_list, name='discussion_list'),
    path('discussions/create/', views.create_discussion, name='create_discussion'),
    path('discussions/<int:discussion_id>/', views.discussion_detail, name='discussion_detail'),
    path('discussions/<int:discussion_id>/comment/', views.add_comment, name='add_comment'),
    path('discussions/<int:discussion_id>/like/', views.toggle_like, name='toggle_like'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
] 