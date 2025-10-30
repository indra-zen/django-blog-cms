# Tutorial 05: Views dan Templates

## Overview

Di chapter ini, lo bakal belajar cara bikin halaman-halaman di website lo dengan Views dan Templates. Ini inti dari web development di Django!

## Apa itu Views?

Inget pas lo bikin website pake JavaScript, lo pasti bikin function yang handle event kan? Misal:

```javascript
// JavaScript
function showBlogPosts() {
    // Ambil data
    const posts = fetch('/api/posts');
    // Render ke HTML
    displayPosts(posts);
}
```

**Django Views mirip banget!** Bedanya, Views di Django:
- Jalan di **server** (bukan browser)
- Return **HTML lengkap** (bukan cuma data JSON)
- Handle **request** dari user dan return **response**

### Analogi Sederhana

```
User klik link → Request ke Server → View function jalan → Return HTML → Browser render
```

Kayak waiter di restoran:
1. Lo (user) pesan makanan
2. Waiter (view) terima pesanan
3. Waiter ambil makanan dari dapur (database)
4. Waiter kasih makanan ke lo (HTML response)

## Function-Based Views (FBV)

View paling sederhana: function Python biasa.

### Example: List Posts

Buka `blog/views.py`:

```python
from django.shortcuts import render
from .models import Post

def home(request):
    """View buat homepage - tampilkan semua published posts"""
    # Ambil data dari database
    posts = Post.objects.filter(status='published').order_by('-published_at')
    
    # Kirim ke template
    context = {
        'posts': posts,
        'page_title': 'Home - My Blog'
    }
    return render(request, 'blog/home.html', context)
```

**Penjelasan:**
- `request` = Object berisi info tentang HTTP request (method, user, cookies, dll)
- `context` = Dictionary data yang dikirim ke template
- `render()` = Function yang render template dengan context

### Example: Post Detail

```python
from django.shortcuts import render, get_object_or_404

def post_detail(request, slug):
    """View buat detail satu post"""
    # Get post atau 404 kalo ga ada
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Get comments yang approved
    comments = post.comments.filter(is_approved=True)
    
    context = {
        'post': post,
        'comments': comments,
        'page_title': post.title
    }
    return render(request, 'blog/post_detail.html', context)
```

**`get_object_or_404`:**
- Kalo post ditemukan → return post
- Kalo ga ketemu → return error 404 (not found)

### Setup URLs

Bikin `blog/urls.py`:

```python
from django.urls import path
from . import views

app_name = 'blog'  # Namespace buat URLs

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
]
```

**Penjelasan URL patterns:**

```python
# Static URL
path('about/', views.about)
# Match: /about/

# Dynamic URL dengan parameter
path('post/<int:id>/', views.post_detail)
# Match: /post/1/, /post/2/, /post/123/
# Parameter 'id' dikirim ke view function

path('post/<slug:slug>/', views.post_detail)
# Match: /post/my-first-post/, /post/django-tutorial/
# Parameter 'slug' dikirim ke view function

# Multiple parameters
path('category/<slug:category_slug>/page/<int:page>/', views.category_posts)
# Match: /category/technology/page/2/
```

Include di `blog_cms/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # Include blog URLs
]
```

## Templates

Template itu file HTML yang bisa punya:
- **Variables** dari context
- **Logic** (loops, conditions)
- **Template inheritance** (DRY - Don't Repeat Yourself)

### Template Syntax

**1. Variables:**
```html
<!-- Print variabel -->
<h1>{{ post.title }}</h1>
<p>{{ post.content }}</p>

<!-- Akses attributes/methods -->
<p>By {{ post.author.username }}</p>
<p>{{ post.created_at|date:"M d, Y" }}</p>
```

**2. Filters (Modifikasi output):**
```html
<!-- Uppercase -->
{{ post.title|upper }}  <!-- MY BLOG POST -->

<!-- Lowercase -->
{{ post.title|lower }}  <!-- my blog post -->

<!-- Truncate -->
{{ post.content|truncatewords:30 }}  <!-- First 30 words... -->

<!-- Date formatting -->
{{ post.created_at|date:"F j, Y" }}  <!-- January 1, 2024 -->

<!-- Default value kalo empty -->
{{ post.excerpt|default:"No excerpt available" }}

<!-- Length -->
{{ post.title|length }}  <!-- 15 -->

<!-- Safe (render HTML) -->
{{ post.content|safe }}  <!-- Render HTML tags -->
```

**3. Tags (Logic):**
```html
<!-- For loop -->
{% for post in posts %}
    <h2>{{ post.title }}</h2>
{% endfor %}

<!-- If condition -->
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
{% else %}
    <p>Please login</p>
{% endif %}

<!-- If with multiple conditions -->
{% if post.status == 'published' and post.featured %}
    <span class="badge">Featured</span>
{% endif %}

<!-- Empty check -->
{% if posts %}
    {% for post in posts %}
        <!-- Show posts -->
    {% endfor %}
{% else %}
    <p>No posts yet.</p>
{% endif %}

<!-- For loop dengan empty -->
{% for post in posts %}
    <h2>{{ post.title }}</h2>
{% empty %}
    <p>No posts found.</p>
{% endfor %}
```

### Template Inheritance (Super Penting!)

Biar ga repeat code, pake template inheritance.

**Base template** (`blog/templates/blog/base.html`):

```html
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Blog{% endblock %}</title>
    
    <!-- CSS -->
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f4f4f4;
        }
        
        nav {
            background: #333;
            color: #fff;
            padding: 1rem;
        }
        
        nav a {
            color: #fff;
            text-decoration: none;
            margin-right: 1rem;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        {% block extra_css %}{% endblock %}
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav>
        <div class="container">
            <a href="{% url 'blog:home' %}">Home</a>
            <a href="{% url 'blog:about' %}">About</a>
            
            {% if user.is_authenticated %}
                <a href="{% url 'blog:create_post' %}">New Post</a>
                <a href="{% url 'blog:logout' %}">Logout ({{ user.username }})</a>
            {% else %}
                <a href="{% url 'blog:login' %}">Login</a>
                <a href="{% url 'blog:register' %}">Register</a>
            {% endif %}
        </div>
    </nav>

    <!-- Messages (buat notifications) -->
    {% if messages %}
        <div class="messages">
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }}">
                    {{ message }}
                </div>
            {% endfor %}
        </div>
    {% endif %}

    <!-- Main content -->
    <div class="container">
        {% block content %}
        {% endblock %}
    </div>

    <!-- Footer -->
    <footer>
        <div class="container">
            <p>&copy; 2024 My Blog. All rights reserved.</p>
        </div>
    </footer>

    {% block extra_js %}{% endblock %}
</body>
</html>
```

**Child template** (`blog/templates/blog/home.html`):

```html
{% extends 'blog/base.html' %}

{% block title %}Home - My Blog{% endblock %}

{% block content %}
    <h1>Welcome to My Blog! 🚀</h1>
    
    {% if posts %}
        <div class="posts">
            {% for post in posts %}
                <article class="post">
                    {% if post.featured_image %}
                        <img src="{{ post.featured_image.url }}" alt="{{ post.title }}">
                    {% endif %}
                    
                    <h2>
                        <a href="{% url 'blog:post_detail' slug=post.slug %}">
                            {{ post.title }}
                        </a>
                    </h2>
                    
                    <div class="meta">
                        <span>By {{ post.author.username }}</span>
                        <span>{{ post.published_at|date:"M d, Y" }}</span>
                        <span>{{ post.category.name }}</span>
                    </div>
                    
                    <p>{{ post.excerpt|truncatewords:30 }}</p>
                    
                    <a href="{% url 'blog:post_detail' slug=post.slug %}" class="read-more">
                        Read More →
                    </a>
                </article>
            {% endfor %}
        </div>
    {% else %}
        <p>No posts yet. Be the first to post!</p>
    {% endif %}
{% endblock %}

{% block extra_css %}
<style>
    .posts {
        display: grid;
        gap: 2rem;
    }
    
    .post {
        background: white;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .post img {
        width: 100%;
        height: 300px;
        object-fit: cover;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
    
    .post h2 {
        margin-bottom: 0.5rem;
    }
    
    .post h2 a {
        color: #333;
        text-decoration: none;
    }
    
    .post h2 a:hover {
        color: #007bff;
    }
    
    .meta {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    .meta span {
        margin-right: 1rem;
    }
    
    .read-more {
        display: inline-block;
        margin-top: 1rem;
        color: #007bff;
        text-decoration: none;
    }
</style>
{% endblock %}
```

**Penjelasan:**
- `{% extends 'blog/base.html' %}` = Pake base template
- `{% block title %}...{% endblock %}` = Override block dari base
- `{% block content %}...{% endblock %}` = Isi content block
- Semua HTML dari base (nav, footer, dll) otomatis included!

### URL Reverse

Jangan hardcode URLs! Pake `{% url %}` tag:

```html
<!-- ❌ BAD - Hardcoded -->
<a href="/post/my-post/">Read More</a>

<!-- ✅ GOOD - Dynamic -->
<a href="{% url 'blog:post_detail' slug=post.slug %}">Read More</a>

<!-- No parameters -->
<a href="{% url 'blog:home' %}">Home</a>

<!-- With parameters -->
<a href="{% url 'blog:post_detail' slug='my-post' %}">Post</a>
<a href="{% url 'blog:category' slug=category.slug %}">{{ category.name }}</a>
```

**Keuntungan:**
- Kalo URL pattern berubah, ga perlu update di semua template
- Typo-proof (error kalo URL ga ada)

## Class-Based Views (CBV)

Alternative dari function-based views. Lebih powerful tapi lebih complex.

### ListView

Tampilkan list objects:

```python
from django.views.generic import ListView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'  # Default: 'object_list'
    paginate_by = 10  # Pagination
    
    def get_queryset(self):
        """Override queryset - filter published only"""
        return Post.objects.filter(status='published').order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        """Add extra context"""
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Home'
        context['categories'] = Category.objects.all()
        return context
```

URL:
```python
from .views import PostListView

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
]
```

### DetailView

Tampilkan detail satu object:

```python
from django.views.generic import DetailView

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        """Only show published posts"""
        return Post.objects.filter(status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add comments
        context['comments'] = self.object.comments.filter(is_approved=True)
        return context
```

URL:
```python
path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
```

### CreateView

Bikin object baru:

```python
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import PostForm

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create_post.html'
    success_url = reverse_lazy('blog:home')
    
    def form_valid(self, form):
        """Set author before saving"""
        form.instance.author = self.request.user
        return super().form_valid(form)
```

### UpdateView & DeleteView

```python
from django.views.generic.edit import UpdateView, DeleteView

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/edit_post.html'
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.object.slug})

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog:home')
```

## Static Files (CSS, JS, Images)

### Setup

1. Bikin folder `static/css/style.css`:

```css
/* static/css/style.css */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

/* Add more styles... */
```

2. Load di template:

```html
{% load static %}

<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <img src="{% static 'images/logo.png' %}" alt="Logo">
    <script src="{% static 'js/main.js' %}"></script>
</body>
</html>
```

**Penjelasan:**
- `{% load static %}` = Load static tag
- `{% static 'path/to/file' %}` = Generate URL ke static file
- Di production, Django collect semua static files ke satu folder

## Request & Response

### Request Object

```python
def my_view(request):
    # HTTP method
    if request.method == 'POST':
        # Handle form submission
        pass
    
    # GET parameters (?search=django&page=2)
    search = request.GET.get('search', '')
    page = request.GET.get('page', 1)
    
    # POST data (dari form)
    username = request.POST.get('username')
    
    # User info
    user = request.user  # Current user
    is_authenticated = request.user.is_authenticated
    
    # Path info
    path = request.path  # /blog/post/1/
    full_path = request.get_full_path()  # /blog/post/1/?page=2
    
    # Headers
    user_agent = request.META.get('HTTP_USER_AGENT')
    
    # Session & Cookies
    request.session['key'] = 'value'
    cookie = request.COOKIES.get('name')
```

### Response Types

```python
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

def my_view(request):
    # HTML response (paling umum)
    return render(request, 'template.html', context)
    
    # Plain text
    return HttpResponse('Hello World')
    
    # JSON response (buat API)
    data = {'status': 'success', 'message': 'OK'}
    return JsonResponse(data)
    
    # Redirect
    return redirect('blog:home')  # Pake URL name
    return redirect('/some/url/')  # Hardcoded URL
    return HttpResponseRedirect('/some/url/')
    
    # 404 Error
    from django.http import Http404
    raise Http404('Post not found')
```

## Kesimpulan

Lo udah belajar:

✅ Function-based views (FBV)  
✅ URL routing dan parameters  
✅ Template syntax (variables, filters, tags)  
✅ Template inheritance  
✅ Class-based views (CBV)  
✅ Static files  
✅ Request/Response objects  

### Kapan Pake FBV vs CBV?

**Function-Based Views:**
- ✅ Simple dan straightforward
- ✅ Easy to understand (especially buat pemula)
- ✅ Flexible
- ❌ Banyak boilerplate code

**Class-Based Views:**
- ✅ Less code (reusable)
- ✅ Built-in functionality (pagination, forms, dll)
- ❌ Harder to understand awalnya
- ❌ Less flexible

**Rekomendasi:** Mulai dari FBV dulu, nanti pake CBV kalo udah nyaman.

## Next Steps

Di [Chapter 6](./06-templates-ui.md), lo bakal belajar:
- Template best practices
- Custom template tags & filters
- Advanced template techniques

Dan di [Chapter 7](./07-forms.md):
- Handle form input
- Form validation
- File uploads

Siap lanjut? Let's go! 🚀
