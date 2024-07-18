from django.test import TestCase
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
    
    allLikes = Like.objects.all()
    WhoYouLiked = [like.post.id for like in allLikes if like.user == request.user]
    
    return render(request, "network/test.html", {
        "allposts": allposts,
        "posts_of_page": posts_of_page,
        "WhoYouLiked": WhoYouLiked,
    })

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