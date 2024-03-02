from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils.snowflake import Snowflake

snowflake = Snowflake()

# Create your models here.
class User(AbstractUser):
    id = models.PositiveBigIntegerField(primary_key=True, default=snowflake.generate_id())
    username = models.CharField(max_length=32, unique=True, db_index=True, null=False, blank=False)
    name = models.CharField(max_length=100, blank=True)
    bio = models.CharField(max_length=150, blank=True)
    avatar = models.ImageField(upload_to='avatars', default="default/blue.png")
    banner = models.ImageField(upload_to="banners", default="default/banner.png")
    banner_color = models.CharField(max_length=6, blank=True)
    is_private = models.BooleanField(default=True)
    email = models.EmailField(max_length=254, unique=True, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
class Post(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.ImageField(upload_to='posts', default=None)
    caption = models.CharField(max_length=150, blank=True)
    like_count = models.IntegerField(default=0)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Like(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')
    
    def __str__(self):
        return self.user.username

class Comment(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=150, blank=False)

class Follow(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')

    class Meta:
        unique_together = ('follower', 'followee')
    
    def __str__(self):
        return f'{self.follower.username} -> {self.followee.username}'

class Chat(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='to_user')
    active_for_initiator = models.BooleanField(default=True)
    active_for_recipient = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.initiator.username} and {self.recipient.username}'

class Message(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000, blank=False)
    is_read = models.BooleanField(default=False)

class Notification(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    notification_type = models.IntegerField(null=False)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notif_origin')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notif_destination')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    follow = models.ForeignKey(Follow, on_delete=models.CASCADE, null=True)

    # 0: like
    # 1: comment
    # 2: follow
    # 3: message
