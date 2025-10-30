# Tutorial 02: Project Setup

## What You'll Build in This Section

- Create the Django project structure
- Create the blog application
- Configure project settings
- Run your first Django server

## Step 1: Create the Django Project

From your project directory (with virtual environment activated):

```bash
django-admin startproject blog_cms .
```

**Note:** The `.` at the end creates the project in the current directory instead of creating a nested folder.

This creates:
```
.
├── blog_cms/
│   ├── __init__.py      # Makes this a Python package
│   ├── asgi.py          # ASGI config (for async)
│   ├── settings.py      # Project settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI config (for deployment)
└── manage.py            # Management script
```

## Step 2: Create the Blog App

Apps are reusable components. Let's create our blog app:

```bash
python manage.py startapp blog
```

This creates:
```
blog/
├── __init__.py
├── admin.py            # Admin panel configuration
├── apps.py             # App configuration
├── models.py           # Database models
├── tests.py            # Unit tests
├── views.py            # View functions
└── migrations/         # Database migrations
    └── __init__.py
```

## Step 3: Configure Settings

Open `blog_cms/settings.py` and let's understand and modify it.

### 3.1: Add Environment Variable Support

At the top of `settings.py`, add:

```python
from pathlib import Path
from decouple import config  # Add this import

BASE_DIR = Path(__file__).resolve().parent.parent
```

### 3.2: Update SECRET_KEY and DEBUG

Find these lines and replace them:

```python
# BEFORE:
SECRET_KEY = 'django-insecure-...'
DEBUG = True

# AFTER:
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key-change-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)
```

**Why?** This allows us to use environment variables for sensitive data.

### 3.3: Update ALLOWED_HOSTS

```python
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS', 
    default='localhost,127.0.0.1',
    cast=lambda v: [s.strip() for s in v.split(',')]
)
```

### 3.4: Register Our Blog App

Find `INSTALLED_APPS` and add our app:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party apps
    'django_extensions',
    # Our apps
    'blog',  # Add this line
]
```

**Why register apps?** Django needs to know about your apps to use their models, templates, and static files.

### 3.5: Configure Templates

Find `TEMPLATES` and update `DIRS`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Add this
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',  # Add this
            ],
        },
    },
]
```

**What this does:**
- `DIRS`: Tells Django to look for templates in a root-level `templates/` folder
- `context_processors`: Makes request and media available in all templates

### 3.6: Configure Database

Django uses SQLite by default. Let's make it configurable:

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

**Why?** You can use SQLite for development and PostgreSQL for production without changing code.

### 3.7: Configure Static and Media Files

Find the static files section and update it:

```python
# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files (User uploads)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**Explanation:**
- `STATIC_URL`: URL prefix for static files
- `STATIC_ROOT`: Where `collectstatic` collects files for production
- `STATICFILES_DIRS`: Where Django looks for static files during development
- `MEDIA_URL`: URL prefix for user uploads
- `MEDIA_ROOT`: Where uploaded files are stored

### 3.8: Add Authentication Settings

At the end of `settings.py`, add:

```python
# Authentication settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
```

**What this does:**
- `LOGIN_URL`: Where to redirect if login is required
- `LOGIN_REDIRECT_URL`: Where to go after successful login
- `LOGOUT_REDIRECT_URL`: Where to go after logout

## Step 4: Create Environment File

Create `.env.example`:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite by default)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

Copy it to `.env`:
```bash
cp .env.example .env
```

## Step 5: Create Directory Structure

Create the necessary directories:

```bash
mkdir -p static/css
mkdir -p media
mkdir -p templates
mkdir -p blog/templates/blog
```

**Directory purposes:**
- `static/css/`: Your CSS files
- `media/`: User-uploaded files (post images)
- `templates/`: Project-wide templates
- `blog/templates/blog/`: Blog app templates

## Step 6: Run Initial Migration

Django comes with built-in apps (admin, auth, etc.) that need database tables:

```bash
python manage.py migrate
```

You'll see output like:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  ...
```

**What happened?** Django created the database file (`db.sqlite3`) and created tables for built-in apps.

## Step 7: Create a Superuser

Create an admin account:

```bash
python manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email: admin@example.com
Password: ******** (type your password)
Password (again): ********
```

## Step 8: Run the Development Server

Start the server:

```bash
python manage.py runserver
```

You'll see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Step 9: Test Your Setup

### Test 1: Visit the Homepage

Open your browser and go to: `http://127.0.0.1:8000/`

You should see the Django welcome page with a rocket! 🚀

### Test 2: Visit the Admin Panel

Go to: `http://127.0.0.1:8000/admin/`

Log in with your superuser credentials. You'll see the Django administration interface!

## Understanding What We've Done

### 1. Project Structure
```
django-blog-tutorial/
├── blog_cms/          # Project configuration
│   ├── settings.py    # All project settings
│   ├── urls.py        # Main URL routing (we'll edit next)
│   └── wsgi.py        # Production server interface
├── blog/              # Our blog app
│   ├── models.py      # Will define Post, Comment, Category
│   ├── views.py       # Will handle requests
│   ├── admin.py       # Will register models
│   └── templates/     # Will store HTML files
├── static/            # CSS, JS, images
├── media/             # User uploads
├── db.sqlite3         # Database file
└── manage.py          # Django management commands
```

### 2. Settings Hierarchy

Django loads settings in this order:
1. Default Django settings
2. Your `settings.py` file
3. Environment variables (via `python-decouple`)

This means you can override settings without changing code!

### 3. The Database

SQLite is perfect for development:
- Single file (`db.sqlite3`)
- No server setup needed
- Easy to delete and recreate

For production, you'd use PostgreSQL or MySQL.

## Common Issues and Solutions

### Issue: "Port already in use"
```bash
# Use a different port
python manage.py runserver 8001
```

### Issue: "ModuleNotFoundError: No module named 'decouple'"
```bash
# Install python-decouple
pip install python-decouple
```

### Issue: Changes not reflecting
```bash
# Stop server (Ctrl+C) and restart
python manage.py runserver
```

### Issue: Can't access admin
- Make sure you created a superuser: `python manage.py createsuperuser`
- Check URL is correct: `http://127.0.0.1:8000/admin/` (note the trailing slash)

## Project Configuration Checklist

Before moving on, verify:

- ✅ Django project created
- ✅ Blog app created and registered in `INSTALLED_APPS`
- ✅ Settings configured with environment variables
- ✅ Static and media directories created
- ✅ Database migrated
- ✅ Superuser created
- ✅ Development server running
- ✅ Admin panel accessible

## Understanding Django's Request Flow

When you visit `http://127.0.0.1:8000/admin/`:

```
1. Browser sends request → http://127.0.0.1:8000/admin/
2. Django receives request
3. Django checks urls.py for matching pattern
4. Found! Sends to admin view
5. Admin view processes request
6. Returns HTML response
7. Browser displays admin page
```

We'll implement this flow for our blog in the next sections!

## Key Takeaways

- **Project** = website configuration
- **App** = reusable component
- **Settings** = control everything
- **Migrations** = database changes
- **Superuser** = admin access
- **Development server** = testing locally

## Next Steps

Now that your project is set up, let's create the database models for our blog!

**→ Continue to [03 - Creating Models](./03-creating-models.md)**

---

## Additional Tips

### Useful Development Commands

```bash
# Check for issues
python manage.py check

# View all available commands
python manage.py help

# Open Django shell
python manage.py shell

# View SQL that migrations will run
python manage.py sqlmigrate blog 0001
```

### VS Code Setup (Optional)

Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true
}
```
