from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('search/', views.search, name='search'),
    path('update-password/', views.update_password, name='update_password'),
    path('update-email/', views.update_email, name='update_email'),
    path('notifications/', views.notifications, name='notifications'),
    path('update-avatar/', views.update_avatar, name='update_avatar'),
    path('reset-avatar/', views.reset_avatar, name='reset_avatar'),
    path('update-banner/', views.update_banner, name='update_banner'),
    path('reset-banner/', views.reset_banner, name='reset_banner'),
    path('add-post/', views.add_post, name='add_post'),
    path('edit-profile/', views.edit_profile, name='edit_profile'), 
    path('delete-post/<int:pk>/', views.delete_post, name='delete_post'),
    path('feed/', views.feed, name='feed'),
    path('u/<str:username>/', views.profile, name='profile'),
    path('like/<int:pk>/', views.like, name='like'),
    path('comment/<int:pk>/', views.comment, name='comment'),
    path('delete-comment/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('follow/<int:pk>/', views.follow, name='follow'),
    path('create-chat/<int:pk>/', views.create_chat, name='create_chat'),
    path('chat/<int:pk>/', views.chat, name='chat'),
    path('delete-message/<int:pk>/', views.delete_message, name='delete_message'),
    path('<str:username>/posts/', views.user_posts, name='user_posts')
]