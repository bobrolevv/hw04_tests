from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page

from yatube.settings import COUNT_POSTS_IN_PAGE
from .forms import PostForm, CommentForm
from .models import Post, Group, User, Comment


# @cache_page(60 * 15)
def index(request):
    post_list = Post.objects.all()  # noqa
    paginator = Paginator(post_list, COUNT_POSTS_IN_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, COUNT_POSTS_IN_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {'page': page})


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None,)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:index')
    return render(request, 'new_post.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user)  # noqa
    posts_amount = post_list.count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    list_flag = True
    context = {'author': user,
               'page': page,
               'paginator': paginator,
               'posts_amount': posts_amount,
               'post_list': post_list,
               'list_flag': list_flag,
               }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    posts_amount = Post.objects.filter(author=post.author).count()  # noqa
    form = CommentForm()
    context = {'post': post,
               'author': post.author,
               'posts_amount': posts_amount,
               'comments': Comment.objects.filter(post=post),
               'form': form,
               }
    return render(request, 'post.html', context)


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    if request.user != post.author:
        return redirect('posts:profile', username=username)
    form = PostForm(request.POST or None,
                    files=request.FILES or None,
                    instance=post)
    if form.is_valid():
        post.save()
        return redirect('posts:post_view', username=username,
                        post_id=post_id)
    return render(request, 'new_post.html', {'form': form, 'post': post})


def page_not_found(request, exception):  # noqa
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)


@login_required
def add_comment(request, username, post_id):
    user_post = get_object_or_404(Post, author__username=username, id=post_id)
    form = CommentForm(request.POST or None, instance=None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = user_post
        comment.author = request.user
        comment.save()
        return redirect('posts:post_view',
                        username=user_post.author.username,
                        post_id=user_post.id)

@login_required
def follow_index(request):
    # информация о текущем пользователе доступна в переменной request.user
    user = request.user
    user_posts = Post.objects.filter()
    return render(request, "follow.html", {'user_posts': user_posts})

@login_required
def profile_follow(request, username):
    # ...
    pass


@login_required
def profile_unfollow(request, username):
    # ...
    pass
