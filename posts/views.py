from __future__ import unicode_literals
from .models import Post, Like
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import PostForm, UserSignUp, UserLogin
from .models import Post
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote
from django.http import Http404, JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

def like_button(request,post_id):
    obj = Post.objects.get(id=post_id)

    like, created = Like.objects.get_or_create(user=request.user, post=obj)

    if created:
        action="like"
    else:
        action="unlike"
        like.delete()

    post_like_count = obj.like_set.all().count()
    context = {
        "action": action,
        "like_count": post_like_count,
    }


    return JsonResponse(context, safe =False)

def usersignup(request):
    context = {}
    form = UserSignUp()
    context['form'] = form
    if request.method == "POST":
        form = UserSignUp(request.POST)
        if form.is_valid():
            
            user = form.save(commit=False)
            username = user.username
            password = user.password
            user.set_password(password)
            user.save()
            auth_user = authenticate(username=username, password=password)
            login(request, auth_user)

            return redirect("posts:list")
        messages.error(request, form.errors)
        return redirect("posts:signup")
    return render(request, 'signup.html', context)

def userlogout(request):
    logout(request)
    return redirect("posts:login")

def userlogin(request):
    context = {}
    form = UserLogin()
    context['form'] = form
    if request.method == "POST":
        form = UserLogin(request.POST)
        if form.is_valid():
        
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # user.set_password(password)
            # user.save()
            # auth_user = authenticate(username=username, password=password)
            # login(request, auth_user)
            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect("posts:list")

            messages.warning(request, "Wrong username/password combo. Go at it again!")
            return redirect("posts:login")
        messages.warning(request, form.errors)
        return redirect("posts:login")
    return render(request,'login.html', context)

def post_list(request):
    today = timezone.now().date()

    if request.user.is_staff or request.user.is_superuser:
        object_list = Post.objects.all()
    else:
        object_list = Post.objects.filter(draft=False).filter(publish__lte=today)
    query = request.GET.get("q")
    if query:
        object_list = object_list.filter(
        Q(title__icontains=query)|
        Q(content__icontains=query)|
        Q(author__first_name__icontains=query)|
        Q(author__last_name__icontains=query)
        ).distinct()

#.order_by("-timestamp","-updated")
    paginator = Paginator(object_list, 5) # Show 5 contacts per page
    page = request.GET.get('page')
    try:
        obj= paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        obj= paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        obj= paginator.page(paginator.num_pages)
    context = {
    "object_list": obj,
    "title": "List",
    "user": request.user,
    "today": today,
    }
    return render(request, 'post_list.html', context)

def post_detail(request, post_slug):
    obj = get_object_or_404(Post, slug=post_slug)
    date = timezone.now().date()

    if obj.publish > timezone.now().date() or obj.draft:
        if not (request.user.is_staff or request.user.is_superuser):
            raise Http404

    if request.user.is_authenticated():
        if Like.objects.filter(post=obj, user=request.user).exists():
            liked = True 
        else:
            liked = False

    post_like_count = obj.like_set.all().count()

    context = {
       "instance": obj,
       "liked": liked,
       "like_count": post_like_count,
    }
    return render(request, "post_detail.html", context)

def post_update(request, post_slug):
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404
    instance = get_object_or_404(Post, slug=post_slug)
    post_object = get_object_or_404(Post, slug=post_slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, "Wanna try again?")
        return redirect("posts:list")
    context = {
       "form":form,
       "instance": instance,
       "title": "Update",
    
       }
    return render (request, 'post_update.html', context)
    

def post_delete(request, post_slug):
    if not (request.user.is_superuser):
        raise Http404
    instance = get_object_or_404(Post, slug=post_slug)
    instance.delete()
    messages.warning(request, "Busted!")
    return redirect ("posts:list")

def post_home(request):
    return HttpResponse("<h1> Hello</h1>")

def post_create(request):
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.author = request.user
        obj.save()
        messages.success(request, "Way to go!")
        return redirect ("posts:list")
    context = {
       "form":form,
    }
    return render(request, 'post_create.html', context)


