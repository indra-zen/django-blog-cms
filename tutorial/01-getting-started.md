# Tutorial 01: Getting Started

## Overview

In this section, you'll set up your development environment and understand the basic concepts of Django web development.

## What is Django?

Django is a high-level Python web framework that helps you build web applications quickly. It follows the **"Don't Repeat Yourself" (DRY)** principle and includes:

- **ORM (Object-Relational Mapping):** Work with databases using Python instead of SQL
- **Admin Interface:** Built-in admin panel for managing content
- **Authentication System:** User login/logout out of the box
- **URL Routing:** Map URLs to Python functions
- **Template Engine:** Generate HTML dynamically
- **Security Features:** Protection against common vulnerabilities

## Architecture: MTV Pattern

Django uses the **Model-Template-View (MTV)** pattern:

```
┌─────────────────────────────────────────┐
│              Browser                     │
│         (User Request)                   │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│             URLs                         │
│    (Route requests to views)            │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│            Views                         │
│   (Process logic & data)                │
└────┬───────────────────────────┬────────┘
     │                           │
     ▼                           ▼
┌─────────┐               ┌──────────┐
│ Models  │               │Templates │
│(Database)               │  (HTML)  │
└─────────┘               └──────────┘
```

- **Models:** Define your data structure (database tables)
- **Templates:** HTML files with dynamic content
- **Views:** Python functions that handle requests and return responses

## Setting Up Your Environment

### Step 1: Check Python Installation

Open your terminal and check if Python is installed:

```bash
python --version
# or
python3 --version
```

You need **Python 3.8 or higher**. If not installed, download from [python.org](https://www.python.org/).

### Step 2: Create a Project Directory

```bash
mkdir django-blog-tutorial
cd django-blog-tutorial
```

### Step 3: Create a Virtual Environment

A virtual environment keeps your project dependencies isolated:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You'll see `(venv)` in your terminal prompt when activated.

### Step 4: Install Django

```bash
pip install --upgrade pip
pip install Django
```

Verify installation:

```bash
python -m django --version
```

### Step 5: Create Requirements File

Create a file called `requirements.txt`:

```txt
# Django Core
Django>=4.2,<5.0

# Database (for production)
psycopg2-binary>=2.9

# Development Tools
black>=23.0
pylint>=2.17
pylint-django>=2.5

# Django Extensions
django-extensions>=3.2

# Environment variables
python-decouple>=3.8

# Image handling
Pillow>=10.0
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

## Understanding the Project Structure

Before we start coding, let's understand what we'll create:

```
django-blog-tutorial/
├── venv/                  # Virtual environment (don't commit to git)
├── blog_cms/              # Main project folder
│   ├── settings.py        # Project configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # Web server gateway
├── blog/                  # Our blog application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # App URL routing
│   ├── admin.py           # Admin configuration
│   ├── forms.py           # Form definitions
│   └── templates/         # HTML templates
├── static/                # CSS, JavaScript, images
├── media/                 # User-uploaded files
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Key Concepts to Remember

### 1. Project vs App

- **Project:** The entire website (blog_cms)
- **App:** A component of the project (blog)
- One project can have multiple apps

### 2. Settings.py

The control center for your Django project. Contains:
- Database configuration
- Installed apps
- Middleware
- Template settings
- Static files configuration

### 3. manage.py

Your command-line utility for:
- Running the development server
- Creating database tables
- Creating admin users
- Running tests

### 4. URLs

Django uses a URL dispatcher to route requests:
```python
path('posts/', views.post_list)  # URL pattern → View function
```

### 5. Models

Define your data structure:
```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
```

This creates a database table automatically!

## Common Django Commands

You'll use these commands frequently:

```bash
# Start a new project
django-admin startproject project_name

# Create a new app
python manage.py startapp app_name

# Run development server
python manage.py runserver

# Create database migrations
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Open Python shell with Django
python manage.py shell
```

## Environment Variables

We'll use environment variables for sensitive data (passwords, secret keys).

Create `.env` file (never commit this to git!):
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
```

Create `.env.example` (safe to commit):
```env
DEBUG=True
SECRET_KEY=change-this-in-production
DATABASE_URL=sqlite:///db.sqlite3
```

## Git Setup (Optional but Recommended)

Create `.gitignore`:
```gitignore
# Python
__pycache__/
*.pyc
*.pyo
venv/
.env

# Django
db.sqlite3
media/
staticfiles/

# IDE
.vscode/
.idea/
```

Initialize git:
```bash
git init
git add .
git commit -m "Initial commit"
```

## Troubleshooting

### Issue: "python: command not found"
**Solution:** Use `python3` instead of `python`

### Issue: "Permission denied"
**Solution:** On macOS/Linux, use `sudo pip install` or fix pip permissions

### Issue: Virtual environment not activating
**Solution:** 
- Check you're in the right directory
- On Windows, you may need to run: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Issue: Django not found after installation
**Solution:** Make sure virtual environment is activated (see `(venv)` in prompt)

## Quiz Yourself

Before moving on, make sure you understand:

1. ✅ What is the MTV pattern?
2. ✅ What's the difference between a project and an app?
3. ✅ What does `manage.py` do?
4. ✅ Why use a virtual environment?
5. ✅ What are models, views, and templates?

## Next Steps

Now that you have your environment ready and understand the basics, let's create the actual project!

**→ Continue to [02 - Project Setup](./02-project-setup.md)**

---

## Additional Resources

- [Django Official Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- [Django Girls Tutorial](https://tutorial.djangogirls.org/)
- [Real Python Django Tutorials](https://realpython.com/tutorials/django/)
