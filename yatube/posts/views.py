from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime as dt

from .models import Post, Group
from .forms import PostForm
from yatube.settings import POSTS_IN_PAGINATOR


def index(request):
    """Главная страница с постами"""
    post_list = Post.objects.all()
    paginator = Paginator(post_list, POSTS_IN_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    current_year = dt.datetime.now().year
    return render(request, "posts/index.html",
                  {"page": page, "year": current_year})


def group_posts(request, slug):
    """Посты по конкретной группе"""
    group = get_object_or_404(Group, slug=slug)
    posts_list = Post.objects.filter(group=group)
    paginator = Paginator(posts_list, POSTS_IN_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "posts/group.html", {"group": group, "page": page})


def profile(request, username):
    """Профиль юзера."""
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    paginator = Paginator(posts, POSTS_IN_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'author': author,
        "posts_count": author.posts.count()
    }

    return render(request, 'posts/profile.html', context)


def post_view(request, username, post_id):
    """Показать пост."""
    post = get_object_or_404(Post, author__username=username, pk=post_id)

    context = {
        "post": post,
        "author": post.author,
        "posts_count": post.author.posts.count()
    }

    return render(request, 'posts/post.html', context)


@login_required
def new_post(request):
    """Создать новый пост."""
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("index")
    form = PostForm()

    context = {
        "form": form,
    }

    return render(request, "posts/new_post.html", context)


def post_edit(request, username, post_id):
    """Отредактировать пост."""
    post = get_object_or_404(Post, author__username=username, pk=post_id)

    if request.user == post.author:
        form = PostForm(instance=post, data=request.POST or None)

        if form.is_valid():
            form.save()

            return redirect('post', username=username, post_id=post_id)

        context = {
            'form': form,
        }

        return render(request, 'posts/post_edit.html', context)

    else:
        return redirect('post', username=username, post_id=post_id)
