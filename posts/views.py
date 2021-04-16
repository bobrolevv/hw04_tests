from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404

from yatube.settings import COUNT_POSTS_IN_PAGE
from .forms import PostForm, CommentForm
from .models import Post, Group, User, Comment


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
    list_flag = True
    context = {'group': group,
               'posts': posts,
               'page': page,
               'list_flag': list_flag,
               }
    return render(request, 'group.html', context)


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
    context = {'post': post,
               'author': post.author,
               'posts_amount': posts_amount
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



@login_required #(login_url="/auth/login/")
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    posts_amount = Post.objects.filter(author=post.author).count()  # noqa
    form = CommentForm(request.POST or None,
                    instance=post)
    print(f'=={form}==')
    if form.is_valid():
        print('======1======')
        new_comment = form.save()
        new_comment.author = request.user
        new_comment.post = current_post
        new_comment.save()
        context = {
            'post': post,
            'author': post.author,
        }
        return render(request, 'post.html', context)
    print('=====2=====')
    comments = Comment.objects.filter(post=post)
    print(f'=====3====={comments}')
    context = {'form': form,
               'comments': comments,
               'post': post,
               'author': post.author,
               'posts_amount': posts_amount,
               }
    print(f'=====4====={context}')
    return render(request, 'post.html', context)
