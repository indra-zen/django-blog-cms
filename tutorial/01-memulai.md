# Tutorial 01: Memulai dengan Django

## Overview

Di bagian ini, lo bakal setup development environment dan pahamin konsep dasar Django web development.

## Apa itu Django?

Bayangin gini - lo udah bisa bikin website pake HTML, CSS, dan JavaScript kan? Nah, itu artinya lo bisa bikin tampilan website yang keren. Tapi ada masalahnya:

- **Data dari mana?** Lo bikin HTML statis, kontennya ga bisa berubah-ubah
- **User gimana login?** JavaScript doang ga cukup buat handle authentication yang aman
- **Database gimana?** Lo perlu simpan data user, post blog, dll

**Nah, di sinilah Django masuk!**

Django itu framework Python buat bikin website yang **dinamis** dan **full-stack**. Artinya:
- Lo bisa simpan dan ambil data dari database
- Lo bisa handle user login/logout dengan aman
- Lo bisa generate HTML secara otomatis dengan data yang berubah-ubah
- Lo bisa bikin API buat frontend lo

### Analogi Sederhana

Kalo lo bikin website pake HTML/CSS/JS doang, itu kayak:
- **HTML/CSS/JS** = Toko offline yang tampilan-nya bagus tapi datanya tetap (statis)

Kalo pake Django:
- **Django** = Toko online lengkap dengan database barang, sistem login, shopping cart, dll (dinamis)
- **HTML/CSS/JS** = Masih dipake buat tampilan, tapi sekarang kontennya bisa berubah dari database

## Apa yang Django Kasih ke Lo?

Django include banyak hal yang udah jadi:

1. **ORM (Object-Relational Mapping):** Kerja sama database pake Python, ga perlu nulis SQL
2. **Admin Interface:** Dashboard admin gratis buat manage konten
3. **Authentication System:** User login/logout udah built-in
4. **URL Routing:** Atur URL website lo dengan gampang
5. **Template Engine:** Bikin HTML yang dinamis (kayak variabel di HTML)
6. **Security Features:** Proteksi dari hacking (SQL injection, XSS, CSRF, dll)

## Arsitektur: MTV Pattern (Model-Template-View)

Lo mungkin denger MVC (Model-View-Controller) di JavaScript framework. Django pake **MTV** yang mirip tapi beda nama:

```
┌─────────────────────────────────────────┐
│         Browser (User)                   │
│    "Gue mau lihat halaman blog"         │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│            URLs                          │
│    "OK, request ini ke View mana ya?"   │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│            Views                         │
│  "Ambil data dari Model, terus kasih    │
│   ke Template buat di-render"           │
└────┬───────────────────────────┬────────┘
     │                           │
     ▼                           ▼
┌─────────┐               ┌──────────┐
│ Models  │               │Templates │
│(Database)               │  (HTML)  │
│ "Data   │               │ "Tampilin│
│  blog"  │               │  data"   │
└─────────┘               └──────────┘
```

### Jelasin Lebih Detail:

1. **Models (Database)** 
   - Tempat lo define struktur data (kayak table di database)
   - Contoh: Model `BlogPost` punya field `title`, `content`, `author`, dll
   - Lo ga perlu nulis SQL, tinggal pake Python aja

2. **Templates (HTML Dinamis)**
   - File HTML lo yang bisa punya **variabel** dan **logic**
   - Contoh: `<h1>{{ post.title }}</h1>` - title diambil dari database
   - Kayak HTML biasa tapi bisa ada variabel Python di dalamnya

3. **Views (Logic/Controller)**
   - Fungsi Python yang handle request dari user
   - Ambil data dari Model, terus kirim ke Template
   - Contoh: Ambil semua blog post dari database, terus render ke halaman

### Contoh Flow:

1. User buka `http://website.com/blog/`
2. Django liat di **URLs**: "Oh, `/blog/` harus ke view `blog_list`"
3. **View** `blog_list` jalan:
   - Ambil semua blog post dari **Model** (database)
   - Kirim data itu ke **Template** `blog_list.html`
4. **Template** render HTML dengan data dari database
5. User liat halaman blog dengan list semua post

## Perbandingan dengan Yang Lo Udah Tau

### HTML/CSS/JavaScript Biasa:
```html
<!-- index.html - STATIS -->
<h1>Welcome to My Blog</h1>
<div class="post">
  <h2>Post Title 1</h2>
  <p>Konten post...</p>
</div>
<div class="post">
  <h2>Post Title 2</h2>
  <p>Konten post...</p>
</div>
```
**Masalah:** Harus edit HTML manual tiap kali ada post baru!

### Dengan Django:
```html
<!-- blog_list.html - DINAMIS -->
<h1>Welcome to My Blog</h1>
{% for post in posts %}
  <div class="post">
    <h2>{{ post.title }}</h2>
    <p>{{ post.content }}</p>
  </div>
{% endfor %}
```
**Keuntungan:** Post diambil dari database otomatis! Tinggal tambahin di admin panel.

## Setup Environment

### Step 1: Check Python Installation

Buka terminal/command prompt lo, terus cek Python udah ada belum:

```bash
python --version
# atau
python3 --version
```

Lo perlu **Python 3.8 atau lebih baru**. Kalo belum ada, download di [python.org](https://www.python.org/).

**Note buat temen lo yang baru belajar:** Python itu bahasa programming yang gampang dipelajari. Kalo belum ngerti Python, belajar basic-nya dulu sekitar 1-2 minggu (variables, functions, loops, classes).

### Step 2: Bikin Folder Project

```bash
mkdir django-blog-tutorial
cd django-blog-tutorial
```

**Penjelasan:**
- `mkdir` = make directory (bikin folder)
- `cd` = change directory (masuk ke folder)

### Step 3: Bikin Virtual Environment

Virtual environment itu kayak "kotak terpisah" buat install package Python. Kenapa perlu?
- Tiap project punya dependencies sendiri
- Ga ganggu project lain
- Gampang manage versi package

```bash
# Bikin virtual environment
python -m venv venv

# Aktifin
# Di macOS/Linux:
source venv/bin/activate

# Di Windows:
venv\Scripts\activate
```

Kalo berhasil, lo bakal liat `(venv)` di awal baris terminal lo.

**Tips:** Setiap kali lo buka terminal baru, harus aktifin venv lagi pake command di atas!

### Step 4: Install Django

```bash
pip install --upgrade pip
pip install Django
```

**Penjelasan:**
- `pip` = package manager Python (kayak npm di JavaScript)
- Command di atas install Django versi terbaru

Verify instalasi:

```bash
python -m django --version
```

Harusnya keluar versi Django (misal: 4.2.7)

## Bikin Project Django Pertama

### Step 1: Create Project

```bash
django-admin startproject blog_cms .
```

**Penjelasan:**
- `django-admin` = tool buat bikin project Django
- `startproject blog_cms` = bikin project namanya "blog_cms"
- `.` = bikin di folder current (jangan bikin folder baru lagi)

### Step 2: Struktur Project

Lo bakal liat struktur kayak gini:

```
django-blog-tutorial/
├── venv/                    # Virtual environment (jangan disentuh)
├── blog_cms/                # Folder konfigurasi project
│   ├── __init__.py         # File Python biasa
│   ├── settings.py         # Settings project (penting!)
│   ├── urls.py             # URL routing utama
│   ├── asgi.py             # Buat deployment (ignore dulu)
│   └── wsgi.py             # Buat deployment (ignore dulu)
└── manage.py                # Tool buat jalanin commands Django
```

**Penjelasan tiap file:**

- **`manage.py`** - Script buat jalanin berbagai command Django (run server, migrations, dll)
- **`settings.py`** - Semua konfigurasi project (database, apps, security, dll)
- **`urls.py`** - Define URL patterns (misal `/blog/` harus kemana)

### Step 3: Jalanin Development Server

```bash
python manage.py runserver
```

**Penjelasan:** Command ini jalanin server development Django di http://localhost:8000/

Buka browser, ke `http://localhost:8000/` - lo bakal liat halaman welcome Django! 🎉

**Tips:** Buat stop server, pencet `Ctrl+C` di terminal.

## Bikin App Pertama

Di Django, **project** itu keseluruhan website, sedangkan **app** itu komponen/modul tertentu.

Contoh:
- **Project:** Online Store
- **App:** Blog, Products, Shopping Cart, User Accounts

Buat blog kita, bikin app namanya `blog`:

```bash
python manage.py startapp blog
```

Sekarang struktur lo jadi:

```
django-blog-tutorial/
├── venv/
├── blog/                    # App blog (BARU!)
│   ├── __init__.py
│   ├── admin.py            # Register models ke admin
│   ├── apps.py             # Config app
│   ├── models.py           # Define database models
│   ├── tests.py            # Unit tests
│   ├── views.py            # View functions
│   └── migrations/         # Database migrations
├── blog_cms/
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── manage.py
```

### Register App di Settings

Buka `blog_cms/settings.py`, cari `INSTALLED_APPS`, tambahin `'blog'`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',  # <-- TAMBAHIN INI
]
```

**Kenapa?** Django harus tau app mana aja yang dipake di project ini.

## Bikin View Pertama

View itu fungsi Python yang handle request dan return response (biasanya HTML).

Buka `blog/views.py` dan tambahin:

```python
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to My Blog!</h1>")
```

**Penjelasan:**
- `request` = objek yang berisi info tentang HTTP request
- `HttpResponse` = response sederhana (return HTML string)

### Setup URL

Sekarang Django harus tau kapan fungsi `home` dipanggil. Setup URL-nya:

1. Bikin file baru `blog/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
```

**Penjelasan:**
- `path('', ...)` = URL root (`/`)
- `views.home` = fungsi yang dipanggil
- `name='home'` = nama URL (buat reference nanti)

2. Include di `blog_cms/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include  # <-- tambahin include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # <-- TAMBAHIN INI
]
```

### Test

Jalanin server lagi:

```bash
python manage.py runserver
```

Buka `http://localhost:8000/` - lo bakal liat "Welcome to My Blog!" 🎉

## Bikin View dengan Template

Return HTML string dari view itu kurang praktis. Better pake **template** (file HTML terpisah).

### Step 1: Bikin Folder Templates

```bash
mkdir -p blog/templates/blog
```

**Penjelasan:** Django otomatis cari templates di folder `templates/` di setiap app.

### Step 2: Bikin Template

Bikin file `blog/templates/blog/home.html`:

```html
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Blog</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }
        .welcome {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="welcome">
        <h1>Welcome to My Blog! 🚀</h1>
        <p>Ini blog pertama gue yang dibikin pake Django!</p>
        <p>Lo udah berhasil setup Django project. Keren!</p>
    </div>
</body>
</html>
```

**Note:** Lo masih pake HTML, CSS biasa kan? Iya! Django ga ngeganti HTML/CSS lo, cuma nambah kemampuan dinamis aja.

### Step 3: Update View

Ganti `blog/views.py`:

```python
from django.shortcuts import render

def home(request):
    return render(request, 'blog/home.html')
```

**Penjelasan:**
- `render()` = fungsi buat render template
- Argumen pertama: request object
- Argumen kedua: path ke template

### Test Lagi

Refresh browser lo - sekarang pake template yang proper! 🎨

## Tambahin Data Dinamis ke Template

Sekarang kita bikin template yang beneran **dinamis** - terima data dari view.

### Update View dengan Context

Edit `blog/views.py`:

```python
from django.shortcuts import render

def home(request):
    # Data yang mau dikirim ke template
    context = {
        'site_name': 'Blog Gue',
        'posts_count': 5,
        'author': 'Nama Lo',
        'posts': [
            {'title': 'Post Pertama', 'content': 'Ini konten post pertama'},
            {'title': 'Post Kedua', 'content': 'Ini konten post kedua'},
            {'title': 'Post Ketiga', 'content': 'Ini konten post ketiga'},
        ]
    }
    return render(request, 'blog/home.html', context)
```

**Penjelasan:**
- `context` = dictionary berisi data yang mau dikirim ke template
- Mirip kayak props di React atau data di Vue

### Update Template

Edit `blog/templates/blog/home.html`:

```html
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ site_name }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }
        .welcome {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .post {
            background: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .post h2 {
            margin-top: 0;
            color: #007bff;
        }
    </style>
</head>
<body>
    <div class="welcome">
        <h1>Welcome to {{ site_name }}! 🚀</h1>
        <p>Author: <strong>{{ author }}</strong></p>
        <p>Total posts: <strong>{{ posts_count }}</strong></p>
    </div>

    <h2>Recent Posts:</h2>
    {% for post in posts %}
        <div class="post">
            <h2>{{ post.title }}</h2>
            <p>{{ post.content }}</p>
        </div>
    {% endfor %}
</body>
</html>
```

**Penjelasan Syntax Template Django:**

- **`{{ variable }}`** - Print variabel (kayak `${variable}` di JavaScript)
- **`{% for item in list %} ... {% endfor %}`** - Loop (kayak `for` di JavaScript)
- **`{% if condition %} ... {% endif %}`** - Conditional (kayak `if` di JavaScript)

**Bandingkan dengan JavaScript:**
```javascript
// JavaScript
const posts = [...];
posts.forEach(post => {
    console.log(post.title);
});

// Django Template (mirip kan?)
{% for post in posts %}
    {{ post.title }}
{% endfor %}
```

### Test

Refresh browser - sekarang lo liat data dari view muncul di template! 🎉

## Kesimpulan Chapter 1

Lo udah belajar:

✅ Apa itu Django dan kenapa lo perlu pake framework  
✅ Arsitektur MTV (Model-Template-View)  
✅ Setup development environment  
✅ Bikin project dan app Django  
✅ Bikin view dan URL routing  
✅ Pake templates buat render HTML  
✅ Kirim data dari view ke template (context)  

### Hubungan dengan HTML/CSS/JS yang Lo Udah Tau

- **HTML/CSS** - Masih lo pake di templates, ga berubah!
- **JavaScript** - Bisa lo tambahin di templates buat interactivity
- **Django** - Handle backend: database, authentication, logic

Django **ga ngeganti** skill HTML/CSS/JS lo - malah **ngeboost** dengan kemampuan backend!

## Next Steps

Di [Chapter 2](./02-setup-project.md), lo bakal belajar lebih dalam tentang:
- Request/Response cycle detail
- Settings dan configuration
- Best practices Django
- Project structure yang bener

Siap lanjut? Let's go! 🚀

## Troubleshooting

### Error: "python: command not found"
**Solusi:** Install Python dulu dari python.org

### Error: "No module named django"
**Solusi:** Pastiin venv udah diaktifin, terus `pip install Django`

### Server ga jalan
**Solusi:** Check ada error message ga. Biasanya karena:
- Port 8000 udah dipake (coba `python manage.py runserver 8001`)
- Ada syntax error di code lo

### Template not found
**Solusi:** 
- Check nama file template bener ga
- Pastiin folder structure: `blog/templates/blog/home.html`
- Check app udah di-register di `INSTALLED_APPS`
