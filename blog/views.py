from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm


def home(request):
    """Home page - list all published posts"""
    search_query = request.GET.get("q", "")
    category_slug = request.GET.get("category", "")

    posts = Post.objects.filter(status="published").select_related("author", "category")

    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query)
            | Q(content__icontains=search_query)
            | Q(excerpt__icontains=search_query)
        )

    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "search_query": search_query,
        "category_slug": category_slug,
    }
    return render(request, "blog/home.html", context)


def post_detail(request, slug):
    """Detail page for a single post"""
    post = get_object_or_404(Post, slug=slug, status="published")
    comments = post.approved_comments

    if request.method == "POST" and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(
                request, "Your comment has been submitted and is awaiting approval."
            )
            return redirect("post_detail", slug=post.slug)
    else:
        comment_form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "comment_form": comment_form,
    }
    return render(request, "blog/post_detail.html", context)


def category_posts(request, slug):
    """List posts in a specific category"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(status="published", category=category).select_related(
        "author"
    )

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "category": category,
        "page_obj": page_obj,
    }
    return render(request, "blog/category_posts.html", context)


@login_required
def create_post(request):
    """Create a new blog post"""
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if post.status == "published" and not post.published_at:
                post.published_at = timezone.now()
            post.save()
            messages.success(request, "Your post has been created successfully!")
            return redirect("post_detail", slug=post.slug)
    else:
        form = PostForm()

    context = {"form": form}
    return render(request, "blog/create_post.html", context)


@login_required
def edit_post(request, slug):
    """Edit an existing blog post"""
    post = get_object_or_404(Post, slug=slug)

    # Only author or staff can edit
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, "You do not have permission to edit this post.")
        return redirect("post_detail", slug=post.slug)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if post.status == "published" and not post.published_at:
                post.published_at = timezone.now()
            post.save()
            messages.success(request, "Your post has been updated successfully!")
            return redirect("post_detail", slug=post.slug)
    else:
        form = PostForm(instance=post)

    context = {"form": form, "post": post}
    return render(request, "blog/edit_post.html", context)


@login_required
def delete_post(request, slug):
    """Delete a blog post"""
    post = get_object_or_404(Post, slug=slug)

    # Only author or staff can delete
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, "You do not have permission to delete this post.")
        return redirect("post_detail", slug=post.slug)

    if request.method == "POST":
        post.delete()
        messages.success(request, "Your post has been deleted.")
        return redirect("home")

    context = {"post": post}
    return render(request, "blog/delete_post.html", context)


@login_required
def user_posts(request):
    """List posts by the logged-in user"""
    posts = Post.objects.filter(author=request.user).select_related("category")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, "blog/user_posts.html", context)


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, "Welcome! Your account has been created successfully."
            )
            return redirect("home")
    else:
        form = UserCreationForm()

    context = {"form": form}
    return render(request, "blog/register.html", context)
