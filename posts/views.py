# from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .forms import PostForm
from .models import Post, Group, User


# class SignUp(CreateView):
#     form_class = CreationForm
#     success_url = reverse_lazy("signup")
#     template_name = "signup.html"


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    return render(request, "group.html", {"group": group, "posts": posts})


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:index')
    return render(request, "new_post.html", {'form': form})

def profile(request, username):
    post_list = Post.objects.filter(author__username=username)
    posts_amount = post_list.count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html',
                  {'username': username,
                   'page': page,
                   'paginator': paginator,
                   'posts_amount': posts_amount,
                   'post_list': post_list,
                   })

def post_view(request, username, post_id):
    user = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id)
    count = Post.objects.filter(author=user).count
    return render(request, 'post.html',
            {'post': post, 'author': user, 'count': count})


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    if request.user != post.author:
        return redirect('posts:post_view',username=username)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post = form.save(commit=True)
        post.author = request.user
        post.save()
        return redirect('posts:post_view',username=username)
    return render(request, "new_post.html", {'form': form})