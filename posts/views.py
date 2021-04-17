from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User
from posts.settings import POSTS_QUANTITY


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, POSTS_QUANTITY)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page},
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all().order_by('-pub_date')
    paginator = Paginator(posts, POSTS_QUANTITY)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'group': group,
        'page': page,
    }
    return render(request, "group.html", context)


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'new.html', {'form': form})
    form.instance.author = request.user
    form.save()
    return redirect('index')


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    paginator = Paginator(posts, POSTS_QUANTITY)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    following = (
        request.user.is_authenticated and Follow.objects.filter(
            user=request.user, author=author
        ).exists()
    )
    following_count = Follow.objects.all().count()
    context = {
        'author': author,
        'page': page,
        'following': following,
        'following_count': following_count
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    form = CommentForm(request.POST or None)
    comments = post.comments.all().order_by('-created')
    following_count = Follow.objects.all().count()
    context = {
        'author': post.author,
        'post': post,
        'form': form,
        'comments': comments,
        'following_count': following_count
    }
    return render(request, 'post.html', context)


@login_required
def post_edit(request, username, post_id):
    if username != request.user.username:
        return redirect('post', username=username, post_id=post_id)
    post = get_object_or_404(Post, id=post_id, author__username=username)
    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
    )
    if not form.is_valid():
        return render(request, "new.html", {"form": form, 'post': post})
    form.save()
    return redirect("post", username=username, post_id=post_id)


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    if not request.user:
        return redirect('login')
    form = CommentForm(request.POST or None)
    context = {'form': form, 'post': post}
    if not form.is_valid():
        form = CommentForm()
        return render(request, 'comments.html', context)
    form.instance.author = get_object_or_404(
        User, username=request.user.username
    )
    comment = form.save(commit=False)
    comment.author = request.user
    comment.post = post
    comment.save()
    return redirect('post', username=username, post_id=post_id)


@login_required
def follow_index(request):
    following_posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(following_posts, POSTS_QUANTITY)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
    }
    return render(request, "follow.html", context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(author=author, user=request.user)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(author=author, user=request.user).delete()
    return redirect('profile', username=username)
