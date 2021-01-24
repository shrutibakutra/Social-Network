from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User,Post,Follow,Like
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def index(request):
    return render(request, "network/index.html")

@csrf_exempt
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

@csrf_exempt
def addPost(request):

    '''add new post'''


    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    post = Post(
        user = request.user,
        text = data['text']
    )
    post.save()
    return render(request,"network/index.html",
            {   
                "user":request.user,
                "text":data['text']
            })

def allPosts(request):


    ''' Get all posts''' 

    all_posts = []
    posts = Post.objects.all().order_by('-created_at')
    likes = []
    for _post in posts:
        all_posts.append(_post)
    
    # Creating pagination(max 10 post per page)
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,"network/posts.html",{
        'page_obj': page_obj,
    })

def profile(request):

    '''open personal profile'''


    user = User.objects.filter(username=request.user)
    post = Post.objects.filter(user = request.user).order_by('-created_at')
    followers = Follow.objects.filter(user=request.user.id)

    followers_num = followers.count()  #number of followers
    following = Follow.objects.filter(following=request.user.id)
    following_num = following.count() #number of followings

    return render(request , "network/profile.html",{
        "userName" : user[0],
        "posts":post,
        "followers":followers_num,
        "user_id":request.user.id,
        "following":following_num
    })  

@login_required
def follow(request,userName):
    print(request.user.id)
    user = User.objects.get(id=userName)
    followers = Follow.objects.all()
    print(vars(followers[0]))
    user_f_id = []
    for id in followers:
        user_f_id.append(id.user_id)
    print(user_f_id)
    # Adding new follower to clicked user
    if request.user.id not in user_f_id:
        follow = Follow(
            following = user,
            follow = True,
            user=request.user
        )
        follow.save()
        return HttpResponseRedirect(reverse("allPosts"))
    else:
        return HttpResponseRedirect(reverse("allPosts"))

def unfollow(request,user_id):

    '''unfollow a user'''


    follower = Follow.objects.filter(following = request.user.id)
    follower.delete()
    return HttpResponseRedirect(reverse("allPosts"))


def seeProfile(request,id):

    '''see clicked profile'''
    print("see profile")
    user = User.objects.get(id=id)
    followers = Follow.objects.filter(user=id)
    is_follower = False
    follow_num = followers.count()
    following = Follow.objects.filter(following = id)
    following_num = following.count()
    
    post = Post.objects.filter(user = user).order_by('-created_at')
    return render(request , "network/profile.html",{
        "userName" : user,
        "posts":post,
        "user_id":user.id,
        # "follow":is_follower,
        "followers":follow_num,
        "following":following_num
    })

def following(request):


    '''see all posts of followings'''


    all_posts = []
    follow = Follow.objects.filter(user_id=request.user.id)
    for f in follow:
        posts = Post.objects.filter(user_id=f.following_id).order_by('-created_at')
        for _post in posts:
            all_posts.append(_post)
    paginator = Paginator(all_posts, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request , "network/posts.html",{
        # "all_posts":all_posts,
        'page_obj': page_obj
    })

@csrf_exempt
def edit(request):

    '''Edit post from here'''


    if request.method == 'POST':
        post_id = request.POST.get('id')
        textarea = request.POST.get('text')
        try:
            post = Post.objects.get(id = post_id)
            post.text = textarea    
            post.save()
            return JsonResponse({}, status=201)
        except:
            return JsonResponse({}, status=404)    
            # return render(request,"network/index.html")
    return JsonResponse({}, status=400)

# @login_required
# @csrf_exempt
# def like(request):
#     if request.method == 'POST':     
#         post_id = request.POST.get('post_id')      
#         user = request.user.id    
#         likeObj = Like.objects.filter(post = post_id,user=user)
#         post = Post.objects.get(id = post_id)
#         user = User.objects.get(id=post.user_id)
#         if likeObj:
#             print("deleting like")
#             likeObj.delete()
#             return JsonResponse({}, status=201)        
#         else:
#             print("adding like")
#             newLike = Like(
#                 like=True,
#                 user=request.user,
#                 post=post,
#                 postBy = user
#             )
#             newLike.save()
#             return JsonResponse({}, status=201)
#         return;  
#     return JsonResponse({}, status=400)

@login_required           
@csrf_exempt
def like(request):
    if request.method=='POST':
       
        post_id = request.POST.get('post_id')
        is_liked = request.POST.get('is_liked')
        user = request.user
        post = Post.objects.get(id = post_id)
        try:
            if is_liked=='yes':
                post.liked_by.remove(user)
                is_liked = 'no'
            else:
                post.liked_by.add(user)
                is_liked = 'yes'
            post.save()
            return JsonResponse({'like_count': post.liked_by.count(), 'is_liked': is_liked, "status": 201})
        except:
            return JsonResponse({'error': "Post not found", "status": 404})  
    return JsonResponse({}, status=400)









 