from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.db.models import Count

from .models import User,Content,Follow,Like

def index(request):
    allposts = Content.objects.all().order_by("id").reverse()
    
    paginator = Paginator(allposts, 10)
    page_Number=request.GET.get('page')
    posts_of_page = paginator.get_page(page_Number)
    
    return render(request, "network/index.html", {
        "allposts": allposts,
        "posts_of_page": posts_of_page,
    })


def profile(request, user_id):
    user=User.objects.get(pk=user_id)
    allposts = Content.objects.filter(user=user).order_by("id").reverse()
    
    paginator = Paginator(allposts, 10)
    page_Number=request.GET.get('page')
    posts_of_page = paginator.get_page(page_Number)
    
    following = Follow.objects.filter(user=user)
    followers = Follow.objects.filter(user_followed=user) 
    
    try:
        checkIfFollowing = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(checkIfFollowing) != 0:
            isFollowing= True
        else:
            isFollowing = False
    except:
        isFollowing = False
    
    return render(request, "network/profile.html", {
        "allposts":allposts,
        "posts_of_page":posts_of_page,
        "username":user.username,
        "following": following,
        "followers": followers,
        "isFollowing": isFollowing,
        "user_profile": user
    })
    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def newPost(request):
    if request.method == "POST":
        content = request.POST['content']
        user= User.objects.get(pk=request.user.id)
        post1 = Content(post=content, user=user)
        post1.save()
        return HttpResponseRedirect(reverse(index))
        
        
def follow(request):
    userfollow= request.POST['userfollow']
    currentUser = User.objects.get(pk=request.user.id)
    userfollowInfo = User.objects.get(username = userfollow)
    F_info = Follow(user=currentUser, user_followed=userfollowInfo)
    F_info.save()
    user_id= userfollowInfo.id
    return HttpResponseRedirect(reverse(profile, kwargs={"user_id" : user_id}))

def unfollow(request):
    userfollow= request.POST['userfollow']
    currentUser = User.objects.get(pk=request.user.id)
    userfollowInfo = User.objects.get(username = userfollow)
    F_info = Follow.objects.get(user=currentUser, user_followed=userfollowInfo)
    F_info.delete()
    user_id= userfollowInfo.id
    return HttpResponseRedirect(reverse(profile, kwargs={"user_id" : user_id}))


def following(request):
    current_user = User.objects.get(pk=request.user.id)
    peopleFollowing = Follow.objects.filter(user=current_user)
    allposts = Content.objects.all().order_by("id").reverse()
    
    following_posts = []
    
    for post in allposts:
        for people in peopleFollowing:
            if people.user_followed == post.user:
                following_posts.append(post)
        
        
        
    paginator = Paginator(following_posts, 10)
    page_Number=request.GET.get('page')
    posts_of_page = paginator.get_page(page_Number)
    
    return render(request, "network/following.html", {
        "posts_of_page":posts_of_page,
        "username":current_user,
    })

def edit(request,post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Content.objects.get(pk=post_id)
        edit_post.post = data["content"]
        edit_post.save()
        return JsonResponse( {"message": "Change Successful", "data" : data["content"]})
        
        
def add_like(request,post_id):
    post = Content.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    newLike = Like(user=user, post=post)
    newLike.save()
    return JsonResponse( {"message": "A New Like Has Been Added!"})

def remove_like(request,post_id):
    post = Content.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Like.objects.filter( user=user, post=post)
    like.delete()
    return JsonResponse( {"message": "A New Like Has Been Removed!"})