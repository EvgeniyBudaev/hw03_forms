from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime as dt

from .models import Post, Group
from .forms import PostForm


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    current_year = dt.datetime.now().year
    return render(request, "index.html", {"page": page, "year": current_year})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts_list = Post.objects.filter(group=group).order_by("-pub_date")
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, "page": page})


def profile(request, username):
    return render(request, 'profile.html', {})


def post_view(request, username, post_id):
    # тут тело функции
    return render(request, 'post.html', {})


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("index")
        return render(request, "new_post.html", {"form": form})
    form = PostForm()
    return render(request, "new_post.html", {"form": form})


def post_edit(request, username, post_id):
    edit_post = get_object_or_404(Post, pk=post_id)
    if edit_post.author == request.user:
        if request.method == "POST":
            form = PostForm(request.POST, files=request.FILES or None, instance=edit_post)
            if form.is_valid():
                form.save()
                return redirect("post", username, post_id)
        form = PostForm(instance=edit_post)
        return render(
            request,
            "new_post.html",
            {
                "form": form,
                "username": username,
                "post_id": post_id,
                "edit_post": edit_post
            }
        )
    return redirect("post", username, post_id)