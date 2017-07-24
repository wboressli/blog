from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404

def post_list(request):
    obj_list = Post.objects.all()
    context = {
       "post_list": obj_list
    }
    return render(request, 'post_list.html', context)

def post_create(request):
    return HttpResponse("<h1> Create </h1>")

def post_detail(request, post_id):
    obj_detail = get_object_or_404(Post, id=post_id)
    context = {
       "instance": obj_detail
    }
    return render(request, "post_detail.html", context)

def post_update(request):
    return HttpResponse("<h1> Update </h1>")

def post_delete(request):
    return HttpResponse("<h1> Delete </h1>")
def post_home(request):
	return HttpResponse("<h1> Hello</h1>")

