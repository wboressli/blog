from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post
from django.shortcuts import get_object_or_404
from django.contrib import messages

def post_list(request):
    obj_list = Post.objects.all()
    context = {
       "post_list": obj_list
    }
    return render(request, 'post_list.html', context)

def post_detail(request, post_id):
    obj_detail = get_object_or_404(Post, id=post_id)
    context = {
       "instance": obj_detail
    }
    return render(request, "post_detail.html", context)

def post_update(request, post_id):
    post_object = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post_object)
    if form.is_valid():
        form.save()
        messages.success(request, "Wanna try again?")
        return redirect("posts:list")
    context = {
       "form":form,
       "post_object":post_object,
       }
    return render (request, 'post_update.html', context)
    

def post_delete(request, post_id):
    obj = Post.object.get(id =post_id).delete()
    messages.warning(request, "Busted!")
    return redirect ("posts:list")

def post_home(request):
	return HttpResponse("<h1> Hello</h1>")

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Way to go!")
        return redirect ("posts:list")
    context = {
       "form":form,
    }
    return render(request, 'post_create.html', context)


