from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from .models import Post

def post_list(request):
    object_list = Post.objects.get(title="re")
    context = {
    "object_list": object_list,
    "title": "List",
    "user": request.user
    }
    return render(request, 'post_list.html', context)

def post_create(request):
    return HttpResponse("<h1> Create </h1>")

def post_detail(request):
    return HttpResponse("<h1> Detail </h1>")

def post_list(request):
    return HttpResponse("<h1> List </h1>")

def post_update(request):
    return HttpResponse("<h1> Update </h1>")

def post_delete(request):
    return HttpResponse("<h1> Delete </h1>")
def post_home(request):
	return HttpResponse("<h1> Hello</h1>")

