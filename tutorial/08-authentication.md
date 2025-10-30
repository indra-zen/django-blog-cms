# Tutorial 08: Authentication

## Apa yang Bakal Lo Pelajari

- Django authentication system
- User registration & login
- Password reset
- Protecting views dengan decorators
- User permissions

## Memahami Authentication

**Authentication:** "Lo siapa?"  
**Authorization:** "Lo boleh ngapain aja?"

Django provides:
- User model built-in
- Login/logout views
- Password hashing (auto secure!)
- Session management
- Permission system

## Step 1: User Model Django

Django punya built-in User model:

```python
from django.contrib.auth.models import User

# Create user
user = User.objects.create_user(
    username='john',
    email='john@example.com',
    password='secret123'  # Auto hashed!
)

# User attributes
user.username       # 'john'
user.email          # 'john@example.com'
user.first_name     # Optional
user.last_name      # Optional
user.is_active      # True/False
user.is_staff       # Bisa access admin?
user.is_superuser   # All permissions?
user.date_joined    # Kapan register
user.last_login     # Last login time

# Check password
user.check_password('secret123')  # True
user.check_password('wrong')      # False
```

**Keren!** Password **NEVER** stored as plain text. Django pake hashing algorithm yang secure!

## Step 2: Login View

Di `blog_cms/urls.py`:

```python
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', 
         auth_views.LoginView.as_view(template_name='blog/login.html'), 
         name='login'),
    path('logout/', 
         auth_views.LogoutView.as_view(), 
         name='logout'),
]
```

**LoginView:**
- Handles GET (show form) dan POST (process login)
- Checks username/password
- Creates session on success
- Redirects ke `LOGIN_REDIRECT_URL`

Di `blog_cms/settings.py`:

```python
LOGIN_URL = 'login'             # Redirect kesini kalo belum login
LOGIN_REDIRECT_URL = 'home'     # Redirect kesini setelah login
LOGOUT_REDIRECT_URL = 'home'    # Redirect kesini setelah logout
```

Login Template (`blog/templates/blog/login.html`):

```django
{% extends 'blog/base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
<div class="auth-container">
    <h2>Login</h2>
    
    {% if form.errors %}
        <div class="alert alert-danger">
            Invalid username or password.
        </div>
    {% endif %}
    
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Login</button>
        <input type="hidden" name="next" value="{{ next }}">
    </form>
    
    <p>Don't have an account? <a href="{% url 'register' %}">Register here</a></p>
    <p>Forgot password? <a href="{% url 'password_reset' %}">Reset it</a></p>
</div>
{% endblock %}
```

**Key:** `{{ next }}` redirect ke original page setelah login!

## Step 3: Registration View

Di `blog/views.py`:

```python
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()              # Create user
            login(request, user)             # Log in immediately!
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})
```

**UserCreationForm** punya:
- `username` field
- `password1` field (password)
- `password2` field (confirm password)
- Built-in validation buat password strength!

## Step 4: Custom Registration Form

Form default cuma punya username & password. Mari tambahin email:

```python
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# Update view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Custom!
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})
```

## Step 5: Protecting Views

Use `@login_required` buat protect views:

```python
from django.contrib.auth.decorators import login_required

@login_required
def create_post(request):
    # Cuma logged-in users yang bisa access!
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Current user!
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'blog/create_post.html', {'form': form})
```

**Apa yang terjadi:**
1. User tries to access `/post/create/`
2. Kalo belum login → redirect ke `/login/?next=/post/create/`
3. After login → redirect back ke `/post/create/`

**Magic!** ✨

## Step 6: Check Permissions di Views

```python
from django.http import HttpResponseForbidden

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # Cuma author atau staff yang bisa edit!
    if post.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You cannot edit this post.")
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})
```

## Step 7: Check Auth di Templates

Check if logged in:

```django
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
    <a href="{% url 'logout' %}">Logout</a>
{% else %}
    <a href="{% url 'login' %}">Login</a>
    <a href="{% url 'register' %}">Register</a>
{% endif %}
```

Check permissions:

```django
{% if post.author == user or user.is_staff %}
    <a href="{% url 'edit_post' post.slug %}">Edit</a>
    <a href="{% url 'delete_post' post.slug %}">Delete</a>
{% endif %}
```

Show user info:

```django
{% if user.is_authenticated %}
    <p>Logged in as {{ user.username }}</p>
    <p>Email: {{ user.email }}</p>
    <p>Joined: {{ user.date_joined|date:"F d, Y" }}</p>
{% endif %}
```

## Step 8: Password Reset

Django provides password reset views. Di `blog_cms/urls.py`:

```python
urlpatterns = [
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='blog/password_reset.html'
         ), name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='blog/password_reset_done.html'
         ), name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='blog/password_reset_confirm.html'
         ), name='password_reset_confirm'),
    
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='blog/password_reset_complete.html'
         ), name='password_reset_complete'),
]
```

**The Flow:**

1. **Password Reset:** User enters email
2. **Done:** Confirm email sent
3. **Confirm:** User clicks link, enters new password
4. **Complete:** Success!

Configure email (development) di `settings.py`:

```python
# Development: Print emails ke console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Production: Use real email server
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-app-password'
```

## Step 9: Sessions

Django pake sessions buat remember logged-in users.

**How it works:**

1. User logs in
2. Django creates session ID
3. Session ID stored di cookie
4. Cookie sent dengan every request
5. Django loads user dari session

**Analogi:** Kayak token di localStorage JavaScript, tapi lebih secure karena HTTP-only cookies!

Store data di session:

```python
# In view
request.session['favorite_color'] = 'blue'

# Later
color = request.session.get('favorite_color')  # 'blue'

# Delete
del request.session['favorite_color']
```

Session settings:

```python
# In settings.py
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = False
```

## Step 10: User Profile (Advanced)

Buat tambahin more user fields, bikin Profile model:

```python
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'

# Auto-create profile when user registers
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)
```

Access profile:

```python
# In view
user = request.user
bio = user.profile.bio

# In template
{{ user.profile.bio }}
{{ user.profile.avatar.url }}
```

## Authentication Helpers

```python
from django.contrib.auth import authenticate, login, logout

# Authenticate
user = authenticate(username='john', password='secret')
if user is not None:
    login(request, user)

# Logout
logout(request)

# Check if authenticated
if request.user.is_authenticated:
    print(f'User: {request.user.username}')

# Check staff
if request.user.is_staff:
    print('Staff member')

# Check superuser
if request.user.is_superuser:
    print('Superuser - all permissions!')
```

Decorators:

```python
from django.contrib.auth.decorators import login_required, user_passes_test

# Require login
@login_required
def my_view(request):
    pass

# Custom check
def is_author(user):
    return user.groups.filter(name='Authors').exists()

@user_passes_test(is_author)
def authors_only(request):
    pass

# Staff only
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def staff_view(request):
    pass
```

## Permissions System

```python
# Check permission
if user.has_perm('blog.add_post'):
    # Bisa add posts
    pass

# Add permission di model
class Post(models.Model):
    class Meta:
        permissions = [
            ('can_publish', 'Can publish posts'),
        ]

# Check custom permission
if user.has_perm('blog.can_publish'):
    pass

# In decorator
from django.contrib.auth.decorators import permission_required

@permission_required('blog.add_post')
def create_post(request):
    pass
```

## Security Best Practices

### 1. Never Store Passwords in Plain Text
Django hashes automatically! ✅

### 2. Use HTTPS in Production
```python
# settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 3. Strong Password Validators
```python
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

### 4. Protect Views
Use `@login_required` and check permissions!

### 5. Logout Properly
```python
logout(request)  # Clear session
```

## Common Patterns

### Login and Redirect to Next

```python
def login_view(request):
    if request.method == 'POST':
        # ... authenticate
        if user:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
```

### Remember Me

```python
def login_view(request):
    if request.method == 'POST':
        remember = request.POST.get('remember_me')
        if not remember:
            request.session.set_expiry(0)  # Expire at browser close
```

## Troubleshooting

### User Not Authenticated
Check:
- `@login_required` decorator added?
- User actually logged in?
- Session working?

### Password Reset Email Not Received
Check:
- Email backend configured?
- Check console (development mode)
- Check spam folder (production)

### CSRF Token Missing
- Add `{% csrf_token %}` in forms
- Check CSRF middleware enabled

## Checklist

Sebelum lanjut:

- ✅ Login view working
- ✅ Registration working
- ✅ Logout working
- ✅ Password reset configured
- ✅ `@login_required` protecting views
- ✅ Permissions checked
- ✅ Auth status shown di templates

## Kesimpulan

Lo udah belajar:

✅ Django User model  
✅ Login & logout  
✅ Registration dengan UserCreationForm  
✅ Custom registration form  
✅ `@login_required` decorator  
✅ Check permissions  
✅ Password reset flow  
✅ Sessions  
✅ Security best practices  

**Django authentication powerful!** Built-in, secure, dan production-ready!

## Next Steps

Authentication done! Sekarang bikin aplikasi lo jadi cantik dengan CSS.

**→ Continue to [09 - Styling](./09-styling.md)**

## Additional Resources

- [Authentication Docs](https://docs.djangoproject.com/en/stable/topics/auth/)
- [User Model Reference](https://docs.djangoproject.com/en/stable/ref/contrib/auth/)
