# Tutorial 03: Model Database

## Overview

Di chapter ini, lo bakal belajar cara bikin dan manage database di Django. Ini salah satu bagian paling powerful dari Django!

## Apa itu Model?

Inget pas lo bikin website pake HTML/CSS/JS, datanya dari mana? Pasti lo pikir "ah nanti ambil dari database aja". Tapi:
- **Gimana bikin table database?** Pake SQL?
- **Gimana ambil data?** Nulis query SQL yang ribet?
- **Gimana update data?** SQL lagi?

**Django Model bikin semua itu jadi gampang!**

### Analogi Sederhana

Bayangin lo punya **spreadsheet** (kayak Excel):

| ID | Title | Content | Author | Date |
|----|-------|---------|--------|------|
| 1  | Post 1 | Content 1 | John | 2024-01-01 |
| 2  | Post 2 | Content 2 | Jane | 2024-01-02 |

Di database, ini disebut **table**. Di Django, lo bikin ini pake **Model** (class Python):

```python
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    date = models.DateField()
```

**Keuntungan pake Model:**
- Ga perlu nulis SQL
- Type-safe (ga bakal ada error tipe data)
- Mudah di-maintain
- Bisa validasi data otomatis

## Bikin Model Pertama

### Step 1: Define Model Post

Buka `blog/models.py` dan ganti isinya:

```python
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    """Model buat kategori post (Technology, Programming, dll)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"  # Bentuk plural di admin
        ordering = ['name']  # Urutkan berdasarkan name

    def __str__(self):
        return self.name


class Post(models.Model):
    """Model buat blog post"""
    # Status choices
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    # Fields
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    excerpt = models.TextField(max_length=300, blank=True)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='posts/%Y/%m/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-published_at', '-created_at']  # Urutkan dari terbaru
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Override save buat set published_at otomatis"""
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


class Comment(models.Model):
    """Model buat komentar di post"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  # Urutkan dari terlama

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
```

### Penjelasan Detail

#### Field Types

Django punya banyak field types buat berbagai kebutuhan:

**Text Fields:**
```python
# CharField - Text pendek (ada max_length)
title = models.CharField(max_length=200)  # Kayak <input type="text">

# TextField - Text panjang (ga ada limit)
content = models.TextField()  # Kayak <textarea>

# SlugField - URL-friendly text
slug = models.SlugField()  # Contoh: "my-blog-post" (no spaces/special chars)
```

**Number Fields:**
```python
# IntegerField - Angka bulat
views_count = models.IntegerField(default=0)

# DecimalField - Angka desimal
price = models.DecimalField(max_digits=10, decimal_places=2)  # 99999999.99
```

**Date/Time Fields:**
```python
# DateField - Tanggal aja (2024-01-01)
birth_date = models.DateField()

# DateTimeField - Tanggal + waktu (2024-01-01 14:30:00)
created_at = models.DateTimeField(auto_now_add=True)  # Set sekali pas create
updated_at = models.DateTimeField(auto_now=True)  # Update setiap save
```

**Boolean:**
```python
# BooleanField - True/False
is_approved = models.BooleanField(default=False)  # Kayak checkbox
```

**File/Image:**
```python
# FileField - Upload file apa aja
document = models.FileField(upload_to='documents/')

# ImageField - Upload gambar (validasi gambar otomatis)
photo = models.ImageField(upload_to='photos/')  # Perlu install Pillow
```

#### Field Options

Tiap field bisa punya options:

```python
# max_length - Panjang maksimum (wajib buat CharField)
title = models.CharField(max_length=200)

# blank - Boleh kosong di form
description = models.TextField(blank=True)

# null - Boleh NULL di database
category = models.ForeignKey(..., null=True)

# default - Nilai default
status = models.CharField(default='draft')

# unique - Harus unique (ga boleh duplikat)
email = models.EmailField(unique=True)

# choices - Pilihan terbatas
STATUS_CHOICES = [('draft', 'Draft'), ('published', 'Published')]
status = models.CharField(choices=STATUS_CHOICES)
```

#### Relationships (Hubungan Antar Model)

Ini konsep penting! Di database, ada 3 tipe relationship:

**1. ForeignKey (Many-to-One)**

Banyak post punya satu author:

```python
author = models.ForeignKey(User, on_delete=models.CASCADE)
```

**Penjelasan:**
- Satu user bisa punya banyak post
- Tapi satu post cuma punya satu author
- `on_delete=models.CASCADE` = Kalo user dihapus, post-nya juga ikut kehapus

**Analogi:**
- Kayak relationship "Siswa - Sekolah"
- Banyak siswa di satu sekolah
- Tapi satu siswa cuma di satu sekolah

**2. ManyToManyField (Many-to-Many)**

Banyak post bisa punya banyak tags:

```python
tags = models.ManyToManyField(Tag)
```

**Penjelasan:**
- Satu post bisa punya banyak tags
- Satu tag bisa dipake di banyak post

**Analogi:**
- Kayak relationship "Mahasiswa - Mata Kuliah"
- Satu mahasiswa ambil banyak mata kuliah
- Satu mata kuliah diambil banyak mahasiswa

**3. OneToOneField (One-to-One)**

Satu user punya satu profile:

```python
profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
```

**Penjelasan:**
- Satu user cuma punya satu profile
- Satu profile cuma milik satu user

**Analogi:**
- Kayak relationship "Orang - KTP"
- Satu orang cuma punya satu KTP
- Satu KTP cuma buat satu orang

#### on_delete Options

Apa yang terjadi kalo objek yang di-reference dihapus?

```python
# CASCADE - Hapus juga objek ini
author = models.ForeignKey(User, on_delete=models.CASCADE)
# Kalo user dihapus, post-nya juga kehapus

# SET_NULL - Set jadi NULL
category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
# Kalo category dihapus, post.category jadi NULL

# PROTECT - Ga boleh dihapus
author = models.ForeignKey(User, on_delete=models.PROTECT)
# Kalo masih ada post, user ga bisa dihapus

# SET_DEFAULT - Set ke nilai default
status = models.ForeignKey(Status, on_delete=models.SET_DEFAULT, default=1)
```

### Step 2: Install Pillow (buat ImageField)

```bash
pip install Pillow
```

**Kenapa?** ImageField butuh Pillow buat validasi gambar.

### Step 3: Bikin Migrations

Migrations itu kayak "instruksi" buat Django bikin/update table di database.

```bash
python manage.py makemigrations
```

Output:
```
Migrations for 'blog':
  blog/migrations/0001_initial.py
    - Create model Category
    - Create model Post
    - Create model Comment
```

**Penjelasan:**
- Django bikin file migration di `blog/migrations/`
- File ini berisi instruksi buat bikin table

Check file migration di `blog/migrations/0001_initial.py` - lo bisa liat Django generate SQL otomatis!

### Step 4: Apply Migrations

```bash
python manage.py migrate
```

Output:
```
Running migrations:
  Applying blog.0001_initial... OK
```

**Apa yang terjadi?**
- Django execute migrations
- Bikin table di database (SQLite by default)
- Table: `blog_category`, `blog_post`, `blog_comment`

## Pake Model di Django Shell

Django shell itu kayak console JavaScript di browser, tapi buat Django.

```bash
python manage.py shell
```

### Create Data

```python
# Import models
from blog.models import Category, Post, Comment
from django.contrib.auth.models import User

# Bikin user dulu (buat author)
user = User.objects.create_user(
    username='john',
    email='john@example.com',
    password='password123'
)

# Bikin category
category = Category.objects.create(
    name='Technology',
    slug='technology',
    description='Posts about technology'
)

# Bikin post
post = Post.objects.create(
    title='My First Post',
    slug='my-first-post',
    author=user,
    category=category,
    content='This is my first blog post!',
    excerpt='A brief intro...',
    status='published'
)

print(f"Post created: {post.title}")
```

### Read Data (Query)

```python
# Get semua post
all_posts = Post.objects.all()
print(all_posts)  # <QuerySet [<Post: My First Post>]>

# Get satu post
post = Post.objects.get(slug='my-first-post')
print(post.title)  # My First Post

# Filter post
published_posts = Post.objects.filter(status='published')
tech_posts = Post.objects.filter(category__name='Technology')

# Get post dengan related data
post = Post.objects.select_related('author', 'category').get(slug='my-first-post')
print(post.author.username)  # john
print(post.category.name)  # Technology

# Counting
post_count = Post.objects.filter(status='published').count()
```

**Penjelasan Query:**

```python
# Bandingkan dengan JavaScript array methods:

# Python/Django ORM:
Post.objects.filter(status='published')
# JavaScript:
posts.filter(post => post.status === 'published')

# Python/Django ORM:
Post.objects.get(id=1)
# JavaScript:
posts.find(post => post.id === 1)

# Python/Django ORM:
Post.objects.all()
# JavaScript:
posts  // semua array
```

### Update Data

```python
# Cara 1: Get terus update
post = Post.objects.get(slug='my-first-post')
post.title = 'My Updated Post'
post.save()

# Cara 2: Update langsung (lebih efisien)
Post.objects.filter(slug='my-first-post').update(title='My Updated Post')

# Update banyak sekaligus
Post.objects.filter(status='draft').update(status='published')
```

### Delete Data

```python
# Delete satu objek
post = Post.objects.get(slug='my-first-post')
post.delete()

# Delete banyak sekaligus
Post.objects.filter(status='draft').delete()

# Delete semua (HATI-HATI!)
Post.objects.all().delete()
```

## Field Lookups (Filter Advanced)

Django punya banyak lookup buat filter data:

```python
# Exact match
Post.objects.filter(status='published')
Post.objects.filter(status__exact='published')  # sama aja

# Case-insensitive
Post.objects.filter(title__iexact='my post')  # "My Post", "MY POST", "my post"

# Contains
Post.objects.filter(title__contains='Django')  # Title ada kata "Django"
Post.objects.filter(title__icontains='django')  # Case-insensitive

# Starts with / Ends with
Post.objects.filter(title__startswith='How to')
Post.objects.filter(title__endswith='Tutorial')

# Greater than / Less than
Post.objects.filter(views__gt=100)  # views > 100
Post.objects.filter(views__gte=100)  # views >= 100
Post.objects.filter(views__lt=100)  # views < 100
Post.objects.filter(views__lte=100)  # views <= 100

# In list
Post.objects.filter(status__in=['draft', 'published'])

# Range
from datetime import date
Post.objects.filter(created_at__range=[date(2024, 1, 1), date(2024, 12, 31)])

# NULL checks
Post.objects.filter(category__isnull=True)  # category = NULL
Post.objects.filter(category__isnull=False)  # category != NULL
```

## Related Lookups (Query Relationship)

```python
# Filter post berdasarkan author name
Post.objects.filter(author__username='john')

# Filter post berdasarkan category
Post.objects.filter(category__name='Technology')

# Double underscore buat traverse relationship
Post.objects.filter(category__name__icontains='tech')

# Reverse relationship
user = User.objects.get(username='john')
user_posts = user.blog_posts.all()  # related_name='blog_posts'

# Count related objects
category = Category.objects.get(slug='technology')
post_count = category.posts.count()  # related_name='posts'
```

## QuerySet Methods (Chaining)

Lo bisa chain methods kayak JavaScript:

```python
# JavaScript:
posts
  .filter(post => post.status === 'published')
  .filter(post => post.category === 'Tech')
  .sort((a, b) => b.date - a.date)
  .slice(0, 5)

# Django (mirip!):
Post.objects \
    .filter(status='published') \
    .filter(category__name='Technology') \
    .order_by('-created_at') \
    [:5]
```

**Common methods:**

```python
# Filter
Post.objects.filter(status='published')

# Exclude
Post.objects.exclude(status='draft')  # semua kecuali draft

# Order
Post.objects.order_by('-created_at')  # Descending (tanda -)
Post.objects.order_by('title')  # Ascending

# Limit (slicing)
Post.objects.all()[:5]  # 5 pertama
Post.objects.all()[5:10]  # 5-10

# Distinct
Post.objects.values('category').distinct()

# First / Last
first_post = Post.objects.first()
last_post = Post.objects.last()

# Exists
has_posts = Post.objects.filter(status='published').exists()  # True/False
```

## Aggregate & Annotate

```python
from django.db.models import Count, Avg, Sum, Max, Min

# Count total posts
Post.objects.count()

# Aggregate (summary data)
from django.db.models import Count
stats = Post.objects.aggregate(
    total=Count('id'),
    published=Count('id', filter=Q(status='published'))
)
# Result: {'total': 10, 'published': 7}

# Annotate (add field ke each object)
categories = Category.objects.annotate(post_count=Count('posts'))
for cat in categories:
    print(f"{cat.name}: {cat.post_count} posts")
```

## Q Objects (Complex Queries)

Buat query yang kompleks (OR, NOT):

```python
from django.db.models import Q

# OR
Post.objects.filter(Q(status='published') | Q(status='archived'))
# SQL: WHERE status='published' OR status='archived'

# AND
Post.objects.filter(Q(status='published') & Q(category__name='Tech'))
# Sama kayak: Post.objects.filter(status='published', category__name='Tech')

# NOT
Post.objects.filter(~Q(status='draft'))
# SQL: WHERE NOT status='draft'

# Complex combination
Post.objects.filter(
    Q(status='published') & (Q(category__name='Tech') | Q(category__name='Programming'))
)
# Published posts in Tech OR Programming category
```

## Model Methods & Properties

Lo bisa tambahin custom methods ke model:

```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_excerpt(self, length=100):
        """Get excerpt dari content"""
        if len(self.content) > length:
            return self.content[:length] + '...'
        return self.content

    @property
    def word_count(self):
        """Count words di content"""
        return len(self.content.split())

    def is_recent(self):
        """Check apakah post dibuat dalam 7 hari terakhir"""
        from datetime import timedelta
        from django.utils import timezone
        return self.created_at >= timezone.now() - timedelta(days=7)
```

Pake di code:

```python
post = Post.objects.get(id=1)
print(post.get_excerpt(50))  # First 50 chars
print(post.word_count)  # Property (ga perlu ())
print(post.is_recent())  # Method (perlu ())
```

## Kesimpulan

Lo udah belajar:

✅ Apa itu Model dan kenapa pake ORM  
✅ Field types dan options  
✅ Relationships (ForeignKey, ManyToMany, OneToOne)  
✅ Bikin dan apply migrations  
✅ CRUD operations (Create, Read, Update, Delete)  
✅ Query filtering dan lookups  
✅ Related queries  
✅ Aggregate dan annotate  
✅ Custom model methods  

### Perbandingan dengan JavaScript

| Konsep | Django ORM | JavaScript |
|--------|-----------|------------|
| Get all | `Post.objects.all()` | `posts` |
| Filter | `Post.objects.filter(status='published')` | `posts.filter(p => p.status === 'published')` |
| Find one | `Post.objects.get(id=1)` | `posts.find(p => p.id === 1)` |
| Count | `Post.objects.count()` | `posts.length` |
| Order | `Post.objects.order_by('-date')` | `posts.sort((a,b) => b.date - a.date)` |
| Slice | `Post.objects.all()[:5]` | `posts.slice(0, 5)` |

## Next Steps

Di [Chapter 4](./04-django-admin.md), lo bakal belajar:
- Register model ke admin panel
- Customisasi admin interface
- Manage data lewat admin panel
- Admin actions

Siap? Let's go! 🚀

## Troubleshooting

### Error: "No such table: blog_post"
**Solusi:** Lo belum run migrations. Jalanin `python manage.py migrate`

### Error: "UNIQUE constraint failed"
**Solusi:** Lo coba create object dengan value yang harus unique tapi udah ada. Check field `unique=True`

### Error: "RelatedObjectDoesNotExist"
**Solusi:** Lo akses related object yang ga ada. Pake `hasattr()` atau try-except

### Migration conflicts
**Solusi:** Hapus file migration di `blog/migrations/` (kecuali `__init__.py`), terus bikin ulang
