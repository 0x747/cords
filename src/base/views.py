from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth.models import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .utils.snowflake import Snowflake
from .utils import avatar
from .utils import helper
from .models import User, Post, Like, Comment, Follow, Chat, Message, Notification
import os

User = get_user_model()
snowflake = Snowflake()

# Create your views here.

@login_required(login_url='login')
def index(request):
    user = User.objects.get(id=request.user.id)
    active_chats = Chat.objects.filter(initiator=user) | Chat.objects.filter(recipient=user)

    return render(request, 'index.html', {'user': user, 'active_chats': active_chats})

def register(request):

    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')

        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR', '')
        
        ua = request.META.get('HTTP_USER_AGENT', '')

        error_messages = {}

        if not email:
            error_messages['email_required'] = 'An Email is required.'
        if email and User.objects.filter(email=email).exists():
            error_messages['email_taken'] = 'Email is already taken.'
        if not helper.is_valid_username(username):
            error_messages['username_required'] = 'Username can be alphanumeric with an underscore and period.'
        if username and User.objects.filter(username=username).exists():
            error_messages['username_taken'] = 'That username is already taken.'
        if not helper.is_valid_password(password):
            error_messages['password_required'] = 'Password must have atleast 1 lowercase letter, 1 uppercase letter, 1 number, and 1 special character.'
        if (password) and (password != password2):
            error_messages['password_mismatch'] = 'Passwords do not match.'

        if error_messages:
            return render(request, 'register.html', {'error_messages': error_messages})
        else:
            user_id = snowflake.generate_id()
            user = User.objects.create_user(id=user_id, email=email, 
                                            username=username.lower(), password=password, 
                                            avatar=avatar.choose_default_avatar(user_id),
                                            ip_address=ip_address, ua=ua)
            user.save()

            return redirect('login')
    else:
        return render(request, 'register.html')
        

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Email or password is invalid.')
            return redirect('login')
            
    else:
        return render(request, 'login.html')

@login_required(login_url='login')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('login')

@login_required(login_url='login')
def reset_avatar(request):
    
    if 'default/' not in request.user.avatar.name:
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, request.user.avatar.name))
        except Exception as e:
            print(e)
    request.user.avatar = avatar.choose_default_avatar(request.user.id)
    request.user.save()

    return JsonResponse({'default_avatar': request.user.avatar.url})

@login_required(login_url='login')
def update_avatar(request):

    if 'default/' not in request.user.avatar.name:
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, request.user.avatar.name))
        except Exception as e:
            print(e)
    request.user.avatar = request.FILES['avatar']
    request.user.save()

    return JsonResponse({'avatar': request.user.avatar.url})

@login_required(login_url='login')
def update_banner(request):

    if 'default/' not in request.user.banner.name:
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, request.user.banner.name))
        except Exception as e:
            print(e)
    request.user.banner = request.FILES['banner']
    request.user.save()

    return JsonResponse({'banner': request.user.banner.url})

@login_required(login_url='login')
def reset_banner(request):

    if 'default/' not in request.user.banner.name:
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, request.user.banner.name))
        except Exception as e:
            print(e)
    request.user.banner = "default/banner.png"
    request.user.save()

    return JsonResponse({'default_banner': request.user.banner.url})

@login_required(login_url='login')
def add_post(request):
    
    post = Post.objects.create(id=snowflake.generate_id(), user=request.user, media=request.FILES["media"], caption=request.POST["caption"])
    post.save()

    return redirect('home')

@login_required(login_url='login')
def edit_profile(request):

    if request.method == 'POST':
        request.user.username = request.POST["username"]
        request.user.name = request.POST["name"]
        request.user.bio = request.POST["bio"]

        request.user.save()

        return redirect("/")
    else:
        return redirect("/")

@login_required(login_url='login')
def update_password(request):

    if request.method == 'POST':
        original_password = request.POST['current-password']
        new_password = request.POST['new-password']
        new_password2 = request.POST['new-password2']
        
        user = auth.authenticate(email=request.user.email, password=original_password)
        
        if user:
            if new_password != new_password2:
                return HttpResponse("<p style='padding: 3px;'>New passwords do not match.</p>")
            if new_password == '' or new_password2 == '':
                return HttpResponse("<p style='padding: 3px;'>New password is required.</p>")
            if helper.is_valid_password(new_password):
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)

                return HttpResponse("<p style='padding: 3px; background-color: green; border-radius: 3px;'>Password updated.</p>")
            else:
                return HttpResponse("<p style='padding: 3px;'>Password must have atleast 1 lowercase letter, 1 uppercase letter, 1 number, and 1 special character.</p>")
        else:   
            return HttpResponse("<p style='padding: 3px;'>Invalid Password.")

@login_required(login_url='login')        
def update_email(request):
    
    if request.method == 'POST':
        password = request.POST['current-password']
        new_email = request.POST['new-email']

        user = auth.authenticate(email=request.user.email, password=password)

        if user:
            if password == '' or new_email == '':
                return HttpResponse("<p style='padding: 3px;'>Email and password are required.</p>")
            if User.objects.filter(email=new_email).exists():
                return HttpResponse("<p style='padding: 3px;'>Email is already taken.</p>")
            else:
                request.user.email = new_email
                request.user.save()

                return HttpResponse("<p style='padding: 3px; background-color: green; border-radius: 3px;'>Email updated.</p>")
        else:
            return HttpResponse("<p style='padding: 3px;'>Invalid Password.</p>")

            
@login_required(login_url='login')
def delete_post(request, pk):

    post = Post.objects.get(id=pk)

    if request.method == 'POST' and request.user == post.user:
        post.delete()
        os.remove(os.path.join(settings.MEDIA_ROOT, post.media.name))

        return render(request, "index.html")
    else:
        return redirect("/")

@login_required(login_url='login')    
def feed(request):
    posts = Post.objects.all().order_by('-id')
    following_users = Follow.objects.filter(follower=request.user).values_list('followee', flat=True)
    following_users = list(following_users) + [request.user]
    posts = Post.objects.filter(user__in=following_users).order_by('-id')

    return render(request, 'feed.html', {'posts': posts})

@login_required(login_url='login')
def like(request, pk):
    post = Post.objects.get(id=pk)
    user_likes = Like.objects.filter(post=post)
    liked_post = Like.objects.filter(post=post, user=request.user).first()

    if request.method == 'POST':
        if liked_post == None:
            like = Like.objects.create(id=snowflake.generate_id(), user=request.user, post=post)
            like.save()
            post.like_count += 1
            post.save()

            if request.user != post.user:
                notification = Notification.objects.create(id=snowflake.generate_id(), notification_type=0, initiator=request.user, recipient=post.user, post=post) 
                notification.save()

            return render(request, 'like_button.html', {'user_has_liked_post': True, 'post': post, 'user_likes': user_likes})
        else:
            liked_post.delete()                
            post.like_count -= 1
            post.save()

            if request.user != post.user:
                Notification.objects.get(notification_type=0, initiator=request.user, post=post).delete()

            return render(request, 'like_button.html', {'user_has_liked_post': False, 'post': post, 'user_likes': user_likes})

    return render(request, 'like_button.html', {'user_has_liked_post': liked_post, 'post': post, 'user_likes': user_likes})

@login_required(login_url='login')
def comment(request, pk):
    post = Post.objects.get(id=pk)
    
    if request.method == 'POST':
        comment_text = request.POST[f'c{pk}']

        if comment_text:
            comment = Comment.objects.create(id=snowflake.generate_id(), user=request.user, post=post, comment_text=comment_text)
            comment.save()

            if request.user != post.user:
                notification = Notification.objects.create(id=snowflake.generate_id(), notification_type=1, initiator=request.user, recipient=post.user, post=post, comment=comment)
                notification.save()
        
    post_comments = Comment.objects.filter(post=post)
    return render(request, 'comments.html', {'post_comments': post_comments, 'post_id': post.id})

@login_required(login_url='login')
def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.user == comment.user:

        if request.user != comment.user:
            Notification.objects.get(initiator=request.user, comment=comment).delete()
        
        comment.delete()
        post_comments = Comment.objects.filter(post=comment.post)
        return render(request, 'comments.html', {'post_comments': post_comments, 'post_id': comment.post.id})

@login_required(login_url='login')
def profile(request, username):

    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user)
    following = Follow.objects.filter(follower=user)
    followers = Follow.objects.filter(followee=user)
    active_chats = Chat.objects.filter(initiator=request.user) | Chat.objects.filter(recipient=request.user)
    
    if Follow.objects.filter(follower= request.user, followee=user).first():
        follows = True
    else: 
        follows = False

    if "HX-Target" in request.headers:
        return render(request, 'profile.html', {'profile_user': user, 
                                                'profile_posts': posts, 
                                                'joined_date': snowflake.id_to_dateUS(user.id), 
                                                'follows': follows, 
                                                'following': following, 
                                                'followers': followers,
                                                'active_chats': active_chats})

    return render(request, 'index_profile.html', {'profile_user': user, 
                                                  'profile_posts': posts, 
                                                  'joined_date': snowflake.id_to_dateUS(user.id), 
                                                  'follows': follows, 
                                                  'following': following, 
                                                  'followers': followers,
                                                  'active_chats': active_chats})

@login_required(login_url='login')
def follow(request, pk):
    followee = User.objects.get(id=pk)
    if request.method == 'POST':
        follower = request.user
        user_following = Follow.objects.filter(follower=follower, followee=followee).first()
        
        if user_following:
            Notification.objects.get(follow=user_following).delete()
            user_following.delete()
            return redirect('profile', username=followee.username)
        else:
            new_follow = Follow.objects.create(id=snowflake.generate_id(), follower=follower, followee=followee)
            new_follow.save()
            notification = Notification.objects.create(id=snowflake.generate_id(), notification_type=2, initiator=request.user, recipient=followee, follow=new_follow)

            return redirect('profile', username=followee.username)
            
    else:
        return redirect('profile', username=followee.username)

@login_required(login_url='login')
def create_chat(request, pk):

    initiator = request.user
    recipient = User.objects.get(id=pk)
    
    existing_chat = Chat.objects.filter(initiator=initiator, recipient=recipient).first()

    if not existing_chat:
        existing_chat = Chat.objects.filter(initiator=recipient, recipient=initiator).first()

    if existing_chat:
        return redirect('chat', pk=existing_chat.id)
    else:
        chat_id = snowflake.generate_id()
        chat = Chat.objects.create(id=chat_id, initiator=initiator, recipient=recipient)
        chat.save()

        return redirect('chat', pk=chat_id)

@login_required(login_url='login')
def chat(request, pk):

    chat = Chat.objects.get(id=pk)
    messages = Message.objects.filter(chat=chat)
    active_chats = Chat.objects.filter(initiator=request.user) | Chat.objects.filter(recipient=request.user)

    if "HX-Target" in request.headers:
        return render(request, 'chat.html', {'chat': chat, 'messages': messages, 'active_chats': active_chats})
    
    return render(request, 'index_chat.html',  {'chat': chat, 'messages': messages, 'active_chats': active_chats})

@login_required(login_url='login')
def delete_message(request, pk):

    message = Message.objects.get(id=pk)

    if request.method == 'POST' and request.user == message.author:
        message.delete()
        return HttpResponse(204)

@login_required(login_url='login')
def search(request):

    query = request.GET["query"]

    if query:
        users = User.objects.filter(username__icontains=query) | User.objects.filter(bio__iregex=r'\b{}\b'.format(query))

        return render(request, "search_result.html", {'users': users})

@login_required(login_url='login')
def user_posts(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user)
    active_chats = Chat.objects.filter(initiator=request.user) | Chat.objects.filter(recipient=request.user)

    if 'HX-Target' in request.headers:
        return render(request, 'user_posts.html', {'posts': posts, 'active_chats': active_chats})

    return render(request, 'index_posts.html', {'posts': posts, 'active_chats': active_chats})

@login_required(login_url='login')
def notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-id')
    return render(request, 'notifications.html', {'notifications': notifications})