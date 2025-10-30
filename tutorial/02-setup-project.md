# Tutorial 02: Setup Project Django

## Apa yang Bakal Lo Bikin di Chapter Ini

- Bikin struktur project Django
- Bikin aplikasi blog
- Configure settings project
- Jalanin Django server pertama lo

## Step 1: Bikin Django Project

Dari folder project lo (dengan virtual environment udah aktif):

```bash
django-admin startproject blog_cms .
```

**Note:** Tanda `.` di akhir bikin project di folder current, bukan bikin folder nested baru.

Ini bakal bikin struktur:
```
.
├── blog_cms/
│   ├── __init__.py      # Bikin ini jadi Python package
│   ├── asgi.py          # Config ASGI (buat async)
│   ├── settings.py      # Settings project (PENTING!)
│   ├── urls.py          # Konfigurasi URL utama
│   └── wsgi.py          # Config WSGI (buat deployment)
└── manage.py            # Script management Django
```

**Penjelasan tiap file:**
- **`manage.py`** - Tool buat jalanin command Django (migrate, runserver, dll)
- **`settings.py`** - Semua konfigurasi project (database, apps, security)
- **`urls.py`** - Define URL patterns (routing)
- **`wsgi.py` / `asgi.py`** - Buat deployment (ignore dulu)

## Step 2: Bikin Blog App

App itu komponen yang reusable. Bikin app blog kita:

```bash
python manage.py startapp blog
```

Ini bikin struktur:
```
blog/
├── __init__.py
├── admin.py            # Konfigurasi admin panel
├── apps.py             # Konfigurasi app
├── models.py           # Model database
├── tests.py            # Unit tests
├── views.py            # Fungsi view
└── migrations/         # Database migrations
    └── __init__.py
```

**Perbedaan Project vs App:**
- **Project** = Keseluruhan website (blog_cms)
- **App** = Komponen/modul tertentu (blog, users, products, dll)

Contoh: Online store punya app: products, cart, checkout, blog

## Step 3: Configure Settings

Buka `blog_cms/settings.py` dan kita pahami + modifikasi.

### 3.1: Tambahin Support Environment Variables

Di bagian atas `settings.py`, tambahin:

```python
from pathlib import Path
from decouple import config  # Tambahin import ini

BASE_DIR = Path(__file__).resolve().parent.parent
```

**Install dulu python-decouple:**
```bash
pip install python-decouple
```

**Kenapa?** Biar kita bisa pake environment variables buat data sensitif (password, secret key).

### 3.2: Update SECRET_KEY dan DEBUG

Cari baris ini dan ganti:

```python
# SEBELUM:
SECRET_KEY = 'django-insecure-...'
DEBUG = True

# SESUDAH:
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)
```

**Kenapa?**
- `SECRET_KEY` harus dirahasiakan (buat enkripsi session, dll)
- `DEBUG` harus False di production (biar error message ga keliatan user)

### 3.3: Update ALLOWED_HOSTS

```python
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS', 
    default='localhost,127.0.0.1',
    cast=lambda v: [s.strip() for s in v.split(',')]
)
```

**Kenapa?** Django cuma allow request dari host yang ada di list ini (security).

### 3.4: Register App Blog Kita

Cari `INSTALLED_APPS` dan tambahin app kita:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Our apps
    'blog',  # TAMBAHIN INI
]
```

**Kenapa register app?** Django harus tau app mana aja yang dipake buat:
- Jalanin migrations
- Load templates
- Load static files
- Register di admin

### 3.5: Configure Templates

Cari `TEMPLATES` dan update `DIRS`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Tambahin ini
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',  # Tambahin ini
            ],
        },
    },
]
```

**Penjelasan:**
- `DIRS`: Django bakal cari templates di folder `templates/` di root
- `APP_DIRS`: Django juga cari di folder `templates/` di tiap app
- `context_processors`: Variabel yang otomatis available di semua templates

### 3.6: Configure Database

Django defaultnya pake SQLite. Kita bikin configurable:

```python
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': config('DB_NAME', default=str(BASE_DIR / 'db.sqlite3')),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default=''),
    }
}
```

**Kenapa?**
- Development: Pake SQLite (simple, ga perlu install apa-apa)
- Production: Pake PostgreSQL/MySQL (lebih robust)
- Tinggal ganti environment variable, ga perlu ubah code!

### 3.7: Configure Static dan Media Files

Cari section static files dan update:

```python
# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files (User uploads)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**Penjelasan:**
- **`STATIC_URL`** - URL prefix buat static files (`/static/css/style.css`)
- **`STATIC_ROOT`** - Folder tempat `collectstatic` kumpulin files (production)
- **`STATICFILES_DIRS`** - Folder tempat Django cari static files (development)
- **`MEDIA_URL`** - URL prefix buat user uploads (`/media/photos/image.jpg`)
- **`MEDIA_ROOT`** - Folder tempat simpan uploaded files

**Analogi:**
- Static files = File lo sendiri (CSS, JS, gambar logo)
- Media files = File yang diupload user (foto profile, gambar post)

### 3.8: Tambahin Authentication Settings

Di akhir `settings.py`, tambahin:

```python
# Authentication settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
```

**Penjelasan:**
- `LOGIN_URL` - Redirect ke sini kalo perlu login
- `LOGIN_REDIRECT_URL` - Redirect ke sini setelah login berhasil
- `LOGOUT_REDIRECT_URL` - Redirect ke sini setelah logout

## Step 4: Bikin Environment File

Bikin file `.env.example`:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite by default)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# Kalo mau pake PostgreSQL:
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=blog_db
# DB_USER=postgres
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=5432
```

Copy ke `.env`:
```bash
cp .env.example .env
```

**PENTING:** Tambahin `.env` ke `.gitignore` biar ga ke-commit ke Git!

```bash
echo ".env" >> .gitignore
```

## Step 5: Bikin Struktur Folder

Bikin folder-folder yang dibutuhkan:

```bash
mkdir -p static/css
mkdir -p static/js
mkdir -p static/images
mkdir -p media
mkdir -p templates
mkdir -p blog/templates/blog
```

**Kegunaan tiap folder:**
- `static/css/` - File CSS lo
- `static/js/` - File JavaScript lo
- `static/images/` - Gambar static (logo, icons)
- `media/` - File yang diupload user (foto post, dll)
- `templates/` - Templates project-wide (base.html, dll)
- `blog/templates/blog/` - Templates khusus blog app

## Step 6: Jalanin Initial Migration

Django udah punya built-in apps (admin, auth, dll) yang butuh table database:

```bash
python manage.py migrate
```

Lo bakal liat output kayak gini:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  ...
```

**Apa yang terjadi?**
- Django bikin file `db.sqlite3` (database lo)
- Django bikin tables buat admin, auth, sessions, dll
- Lo sekarang bisa pake admin panel dan authentication system!

## Step 7: Bikin Superuser

Bikin akun admin buat akses admin panel:

```bash
python manage.py createsuperuser
```

Isi data yang diminta:
```
Username: admin
Email: admin@example.com
Password: (ketik password, ga keliatan)
Password (again): (ketik lagi)
```

**Tips:** Pake password yang gampang diinget buat development (misal: `admin123`)

## Step 8: Jalanin Development Server

Sekarang jalanin server:

```bash
python manage.py runserver
```

Lo bakal liat:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
October 30, 2025 - 10:00:00
Django version 4.2.7, using settings 'blog_cms.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

✅ **Buka browser:** http://localhost:8000/

Lo bakal liat halaman welcome Django! 🎉

✅ **Coba admin panel:** http://localhost:8000/admin/

Login pake username & password yang lo bikin tadi. Lo bakal liat Django admin panel yang keren!

## Step 9: Configure URLs buat Media Files

Buka `blog_cms/urls.py` dan update:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # Nanti kita bikin
]

# Serve media files di development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

**Kenapa?** Biar Django bisa serve uploaded files di development mode.

## Kesimpulan Chapter 2

Lo udah belajar:

✅ Bikin Django project dan app  
✅ Configure settings (database, static, media, authentication)  
✅ Setup environment variables  
✅ Bikin struktur folder  
✅ Jalanin migrations  
✅ Bikin superuser  
✅ Jalanin development server  
✅ Akses admin panel  

### Struktur Project Sekarang:

```
django-blog-tutorial/
├── venv/                   # Virtual environment
├── blog_cms/               # Project folder
│   ├── settings.py        # ✅ Udah dikonfigurasi
│   ├── urls.py            # ✅ Udah dikonfigurasi
│   └── ...
├── blog/                   # Blog app
│   ├── models.py
│   ├── views.py
│   └── ...
├── static/                 # ✅ Static files
│   ├── css/
│   ├── js/
│   └── images/
├── media/                  # ✅ User uploads
├── templates/              # ✅ Templates
├── .env                    # ✅ Environment variables
├── .env.example
├── db.sqlite3              # ✅ Database
└── manage.py
```

## Next Steps

Di [Chapter 3](./03-model-database.md), lo bakal belajar:
- Bikin Models (Post, Category, Comment)
- Relationships (ForeignKey, ManyToMany)
- Migrations
- Django ORM (query database)

Siap lanjut? Let's go! 🚀

## Troubleshooting

### Error: "No module named 'decouple'"
**Solusi:** Install: `pip install python-decouple`

### Error: "ImproperlyConfigured: SECRET_KEY"
**Solusi:** Pastiin file `.env` udah ada dan ada `SECRET_KEY` di dalemnya

### Server ga jalan
**Solusi:**
- Check ada error message ga
- Pastiin port 8000 ga dipake app lain
- Coba port lain: `python manage.py runserver 8001`

### Admin panel ga ada
**Solusi:**
- Pastiin lo udah run migrations: `python manage.py migrate`
- Pastiin `django.contrib.admin` ada di `INSTALLED_APPS`
