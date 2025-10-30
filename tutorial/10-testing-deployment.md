# Tutorial 10: Testing & Deployment

## Apa yang Bakal Lo Pelajari

- Writing tests di Django
- Running tests
- Deployment ke production
- Production settings

## Part 1: Testing

### Kenapa Testing?

- Catch bugs early
- Confidence saat refactor
- Documentation (tests show gimana code should work)

### Test File Structure

```
blog/tests/
  __init__.py
  test_models.py
  test_views.py
  test_forms.py
```

### Test Models

`blog/tests/test_models.py`:

```python
from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Category, Post

class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(
            name="Tech",
            description="Technology posts"
        )
        self.assertEqual(str(category), "Tech")
        self.assertEqual(category.slug, "tech")

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'pass')
        self.category = Category.objects.create(name="Tech")
    
    def test_post_creation(self):
        post = Post.objects.create(
            title="Test Post",
            content="Content here",
            author=self.user,
            category=self.category,
            status='published'
        )
        self.assertEqual(str(post), "Test Post")
        self.assertTrue(post.slug)
```

### Test Views

`blog/tests/test_views.py`:

```python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post, Category

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test', 'test@test.com', 'pass')
        self.category = Category.objects.create(name="Tech")
    
    def test_home_page_status(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_home_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'blog/home.html')

class CreatePostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test', 'test@test.com', 'pass')
        self.category = Category.objects.create(name="Tech")
    
    def test_create_post_requires_login(self):
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_create_post_with_login(self):
        self.client.login(username='test', password='pass')
        response = self.client.post(reverse('create_post'), {
            'title': 'Test Post',
            'content': 'A' * 100,
            'category': self.category.id,
            'status': 'draft'
        })
        self.assertEqual(Post.objects.count(), 1)
```

### Test Forms

`blog/tests/test_forms.py`:

```python
from django.test import TestCase
from blog.forms import PostForm
from blog.models import Category

class PostFormTest(TestCase):
    def test_post_form_valid(self):
        category = Category.objects.create(name="Tech")
        form = PostForm(data={
            'title': 'Test Post',
            'content': 'A' * 100,
            'category': category.id,
            'status': 'draft'
        })
        self.assertTrue(form.is_valid())
    
    def test_post_form_invalid_short_content(self):
        form = PostForm(data={
            'title': 'Test',
            'content': 'Too short',  # < 50 chars
        })
        self.assertFalse(form.is_valid())
```

### Run Tests

```bash
# Run all tests
python manage.py test

# Run specific app
python manage.py test blog

# Run specific test file
python manage.py test blog.tests.test_models

# Run specific test class
python manage.py test blog.tests.test_models.PostModelTest

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Coverage Report

Buka `htmlcov/index.html` di browser buat liat coverage report yang bagus!

## Part 2: Deployment Preparation

### 1. Environment Variables

Pake `python-decouple` (sudah installed):

`.env` file:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:pass@host:port/dbname
```

`settings.py`:
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')
```

### 2. Production Settings

```python
# settings.py

# Security
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Database - PostgreSQL untuk production
import dj_database_url
if not DEBUG:
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL')
        )
    }
```

### 3. Requirements

Generate `requirements.txt`:

```bash
pip freeze > requirements.txt
```

Or manually create:
```
Django==4.2.7
python-decouple==3.8
Pillow==10.1.0
dj-database-url==2.1.0
psycopg2-binary==2.9.9  # PostgreSQL
gunicorn==21.2.0        # Production server
whitenoise==6.6.0       # Static files
```

### 4. Whitenoise (Static Files)

Install:
```bash
pip install whitenoise
```

`settings.py`:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this!
    # ... other middleware
]

# Static files with compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 5. Gunicorn (Production Server)

`Procfile` (buat Heroku):
```
web: gunicorn blog_cms.wsgi
```

Run locally:
```bash
gunicorn blog_cms.wsgi:application
```

## Part 3: Deployment Options

### Option 1: PythonAnywhere (Gratis!)

1. Sign up: https://www.pythonanywhere.com
2. Upload code atau clone dari GitHub
3. Setup virtual environment
4. Configure WSGI file
5. Set static files path
6. Reload web app

**Pros:** Free, easy, perfect buat learning  
**Cons:** Limited resources di free tier

### Option 2: Heroku

1. Install Heroku CLI
2. Create `Procfile`
3. Create `runtime.txt`:
   ```
   python-3.11.6
   ```
4. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

**Pros:** Easy deployment, Git-based  
**Cons:** Not free anymore (minimum $5/month)

### Option 3: DigitalOcean / AWS

Lebih advanced, butuh setup server manually.

**Pros:** Full control, scalable  
**Cons:** More complex, butuh devops knowledge

### Option 4: Vercel / Railway

Modern hosting dengan Git integration.

**Pros:** Easy, modern  
**Cons:** Bisa mahal kalo traffic tinggi

## Deployment Checklist

Sebelum deploy:

- ✅ `DEBUG = False`
- ✅ `SECRET_KEY` di environment variable
- ✅ `ALLOWED_HOSTS` configured
- ✅ Database production (PostgreSQL)
- ✅ Static files configured
- ✅ Run `collectstatic`
- ✅ Run migrations
- ✅ Create superuser
- ✅ Test di production!

## Post-Deployment

### Monitoring

```bash
# Check logs
heroku logs --tail  # Heroku
# atau
tail -f /var/log/django/error.log  # VPS
```

### Backups

```bash
# Backup database
python manage.py dumpdata > backup.json

# Restore
python manage.py loaddata backup.json
```

### Updates

```bash
git push heroku main  # Deploy update
heroku run python manage.py migrate  # Run migrations
heroku restart  # Restart app
```

## Common Production Issues

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Database Connection Error
Check `DATABASE_URL` environment variable.

### 500 Error
Check logs! Set `DEBUG=True` temporarily buat liat error.

### ALLOWED_HOSTS Error
Add domain ke `ALLOWED_HOSTS`:
```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

## Performance Tips

### 1. Use PostgreSQL (Not SQLite)

SQLite bagus buat development, tapi PostgreSQL better buat production.

### 2. Cache

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
    }
}
```

### 3. CDN untuk Static Files

Pake Cloudflare atau AWS CloudFront buat serve static files.

### 4. Compress Images

Compress images sebelum upload atau pake library kayak `django-imagekit`.

### 5. Database Indexes

```python
class Post(models.Model):
    slug = models.SlugField(unique=True, db_index=True)  # Index!
```

## Kesimpulan

Lo udah belajar:

✅ Writing tests di Django  
✅ Running dan checking coverage  
✅ Production settings  
✅ Environment variables  
✅ Static files setup  
✅ Deployment options  
✅ Production checklist  
✅ Monitoring dan maintenance  

**Selamat!** 🎉 Lo udah complete full Django tutorial dari zero sampe deployment!

## What's Next?

### Improve Blog
- Add tags
- Search functionality
- RSS feed
- Social sharing
- Email notifications

### Learn More
- Django REST Framework (API)
- Django Channels (WebSockets)
- Celery (Background tasks)
- Docker (Containerization)

### Build More Projects
- E-commerce site
- Social media clone
- Portfolio website
- API backend

## Resources

- [Django Docs](https://docs.djangoproject.com/)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)

---

**Congratulations!** Lo udah selesai Django tutorial lengkap! 🚀

Sekarang saatnya **BIKIN PROJECT LO SENDIRI!** Good luck! 💪
