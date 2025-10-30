# Django Cheat Sheet - Bahasa Indonesia 🚀

Quick reference buat command dan syntax Django yang sering dipake!

## 📋 Table of Contents

- [Commands Django](#commands-django)
- [Model Fields](#model-fields)
- [QuerySet API](#queryset-api)
- [Template Syntax](#template-syntax)
- [Views](#views)
- [URLs](#urls)
- [Forms](#forms)

---

## Commands Django

### Setup Project
```bash
# Install Django
pip install django

# Bikin project baru
django-admin startproject myproject

# Bikin app baru
python manage.py startapp myapp

# Jalanin development server
python manage.py runserver

# Jalanin di port lain
python manage.py runserver 8080
```

### Database
```bash
# Bikin migrations (detect changes di models)
python manage.py makemigrations

# Apply migrations (execute ke database)
python manage.py migrate

# Liat SQL yang akan dijalanin
python manage.py sqlmigrate myapp 0001

# Check migrations yang udah/belum jalan
python manage.py showmigrations
```

### User Management
```bash
# Bikin superuser (admin)
python manage.py createsuperuser

# Change password user
python manage.py changepassword username
```

### Django Shell
```bash
# Buka interactive Python shell dengan Django
python manage.py shell

# Di shell:
>>> from blog.models import Post
>>> Post.objects.all()
>>> exit()
```

### Static Files
```bash
# Collect semua static files ke satu folder (production)
python manage.py collectstatic
```

### Testing
```bash
# Jalanin semua tests
python manage.py test

# Test app tertentu
python manage.py test myapp

# Test dengan verbosity
python manage.py test --verbosity=2
```

### Custom Commands
```bash
# Jalanin custom management command
python manage.py my_custom_command

# Contoh: bikin sample data
python manage.py create_sample_data
```

---

## Model Fields

### Text Fields
```python
from django.db import models

# CharField - text pendek (HARUS ada max_length)
title = models.CharField(max_length=200)

# TextField - text panjang (no limit)
content = models.TextField()

# SlugField - URL-friendly text
slug = models.SlugField(unique=True)

# EmailField - validasi email
email = models.EmailField()

# URLField - validasi URL
website = models.URLField()
```

### Number Fields
```python
# IntegerField - integer
count = models.IntegerField(default=0)

# DecimalField - decimal dengan precision
price = models.DecimalField(max_digits=10, decimal_places=2)

# FloatField - floating point
rating = models.FloatField()
```

### Boolean
```python
# BooleanField - True/False
is_published = models.BooleanField(default=False)
```

### Date/Time
```python
# DateField - date aja
birth_date = models.DateField()

# DateTimeField - date + time
created_at = models.DateTimeField(auto_now_add=True)  # Set once
updated_at = models.DateTimeField(auto_now=True)      # Update every save
```

### Files
```python
# FileField - any file
document = models.FileField(upload_to='documents/')

# ImageField - image file (butuh Pillow)
photo = models.ImageField(upload_to='photos/')
```

### Relationships
```python
# ForeignKey - Many to One
author = models.ForeignKey(User, on_delete=models.CASCADE)

# ManyToManyField - Many to Many
tags = models.ManyToManyField(Tag)

# OneToOneField - One to One
profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
```

### Field Options
```python
# null - allow NULL di database
category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

# blank - allow empty di forms
bio = models.TextField(blank=True)

# default - nilai default
status = models.CharField(default='draft')

# unique - harus unique
email = models.EmailField(unique=True)

# choices - pilihan terbatas
STATUS_CHOICES = [('draft', 'Draft'), ('published', 'Published')]
status = models.CharField(choices=STATUS_CHOICES)

# db_index - bikin index di database (faster queries)
slug = models.SlugField(db_index=True)

# help_text - text bantuan di forms
title = models.CharField(help_text="Enter the post title")
```

---

## QuerySet API

### Get Data
```python
# Get semua
Post.objects.all()

# Get satu object
Post.objects.get(id=1)
Post.objects.get(slug='my-post')

# Filter (multiple results)
Post.objects.filter(status='published')
Post.objects.filter(status='published', category__name='Tech')

# Exclude
Post.objects.exclude(status='draft')

# First / Last
Post.objects.first()
Post.objects.last()

# Check exists
Post.objects.filter(slug='my-post').exists()  # True/False

# Count
Post.objects.filter(status='published').count()
```

### Field Lookups
```python
# Exact match
Post.objects.filter(status='published')
Post.objects.filter(status__exact='published')  # sama aja

# Case-insensitive
Post.objects.filter(title__iexact='my post')

# Contains
Post.objects.filter(title__contains='Django')
Post.objects.filter(title__icontains='django')  # case-insensitive

# Starts with / Ends with
Post.objects.filter(title__startswith='How to')
Post.objects.filter(title__endswith='Tutorial')

# Greater than / Less than
Post.objects.filter(views__gt=100)   # >
Post.objects.filter(views__gte=100)  # >=
Post.objects.filter(views__lt=100)   # <
Post.objects.filter(views__lte=100)  # <=

# In list
Post.objects.filter(status__in=['draft', 'published'])

# Range
Post.objects.filter(created_at__range=[start_date, end_date])

# NULL checks
Post.objects.filter(category__isnull=True)
Post.objects.filter(category__isnull=False)
```

### Related Lookups
```python
# Query by related field
Post.objects.filter(author__username='john')
Post.objects.filter(category__name='Technology')

# Double underscore untuk traverse
Post.objects.filter(author__profile__country='Indonesia')
```

### Ordering
```python
# Order ascending
Post.objects.order_by('created_at')

# Order descending (minus sign)
Post.objects.order_by('-created_at')

# Multiple ordering
Post.objects.order_by('-created_at', 'title')

# Random order
Post.objects.order_by('?')
```

### Limit (Slicing)
```python
# First 5
Post.objects.all()[:5]

# 6-10
Post.objects.all()[5:10]

# PERHATIAN: negative indexing ga bisa!
# Post.objects.all()[-1]  # ERROR!
```

### Chaining
```python
# Chain multiple methods
Post.objects.filter(status='published') \
           .exclude(category__name='Archive') \
           .order_by('-created_at') \
           [:10]
```

### Create / Update / Delete
```python
# Create
post = Post.objects.create(
    title='My Post',
    content='Content here',
    author=user
)

# Update satu object
post = Post.objects.get(id=1)
post.title = 'New Title'
post.save()

# Update multiple
Post.objects.filter(status='draft').update(status='published')

# Delete satu object
post = Post.objects.get(id=1)
post.delete()

# Delete multiple
Post.objects.filter(status='draft').delete()
```

### Aggregate & Annotate
```python
from django.db.models import Count, Avg, Sum, Max, Min

# Aggregate (summary data)
Post.objects.aggregate(total=Count('id'))
Post.objects.aggregate(avg_views=Avg('views'))

# Annotate (add field to each object)
categories = Category.objects.annotate(post_count=Count('posts'))
for cat in categories:
    print(f"{cat.name}: {cat.post_count}")
```

---

## Template Syntax

### Variables
```django
{# Print variabel #}
{{ variable }}
{{ post.title }}
{{ user.username }}

{# Akses dictionary #}
{{ my_dict.key }}

{# Akses list #}
{{ my_list.0 }}
```

### Filters
```django
{# String manipulation #}
{{ name|upper }}           <!-- JOHN -->
{{ name|lower }}           <!-- john -->
{{ name|title }}           <!-- John Smith -->
{{ name|capfirst }}        <!-- John -->

{# Truncate #}
{{ text|truncatewords:30 }}      <!-- First 30 words... -->
{{ text|truncatechars:100 }}     <!-- First 100 chars... -->

{# Default value #}
{{ value|default:"N/A" }}

{# Length #}
{{ list|length }}

{# Date formatting #}
{{ date|date:"Y-m-d" }}           <!-- 2024-01-01 -->
{{ date|date:"F j, Y" }}          <!-- January 1, 2024 -->

{# Join #}
{{ list|join:", " }}

{# Safe (render HTML) #}
{{ html_content|safe }}

{# Linebreaks (convert \n to <br>) #}
{{ text|linebreaks }}
```

### Tags

#### For Loop
```django
{% for item in items %}
    <p>{{ item }}</p>
{% endfor %}

{# With empty #}
{% for post in posts %}
    <h2>{{ post.title }}</h2>
{% empty %}
    <p>No posts yet.</p>
{% endfor %}

{# Loop variables #}
{% for item in items %}
    {{ forloop.counter }}      <!-- 1, 2, 3, ... -->
    {{ forloop.counter0 }}     <!-- 0, 1, 2, ... -->
    {{ forloop.first }}        <!-- True on first iteration -->
    {{ forloop.last }}         <!-- True on last iteration -->
{% endfor %}
```

#### If Statement
```django
{% if condition %}
    <p>True</p>
{% endif %}

{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
{% else %}
    <p>Please login</p>
{% endif %}

{# Multiple conditions #}
{% if age >= 18 and has_license %}
    <p>Can drive</p>
{% elif age >= 18 %}
    <p>Need license</p>
{% else %}
    <p>Too young</p>
{% endif %}

{# Operators #}
{% if a == b %}     <!-- equal -->
{% if a != b %}     <!-- not equal -->
{% if a < b %}      <!-- less than -->
{% if a > b %}      <!-- greater than -->
{% if a <= b %}     <!-- less than or equal -->
{% if a >= b %}     <!-- greater than or equal -->
{% if a in list %}  <!-- in -->
{% if not condition %} <!-- not -->
```

#### URL
```django
{# Simple #}
<a href="{% url 'home' %}">Home</a>

{# With args #}
<a href="{% url 'post_detail' slug=post.slug %}">Read</a>
<a href="{% url 'post_detail' slug='my-post' %}">Read</a>

{# With namespace #}
<a href="{% url 'blog:post_detail' slug=post.slug %}">Read</a>
```

#### Template Inheritance
```django
{# base.html #}
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Site{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>

{# home.html #}
{% extends 'base.html' %}

{% block title %}Home - My Site{% endblock %}

{% block content %}
    <h1>Welcome!</h1>
{% endblock %}
```

#### Include
```django
{% include 'partials/navbar.html' %}
{% include 'partials/footer.html' %}
```

#### Static Files
```django
{% load static %}

<link rel="stylesheet" href="{% static 'css/style.css' %}">
<img src="{% static 'images/logo.png' %}">
<script src="{% static 'js/main.js' %}"></script>
```

#### Comments
```django
{# Single line comment #}

{% comment %}
Multi-line
comment
{% endcomment %}
```

---

## Views

### Function-Based Views
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse

def home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'home.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'post_detail.html', {'post': post})

def api_data(request):
    data = {'status': 'success', 'data': [...]}
    return JsonResponse(data)
```

### Class-Based Views
```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# ListView
class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

# DetailView
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

# CreateView
class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'post_form.html'
    success_url = '/posts/'
```

---

## URLs

```python
from django.urls import path, include
from . import views

app_name = 'blog'  # namespace

urlpatterns = [
    # Simple
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    
    # With parameters
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/', views.post_by_slug, name='post_by_slug'),
    
    # Class-based views
    path('posts/', PostListView.as_view(), name='post_list'),
    
    # Include other URLs
    path('blog/', include('blog.urls')),
]
```

**Parameter types:**
- `<int:name>` - integer
- `<str:name>` - string
- `<slug:name>` - slug (letters, numbers, hyphens, underscores)
- `<uuid:name>` - UUID

---

## Forms

### ModelForm
```python
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'status']
        # atau
        exclude = ['author', 'created_at']
        
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
        labels = {
            'title': 'Post Title',
        }
        
        help_texts = {
            'title': 'Enter a catchy title',
        }

# Di view
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'create_post.html', {'form': form})
```

### Regular Form
```python
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@example.com'):
            raise forms.ValidationError('Must use example.com email')
        return email
```

### Render Form di Template
```django
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    
    {# Render all fields #}
    {{ form.as_p }}
    
    {# Or render individual fields #}
    {{ form.title }}
    {{ form.content }}
    
    {# With labels and errors #}
    <div>
        {{ form.title.label_tag }}
        {{ form.title }}
        {{ form.title.errors }}
    </div>
    
    <button type="submit">Submit</button>
</form>
```

---

## Tips & Best Practices

### Development
```bash
# Always work di virtual environment
python -m venv venv
source venv/bin/activate  # atau venv\Scripts\activate

# Freeze dependencies
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

### Security
```python
# settings.py

# NEVER commit SECRET_KEY
SECRET_KEY = os.environ.get('SECRET_KEY')

# Production settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Performance
```python
# Use select_related for ForeignKey
posts = Post.objects.select_related('author', 'category').all()

# Use prefetch_related for ManyToMany
posts = Post.objects.prefetch_related('tags').all()

# Don't repeat queries
posts = Post.objects.all()  # Query once
for post in posts:
    print(post.title)  # No additional queries
```

---

**Bookmark page ini!** Bakal sering lo pake pas ngoding Django! 🔖

Made with ❤️ for Indonesian Django developers!
