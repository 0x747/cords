from django.contrib import admin
from .models import User, Post, Like, Comment, Follow, Chat, Message, Notification
# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Notification)