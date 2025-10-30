# Tutorial 10: Testing & Deployment

## What You'll Learn

- Writing Django tests
- Test-driven development
- Deploying to production
- Security considerations
- Performance optimization
- Monitoring and maintenance

## Understanding Testing

**Why Test?**
- Catch bugs early
- Confidence in changes
- Documentation (tests show how code works)
- Prevent regressions

**Types of Tests:**
1. **Unit Tests**: Test individual functions/methods
2. **Integration Tests**: Test components together
3. **Functional Tests**: Test user workflows

## Django Testing Basics

Django uses Python's `unittest` framework.

### Test File Structure

```
blog/
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   ├── test_forms.py
│   └── test_urls.py
```

Or single file:
```
blog/
├── tests.py
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app
python manage.py test blog

# Run specific test file
python manage.py test blog.tests.test_models

# Run specific test
python manage.py test blog.tests.test_models.PostModelTest.test_slug_generation

# Verbose output
python manage.py test --verbosity=2

# Keep test database
python manage.py test --keepdb
```

## Step 1: Testing Models

Create `blog/tests/test_models.py`:

```python
from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Category, Post, Comment


class CategoryModelTest(TestCase):
    """Test Category model"""
    
    def setUp(self):
        """Run before each test"""
        self.category = Category.objects.create(
            name='Technology',
            description='Tech posts'
        )
    
    def test_category_creation(self):
        """Test category is created correctly"""
        self.assertEqual(self.category.name, 'Technology')
        self.assertEqual(self.category.description, 'Tech posts')
        self.assertTrue(isinstance(self.category, Category))
    
    def test_slug_generation(self):
        """Test slug is auto-generated"""
        self.assertEqual(self.category.slug, 'technology')
    
    def test_slug_uniqueness(self):
        """Test duplicate names get unique slugs"""
        category2 = Category.objects.create(name='Technology')
        self.assertNotEqual(self.category.slug, category2.slug)
    
    def test_str_method(self):
        """Test string representation"""
        self.assertEqual(str(self.category), 'Technology')


class PostModelTest(TestCase):
    """Test Post model"""
    
    def setUp(self):
        """Create test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Tech')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content that is long enough to be valid.',
            author=self.user,
            category=self.category,
            status='published'
        )
    
    def test_post_creation(self):
        """Test post is created correctly"""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.category, self.category)
    
    def test_slug_generation(self):
        """Test slug generated from title"""
        self.assertEqual(self.post.slug, 'test-post')
    
    def test_published_posts(self):
        """Test published posts query"""
        draft_post = Post.objects.create(
            title='Draft',
            content='Draft content' * 10,
            author=self.user,
            category=self.category,
            status='draft'
        )
        published = Post.published.all()
        self.assertIn(self.post, published)
        self.assertNotIn(draft_post, published)
    
    def test_approved_comments(self):
        """Test approved_comments property"""
        # Create approved comment
        Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Approved comment',
            approved=True
        )
        # Create unapproved comment
        Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Unapproved comment',
            approved=False
        )
        self.assertEqual(self.post.approved_comments.count(), 1)


class CommentModelTest(TestCase):
    """Test Comment model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Tech')
        self.post = Post.objects.create(
            title='Test Post',
            content='Content' * 20,
            author=self.user,
            category=self.category
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment'
        )
    
    def test_comment_creation(self):
        """Test comment is created correctly"""
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.author, self.user)
        self.assertFalse(self.comment.approved)  # Default is False
    
    def test_str_method(self):
        """Test string representation"""
        expected = f'Comment by {self.user.username} on {self.post.title}'
        self.assertEqual(str(self.comment), expected)
```

### Understanding Test Methods

**setUp()**: Runs before each test
```python
def setUp(self):
    self.user = User.objects.create_user(...)
```

**Assertions:**
```python
self.assertEqual(a, b)          # a == b
self.assertNotEqual(a, b)       # a != b
self.assertTrue(x)              # bool(x) is True
self.assertFalse(x)             # bool(x) is False
self.assertIn(a, b)             # a in b
self.assertNotIn(a, b)          # a not in b
self.assertIsNone(x)            # x is None
self.assertIsNotNone(x)         # x is not None
self.assertRaises(Exception)    # Code raises exception
```

## Step 2: Testing Views

Create `blog/tests/test_views.py`:

```python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Category, Post


class HomeViewTest(TestCase):
    """Test home view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Tech')
        
        # Create published post
        self.post = Post.objects.create(
            title='Published Post',
            content='Content' * 20,
            author=self.user,
            category=self.category,
            status='published'
        )
        
        # Create draft post
        self.draft = Post.objects.create(
            title='Draft Post',
            content='Content' * 20,
            author=self.user,
            category=self.category,
            status='draft'
        )
    
    def test_home_view_status_code(self):
        """Test home page loads"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_home_view_uses_correct_template(self):
        """Test correct template used"""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'blog/home.html')
    
    def test_home_view_shows_published_posts(self):
        """Test only published posts shown"""
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Published Post')
        self.assertNotContains(response, 'Draft Post')
    
    def test_home_view_search(self):
        """Test search functionality"""
        response = self.client.get(reverse('home') + '?q=Published')
        self.assertContains(response, 'Published Post')
        self.assertNotContains(response, 'Draft Post')


class PostDetailViewTest(TestCase):
    """Test post detail view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Tech')
        self.post = Post.objects.create(
            title='Test Post',
            content='Content' * 20,
            author=self.user,
            category=self.category,
            status='published'
        )
    
    def test_post_detail_view(self):
        """Test post detail page loads"""
        response = self.client.get(
            reverse('post_detail', kwargs={'slug': self.post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
    
    def test_post_detail_404(self):
        """Test 404 for non-existent post"""
        response = self.client.get(
            reverse('post_detail', kwargs={'slug': 'nonexistent'})
        )
        self.assertEqual(response.status_code, 404)


class CreatePostViewTest(TestCase):
    """Test create post view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Tech')
    
    def test_create_post_requires_login(self):
        """Test redirect if not logged in"""
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertIn('/login/', response.url)
    
    def test_create_post_logged_in(self):
        """Test create post when logged in"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 200)
    
    def test_create_post_submission(self):
        """Test creating a post"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('create_post'), {
            'title': 'New Post',
            'content': 'New content' * 20,
            'category': self.category.id,
            'status': 'draft',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Post.objects.filter(title='New Post').exists())


class EditPostViewTest(TestCase):
    """Test edit post view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Tech')
        self.post = Post.objects.create(
            title='Test Post',
            content='Content' * 20,
            author=self.user,
            category=self.category,
        )
    
    def test_edit_own_post(self):
        """Test author can edit own post"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('edit_post', kwargs={'slug': self.post.slug})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_cannot_edit_others_post(self):
        """Test user cannot edit others' posts"""
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(
            reverse('edit_post', kwargs={'slug': self.post.slug})
        )
        self.assertEqual(response.status_code, 403)  # Forbidden
```

### Understanding View Tests

**Client:**
```python
self.client = Client()
self.client.get(url)
self.client.post(url, data)
self.client.login(username='user', password='pass')
```

**URL Reverse:**
```python
reverse('home')  # Instead of hardcoding '/blog/'
reverse('post_detail', kwargs={'slug': 'my-post'})
```

**Response Assertions:**
```python
self.assertEqual(response.status_code, 200)
self.assertTemplateUsed(response, 'blog/home.html')
self.assertContains(response, 'text')
self.assertNotContains(response, 'text')
```

## Step 3: Testing Forms

Create `blog/tests/test_forms.py`:

```python
from django.test import TestCase
from django.contrib.auth.models import User
from blog.forms import PostForm, CommentForm
from blog.models import Category, Post


class PostFormTest(TestCase):
    """Test PostForm"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Tech')
    
    def test_post_form_valid_data(self):
        """Test form with valid data"""
        form = PostForm(data={
            'title': 'Test Post',
            'content': 'Test content' * 20,
            'category': self.category.id,
            'status': 'draft',
        })
        self.assertTrue(form.is_valid())
    
    def test_post_form_empty_title(self):
        """Test form with empty title"""
        form = PostForm(data={
            'title': '',
            'content': 'Test content' * 20,
            'category': self.category.id,
            'status': 'draft',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_post_form_short_content(self):
        """Test form with short content"""
        form = PostForm(data={
            'title': 'Test',
            'content': 'Short',  # Too short
            'category': self.category.id,
            'status': 'draft',
        })
        self.assertFalse(form.is_valid())


class CommentFormTest(TestCase):
    """Test CommentForm"""
    
    def test_comment_form_valid(self):
        """Test form with valid data"""
        form = CommentForm(data={
            'content': 'Test comment',
        })
        self.assertTrue(form.is_valid())
    
    def test_comment_form_empty(self):
        """Test form with empty content"""
        form = CommentForm(data={
            'content': '',
        })
        self.assertFalse(form.is_valid())
```

## Step 4: Test Coverage

Install coverage tool:

```bash
pip install coverage
```

Run with coverage:

```bash
# Run tests with coverage
coverage run --source='.' manage.py test blog

# Generate report
coverage report

# Generate HTML report
coverage html

# Open in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

**Interpreting Coverage:**
- 80%+: Good coverage
- 90%+: Great coverage
- 100%: Perfect (but hard to achieve)

## Deployment Preparation

### Step 1: Environment Variables

Update `.env`:

```bash
# Production settings
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL for production)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Step 2: Production Settings

Update `settings.py`:

```python
from decouple import config, Csv

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Security settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

### Step 3: Static Files for Production

```python
# settings.py
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Collect static files
python manage.py collectstatic
```

This copies all static files to one directory for serving.

### Step 4: Database Migration

For PostgreSQL:

```bash
# Install psycopg2
pip install psycopg2-binary

# Create database
createdb blog_cms_db

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Step 5: Requirements File

Generate production requirements:

```bash
pip freeze > requirements.txt
```

Should include:
```
Django==4.2.25
psycopg2-binary==2.9.9
python-decouple==3.8
Pillow==10.0.0
gunicorn==21.2.0  # For production server
whitenoise==6.5.0  # For serving static files
```

## Deployment Options

### Option 1: Heroku

1. **Install Heroku CLI**
   ```bash
   # Follow: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create `Procfile`:**
   ```
   web: gunicorn blog_cms.wsgi --log-file -
   ```

3. **Create `runtime.txt`:**
   ```
   python-3.11.14
   ```

4. **Deploy:**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   heroku open
   ```

### Option 2: DigitalOcean / AWS / VPS

1. **Install dependencies on server:**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx postgresql
   ```

2. **Setup project:**
   ```bash
   git clone your-repo
   cd your-project
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Setup Gunicorn:**
   ```bash
   gunicorn --bind 0.0.0.0:8000 blog_cms.wsgi
   ```

4. **Setup Nginx:**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location /static/ {
           root /path/to/your/project;
       }
       
       location /media/ {
           root /path/to/your/project;
       }
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

5. **Setup Supervisor (process manager):**
   ```bash
   sudo apt install supervisor
   ```
   
   Create `/etc/supervisor/conf.d/blog_cms.conf`:
   ```
   [program:blog_cms]
   command=/path/to/venv/bin/gunicorn blog_cms.wsgi:application --bind 127.0.0.1:8000
   directory=/path/to/project
   user=your-user
   autostart=true
   autorestart=true
   ```

6. **Setup SSL with Let's Encrypt:**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

### Option 3: PythonAnywhere

1. **Sign up:** https://www.pythonanywhere.com/
2. **Upload code** via Git or files
3. **Create virtual environment**
4. **Configure Web app** in dashboard
5. **Set environment variables**
6. **Reload app**

## Security Checklist

Before deploying:

- ✅ `DEBUG = False` in production
- ✅ Strong `SECRET_KEY` (don't commit to Git!)
- ✅ `ALLOWED_HOSTS` configured
- ✅ Use HTTPS (SSL certificate)
- ✅ `SECURE_*` settings enabled
- ✅ Database credentials secure
- ✅ Use environment variables
- ✅ Keep dependencies updated
- ✅ Validate user input
- ✅ Use CSRF protection
- ✅ SQL injection protection (ORM does this)
- ✅ XSS protection (templates do this)

## Monitoring

### Logging

Configure logging in `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

Create logs directory:
```bash
mkdir logs
```

### Error Tracking

Use services like:
- **Sentry**: Error tracking and monitoring
- **Rollbar**: Real-time error tracking
- **Bugsnag**: Exception reporting

Install Sentry:
```bash
pip install sentry-sdk
```

Configure:
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
)
```

## Performance Optimization

### 1. Database Query Optimization

```python
# Bad: N+1 queries
posts = Post.objects.all()
for post in posts:
    print(post.author.username)  # Query per post!

# Good: Select related
posts = Post.objects.select_related('author', 'category')
for post in posts:
    print(post.author.username)  # No extra queries!

# Prefetch related (for many-to-many)
posts = Post.objects.prefetch_related('comments')
```

### 2. Caching

Install Redis:
```bash
pip install django-redis
```

Configure:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

Use caching:
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def home(request):
    # ...
```

### 3. Static File Serving

Use WhiteNoise:
```bash
pip install whitenoise
```

Configure:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ...
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 4. Database Indexing

```python
class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True)  # Add index
    slug = models.SlugField(unique=True, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['status', 'created_at']),
        ]
```

## Maintenance

### Regular Tasks

1. **Update dependencies:**
   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```

2. **Backup database:**
   ```bash
   python manage.py dumpdata > backup.json
   
   # PostgreSQL
   pg_dump dbname > backup.sql
   ```

3. **Monitor logs:**
   ```bash
   tail -f logs/django.log
   ```

4. **Check security:**
   ```bash
   python manage.py check --deploy
   ```

5. **Run tests regularly:**
   ```bash
   python manage.py test
   ```

## Deployment Checklist

Final checklist before going live:

- ✅ All tests passing
- ✅ `DEBUG = False`
- ✅ Secret key secure
- ✅ Environment variables set
- ✅ Database configured
- ✅ Static files collected
- ✅ Media files directory created
- ✅ Migrations applied
- ✅ Superuser created
- ✅ SSL certificate installed
- ✅ Domain configured
- ✅ Email sending working
- ✅ Error logging configured
- ✅ Backups automated
- ✅ Monitoring setup

## Troubleshooting Production

### Issue: Static files not loading

Check:
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

Run:
```bash
python manage.py collectstatic
```

### Issue: Database connection error

Check:
- Database is running
- Credentials are correct
- Database exists
- Firewall allows connection

### Issue: 500 Internal Server Error

Check:
- Error logs
- `DEBUG = True` temporarily (remove after!)
- Sentry/error tracking

### Issue: Permission denied

Check:
- File/directory permissions
- Media directory writable
- Static directory readable

## What You've Learned

- Writing Django tests
- Testing models, views, and forms
- Test coverage
- Deployment preparation
- Production settings
- Security best practices
- Performance optimization
- Monitoring and maintenance
- Deployment options

## Congratulations!

You've completed the Django Blog/CMS tutorial! You now know:

1. Django basics (models, views, URLs)
2. Admin customization
3. Forms and validation
4. Authentication and permissions
5. Template system
6. Static files and CSS
7. Testing
8. Deployment

## Next Steps

Continue learning:

1. **Django REST Framework**: Build APIs
2. **Celery**: Background tasks
3. **Docker**: Containerization
4. **CI/CD**: Automated deployment
5. **Advanced queries**: Aggregation, annotations
6. **Custom middleware**: Request/response processing
7. **Custom template tags**: Reusable template logic
8. **WebSockets**: Real-time features

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Two Scoops of Django](https://www.feldroy.com/two-scoops-of-django-3-x)
- [Django Discord](https://discord.gg/xcRH6mN4fa)
- [r/django](https://www.reddit.com/r/django/)

---

**Thank you for following this tutorial! Happy coding! 🚀**
