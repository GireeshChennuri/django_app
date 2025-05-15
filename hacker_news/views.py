from django.shortcuts import render

from .models import Details,Posts,Comments
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta


def home(request):
     username = request.session.get('username')
     if username:
        posts = Posts.objects.all().order_by('-created_at')
        return render(request, 'hacker_news/home.html', {
            'user_authenticated': True,
            'username': username,
            'posts': posts
        })
     else:
        posts = Posts.objects.all().order_by('-created_at')
        return render(request, 'hacker_news/home.html', {
            'user_authenticated': False,
            'posts': posts
        })

def login_view(request):
   if request.method == 'POST':
        if 'login_submit' in request.POST:
            # Handle login
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                details = Details.objects.get(username=username)
                if details.password == password:
                    posts = Posts.objects.all().order_by('-created_at')
                    request.session['username'] = username  # store session manually
                    return redirect('hacker_news:home')
                else:
                    messages.error(request, "Incorrect password.")
            except Details.DoesNotExist:
                messages.error(request, "User does not exist.")
            return redirect('hacker_news:login')

        elif 'signup_submit' in request.POST:
            # Handle signup
            username = request.POST.get('username')
            password = request.POST.get('password')
            if Details.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            else:
                Details.objects.create(username=username, password=password)
                messages.success(request, 'Signup successful! Please log in.')
            return redirect('hacker_news:login')
   return render(request, 'hacker_news/login.html')



def logout_view(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('hacker_news:home')  # or redirect to 'home' if you prefer

def new_posts(request):
    if not request.session.get('username'):
        return redirect('hacker_news:login')
    two_days_ago = timezone.now() - timedelta(days=2)
    posts = Posts.objects.filter(created_at__gte=two_days_ago).order_by('-created_at')
    username = request.session.get('username')

    return render(request, 'hacker_news/home.html', {
        'posts': posts,
        'user_authenticated': True,
        'username': username,
    })

def past_posts(request):
    if not request.session.get('username'):
        return redirect('hacker_news:login')

    four_days_ago = timezone.now() - timedelta(days=1)
    posts = Posts.objects.filter(created_at__lt=four_days_ago).order_by('-created_at')
    username = request.session.get('username')

    return render(request, 'hacker_news/home.html', {
        'posts': posts,
        'user_authenticated': True,
        'username': username,
    })

def submit_view(request):
        username = request.session.get('username')
        if not username:
            return redirect('hacker_news:login')  # Redirect to login if not authenticated
        if request.method=="POST":
            title = request.POST.get('title')
            link = request.POST.get('link')
            if title and link:
                try:
                    user = Details.objects.get(username=username)
                    Posts.objects.create(user=user, title=title, link=link,likes=0,
                    dislikes=0,
                    )
                    messages.success(request, "Post submitted successfully.")
                    return redirect('hacker_news:submit_view') 
                except Details.DoesNotExist:
                    messages.error(request, "User not found.")
                    return redirect('hacker_news:login')
            else:
                messages.error(request, "Both title and link are required.")
                return redirect('hacker_news:submit_ view')
        return render(request, 'hacker_news/submit.html', {
            'user_authenticated': True,
            'username': username,
        })

def comment_view(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment', '').strip()
        if comment_text:
            Comments.objects.create(post=post, comment=comment_text)
            messages.success(request, "Comment added successfully.")
            return redirect('hacker_news:comment', post_id=post.id)
        else:
            messages.error(request, "Comment cannot be empty.")
    comments = post.comments.all()
    return render(request, 'hacker_news/comments.html', {'user_authenticated': True,'post': post, 'comments': comments})

def handle_vote(request, post_id, vote_type):
    if not request.session.get('username'):
        messages.error(request, "You must be logged in to vote.")
        return redirect('hacker_news:login')

    # Get the vote history from session, or initialize it
    voted_posts = request.session.get('voted_posts', {})

    # Prevent double voting
    if str(post_id) in voted_posts:
        messages.warning(request, "You have already voted on this post.")
        return redirect('hacker_news:home')

    try:
        post = Posts.objects.get(id=post_id)
    except Posts.DoesNotExist:
        messages.error(request, "Post not found.")
        return redirect('hacker_news:home')

    if vote_type == 'like':
        post.likes += 1
    elif vote_type == 'dislike':
        post.dislikes += 1
    post.save()

    # Mark this post as voted in the session
    voted_posts[str(post_id)] = vote_type
    request.session['voted_posts'] = voted_posts

    return redirect('hacker_news:home')

    
# Create your views here.
