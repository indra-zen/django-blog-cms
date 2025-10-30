# Tutorial 05: Views and URLs

## What You'll Learn

- Understand Django views and URL routing
- Create views for listing and displaying posts
- Handle user requests and return responses
- Map URLs to views
- Pass data to templates
- Work with querysets and filters

## Understanding Views

A **view** is a Python function that:
1. Receives a web request
2. Processes it (fetch data, logic, etc.)
3. Returns a web response (HTML, JSON, redirect, etc.)

```python
def my_view(request):
    # 1. Get data
    posts = Post.objects.all()
    
    # 2. Process
    # (optional logic here)
    
    # 3. Return response
    return render(request, 'template.html', {'posts': posts})
```

## Understanding URLs

URLs map paths to views:

```python
path('posts/', views.post_list, name='post_list')
```

- `'posts/'`: URL pattern
- `views.post_list`: Function to call
- `name='post_list'`: Name for referencing in templates

## Project URL Structure

We'll create a two-level URL system:

```
blog_cms/urls.py (Main)
       ↓
   includes blog/urls.py
       ↓
   Routes to views
```

## Step 1: Create URL Configuration

### Create Blog URLs

Create `blog/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("post/create/", views.create_post, name="create_post"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("post/<slug:slug>/edit/", views.edit_post, name="edit_post"),
    path("post/<slug:slug>/delete/", views.delete_post, name="delete_post"),
    path("category/<slug:slug>/", views.category_posts, name="category_posts"),
    path("my-posts/", views.user_posts, name="user_posts"),
    path("register/", views.register, name="register"),
]
```

### Understanding URL Patterns

**Basic Pattern:**
```python
path("posts/", views.post_list, name="post_list")
```
Matches: `/posts/`

**URL Parameters:**
```python
path("post/<slug:slug>/", views.post_detail, name="post_detail")
```
- `<slug:slug>`: Captures a slug from URL
- Matches: `/post/my-first-post/`
- Passes `slug="my-first-post"` to view

**Path Converters:**
- `<int:id>`: Integer (e.g., 123)
- `<slug:slug>`: Slug (letters, numbers, hyphens)
- `<str:username>`: String
- `<uuid:id>`: UUID

**⚠️ Order Matters!**
```python
# WRONG - 'create' will match as a slug!
path("post/<slug:slug>/", ...),
path("post/create/", ...),  # Never reached!

# RIGHT - Specific patterns first
path("post/create/", ...),
path("post/<slug:slug>/", ...),  # This is correct!
```

### Connect to Main URLs

Open `blog_cms/urls.py` and update it:

```python
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # Include blog URLs
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='blog/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='blog/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='blog/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='blog/password_reset_complete.html'), name='password_reset_complete'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### Understanding includes

```python
path('', include('blog.urls'))
```
- All URLs from `blog/urls.py` are included
- Empty string `''` means root URL
- So `blog/urls.py` path `"posts/"` becomes `"/posts/"`

**Built-in Auth Views:**
```python
auth_views.LoginView.as_view(template_name='blog/login.html')
```
Django provides login/logout views. We just specify the template!

## Step 2: Create the Home View

Open `blog/views.py` and let's start building views:

```python
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
    search_query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    
    posts = Post.objects.filter(status='published').select_related('author', 'category')
    
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_slug': category_slug,
    }
    return render(request, 'blog/home.html', context)
```

### Understanding the Home View

**Get Query Parameters:**
```python
search_query = request.GET.get('q', '')
```
- `request.GET`: Dictionary of URL parameters
- `.get('q', '')`: Get 'q' parameter or empty string
- From URL: `/?q=django` → `search_query = "django"`

**Filter Posts:**
```python
posts = Post.objects.filter(status='published')
```
Only show published posts (not drafts).

**Optimize Queries:**
```python
.select_related('author', 'category')
```
Fetches related data in one query instead of multiple. Much faster!

**Search with Q Objects:**
```python
Q(title__icontains=search_query) | Q(content__icontains=search_query)
```
- `Q`: Creates complex queries
- `__icontains`: Case-insensitive contains
- `|`: OR operator
- Searches in title OR content OR excerpt

**Pagination:**
```python
paginator = Paginator(posts, 10)
page_obj = paginator.get_page(page_number)
```
- Shows 10 posts per page
- `page_obj` has posts + pagination info

**Context Dictionary:**
```python
context = {'page_obj': page_obj, ...}
return render(request, 'template.html', context)
```
Variables available in the template.

## Step 3: Create Post Detail View

Add this to `views.py`:

```python
def post_detail(request, slug):
    """Detail page for a single post"""
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.approved_comments
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been submitted and is awaiting approval.')
            return redirect('post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/post_detail.html', context)
```

### Understanding Post Detail

**get_object_or_404:**
```python
post = get_object_or_404(Post, slug=slug, status='published')
```
- Tries to get post with matching slug
- Returns 404 page if not found
- Better than `Post.objects.get()` which crashes

**Handle POST Request:**
```python
if request.method == 'POST':
    # Process form
else:
    # Show empty form
```
- GET: Show the page
- POST: Process form submission

**Save with Relationships:**
```python
comment = comment_form.save(commit=False)
comment.post = post
comment.author = request.user
comment.save()
```
- `commit=False`: Don't save to database yet
- Set relationships first
- Then save

**Messages Framework:**
```python
messages.success(request, 'Your comment has been submitted')
```
Shows a success message to the user.

**Redirect:**
```python
return redirect('post_detail', slug=post.slug)
```
- Redirects to post detail page
- Uses URL name, not hard-coded path
- Passes slug parameter

## Step 4: Create Category View

```python
def category_posts(request, slug):
    """List posts in a specific category"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(status='published', category=category).select_related('author')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category_posts.html', context)
```

Simple! Gets category, filters posts, paginates, renders template.

## Step 5: Create Post Management Views

### Create Post View

```python
@login_required
def create_post(request):
    """Create a new blog post"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if post.status == 'published' and not post.published_at:
                post.published_at = timezone.now()
            post.save()
            messages.success(request, 'Your post has been created successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    
    context = {'form': form}
    return render(request, 'blog/create_post.html', context)
```

### Understanding Create Post

**@login_required Decorator:**
```python
@login_required
def create_post(request):
```
Redirects to login if user not authenticated.

**Handle File Uploads:**
```python
form = PostForm(request.POST, request.FILES)
```
`request.FILES` needed for image uploads!

**Set Timestamp:**
```python
if post.status == 'published' and not post.published_at:
    post.published_at = timezone.now()
```
Set published date when publishing.

### Edit Post View

```python
@login_required
def edit_post(request, slug):
    """Edit an existing blog post"""
    post = get_object_or_404(Post, slug=slug)
    
    # Only author or staff can edit
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('post_detail', slug=post.slug)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if post.status == 'published' and not post.published_at:
                post.published_at = timezone.now()
            post.save()
            messages.success(request, 'Your post has been updated successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    context = {'form': form, 'post': post}
    return render(request, 'blog/edit_post.html', context)
```

**Key difference:** `instance=post` pre-fills the form with existing data.

**Permission Check:**
```python
if post.author != request.user and not request.user.is_staff:
    messages.error(request, '...')
    return redirect(...)
```
Only author or staff can edit.

### Delete Post View

```python
@login_required
def delete_post(request, slug):
    """Delete a blog post"""
    post = get_object_or_404(Post, slug=slug)
    
    # Only author or staff can delete
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('post_detail', slug=post.slug)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted.')
        return redirect('home')
    
    context = {'post': post}
    return render(request, 'blog/delete_post.html', context)
```

Shows confirmation page on GET, deletes on POST.

## Step 6: Create User Views

### User's Posts View

```python
@login_required
def user_posts(request):
    """List posts by the logged-in user"""
    posts = Post.objects.filter(author=request.user).select_related('category')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'blog/user_posts.html', context)
```

### Registration View

```python
def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created successfully.')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'blog/register.html', context)
```

**Auto-login After Registration:**
```python
user = form.save()
login(request, user)
```
User is logged in immediately after signup.

## Complete views.py File

Your complete `blog/views.py` should have all these imports and functions. (See the actual file in the project.)

## Understanding Common Patterns

### The Standard View Pattern

```python
def my_view(request):
    # 1. Get data
    objects = Model.objects.filter(...)
    
    # 2. Process/logic
    if some_condition:
        do_something()
    
    # 3. Prepare context
    context = {'objects': objects}
    
    # 4. Render template
    return render(request, 'template.html', context)
```

### The Form View Pattern

```python
def form_view(request):
    if request.method == 'POST':
        # Process form
        form = MyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        # Show empty form
        form = MyForm()
    
    return render(request, 'form.html', {'form': form})
```

### The Detail View Pattern

```python
def detail_view(request, slug):
    # Get object or 404
    obj = get_object_or_404(Model, slug=slug)
    
    # Render with object
    return render(request, 'detail.html', {'object': obj})
```

## URL Naming and Reversing

### Why Name URLs?

```python
# In urls.py
path('posts/', views.post_list, name='post_list')

# In views - redirect by name
return redirect('post_list')

# In templates - link by name
<a href="{% url 'post_list' %}">Posts</a>
```

**Benefits:**
- Change URL path without updating code
- No typos in URLs
- Easier to maintain

### Reversing with Parameters

```python
# In urls.py
path('post/<slug:slug>/', views.post_detail, name='post_detail')

# In views
return redirect('post_detail', slug='my-post')

# In templates
<a href="{% url 'post_detail' slug=post.slug %}">{{ post.title }}</a>
```

## Request and Response Objects

### Request Object

```python
request.method          # 'GET' or 'POST'
request.GET             # URL parameters (dict)
request.POST            # Form data (dict)
request.FILES           # Uploaded files (dict)
request.user            # Current user
request.path            # '/posts/my-post/'
request.META            # HTTP headers, etc.
```

### Response Types

```python
# Render template
return render(request, 'template.html', context)

# Redirect
return redirect('url_name')
return redirect('/posts/')

# HTTP response
from django.http import HttpResponse, JsonResponse
return HttpResponse('Hello')
return JsonResponse({'key': 'value'})

# 404
from django.http import Http404
raise Http404('Not found')
```

## Query Optimization Tips

### Use select_related for ForeignKeys

```python
# Bad - N+1 queries
posts = Post.objects.all()
for post in posts:
    print(post.author.username)  # Query each time!

# Good - 1 query
posts = Post.objects.select_related('author')
for post in posts:
    print(post.author.username)  # No extra query
```

### Use prefetch_related for Reverse Relations

```python
# Bad
posts = Post.objects.all()
for post in posts:
    print(post.comments.count())  # Query each time!

# Good
posts = Post.objects.prefetch_related('comments')
for post in posts:
    print(post.comments.count())  # No extra query
```

## Troubleshooting

### Issue: "Reverse for 'home' not found"
Check URL name in `urls.py` matches what you're using.

### Issue: "Page not found (404)"
- Check URL pattern order
- Verify URL name is correct
- Check slug/ID parameter is passed correctly

### Issue: "'NoneType' object has no attribute"
Use `get_object_or_404` instead of `.get()` to show proper 404 page.

### Issue: Form not saving
Make sure to call `form.save()` and handle `commit=False` if needed.

### Issue: Images not uploading
Include `request.FILES` in form initialization:
```python
form = PostForm(request.POST, request.FILES)
```

## Testing Your Views

Test in the browser:

1. **Test home view:** `http://127.0.0.1:8000/`
2. **Test non-existent post:** `http://127.0.0.1:8000/post/fake-slug/`
   - Should show 404
3. **Test search:** `http://127.0.0.1:8000/?q=python`
4. **Test category filter:** `http://127.0.0.1:8000/?category=technology`

Use Django shell to test:

```python
from django.test import RequestFactory
from blog.views import home

factory = RequestFactory()
request = factory.get('/')
response = home(request)
print(response.status_code)  # Should be 200
```

## Checklist

Before moving on, verify:

- ✅ URLs configured in both `blog/urls.py` and `blog_cms/urls.py`
- ✅ All view functions created
- ✅ URL order correct (specific before dynamic)
- ✅ Forms imported (we'll create these next)
- ✅ @login_required added where needed
- ✅ Permission checks in place
- ✅ Messages framework used

## What You've Learned

- How Django views work
- URL routing and patterns
- URL parameters and converters
- GET vs POST requests
- Form handling in views
- Querysets and filtering
- Pagination
- Permission decorators
- Messages framework
- Redirects vs renders

## Next Steps

Views are done! Now let's create the templates to display the data.

**→ Continue to [06 - Templates and UI](./06-templates-and-ui.md)**

---

## Additional Resources

- [Django Views Documentation](https://docs.djangoproject.com/en/stable/topics/http/views/)
- [URL Dispatcher](https://docs.djangoproject.com/en/stable/topics/http/urls/)
- [Request/Response Objects](https://docs.djangoproject.com/en/stable/ref/request-response/)
