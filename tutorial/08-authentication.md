# Tutorial 08: Authentication

## What You'll Learn

- Django's authentication system
- User registration
- Login and logout
- Password reset functionality
- Protecting views with decorators
- User permissions

## Understanding Authentication

**Authentication** answers: "Who are you?"
**Authorization** answers: "What can you do?"

Django provides:
- User model (`User`)
- Login/logout views
- Password hashing
- Session management
- Permission system

## Step 1: Understanding the User Model

Django's built-in User model has:

```python
from django.contrib.auth.models import User

user = User.objects.create_user(
    username='john',
    email='john@example.com',
    password='secret123'  # Automatically hashed!
)

# User attributes
user.username       # 'john'
user.email          # 'john@example.com'
user.first_name     # Optional
user.last_name      # Optional
user.is_active      # True/False
user.is_staff       # Can access admin?
user.is_superuser   # All permissions?
user.date_joined    # When registered
user.last_login     # Last login time

# Check password
user.check_password('secret123')  # True
user.check_password('wrong')      # False
```

## Step 2: Login View

We created a simple login in our main URLs. Let's understand it:

### In `blog_cms/urls.py`:

```python
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
```

**LoginView:**
- Handles GET (show form) and POST (process login)
- Uses `authentication_form` (can customize)
- Checks username/password
- Creates session on success
- Redirects to `LOGIN_REDIRECT_URL`

### In `blog_cms/settings.py`:

```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
```

**What these do:**
- `LOGIN_URL`: Where to redirect if not logged in
- `LOGIN_REDIRECT_URL`: Where to go after login
- `LOGOUT_REDIRECT_URL`: Where to go after logout

### Login Template (`blog/templates/blog/login.html`):

```html
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
        
        <div class="form-group">
            <label>Username:</label>
            {{ form.username }}
        </div>
        
        <div class="form-group">
            <label>Password:</label>
            {{ form.password }}
        </div>
        
        <button type="submit">Login</button>
        <input type="hidden" name="next" value="{{ next }}">
    </form>
    
    <p>Don't have an account? <a href="{% url 'register' %}">Register here</a></p>
    <p>Forgot password? <a href="{% url 'password_reset' %}">Reset it</a></p>
</div>
{% endblock %}
```

**Key Points:**
- `{{ next }}`: Redirect to original page after login
- `form.errors`: Show login errors
- Built-in form handles validation

## Step 3: Registration View

We created a custom registration view:

### In `blog/views.py`:

```python
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in immediately
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})
```

**Understanding the code:**

1. **`UserCreationForm`**: Built-in form with:
   - `username` field
   - `password1` field (password)
   - `password2` field (confirm password)
   - Validation for password strength

2. **`form.save()`**: Creates User and hashes password

3. **`login(request, user)`**: Logs user in immediately

### Registration Template:

```html
{% extends 'blog/base.html' %}

{% block title %}Register{% endblock %}

{% block content %}
<div class="auth-container">
    <h2>Register</h2>
    
    <form method="post">
        {% csrf_token %}
        
        {% if form.errors %}
            <div class="alert alert-danger">
                Please correct the errors below.
            </div>
        {% endif %}
        
        {{ form.as_p }}
        
        <button type="submit">Register</button>
    </form>
    
    <p>Already have an account? <a href="{% url 'login' %}">Login here</a></p>
</div>
{% endblock %}
```

## Step 4: Customizing Registration Form

The default `UserCreationForm` only has username and password. Let's add email:

```python
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        form = CustomUserCreationForm(request.POST)  # Use custom form
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})
```

## Step 5: Protecting Views

Use `@login_required` to protect views:

```python
from django.contrib.auth.decorators import login_required

@login_required
def create_post(request):
    # Only logged-in users can access
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

**What happens:**
1. User tries to access `/post/create/`
2. If not logged in → redirect to `/login/?next=/post/create/`
3. After login → redirect back to `/post/create/`

## Step 6: Checking Permissions in Views

```python
from django.http import HttpResponseForbidden

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    # Only author or staff can edit
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

## Step 7: Checking Auth in Templates

### Check if logged in:

```django
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
    <a href="{% url 'logout' %}">Logout</a>
{% else %}
    <a href="{% url 'login' %}">Login</a>
    <a href="{% url 'register' %}">Register</a>
{% endif %}
```

### Check permissions:

```django
{% if post.author == user or user.is_staff %}
    <a href="{% url 'edit_post' post.slug %}">Edit</a>
    <a href="{% url 'delete_post' post.slug %}">Delete</a>
{% endif %}
```

### Show username:

```django
{% if user.is_authenticated %}
    <p>Logged in as {{ user.username }}</p>
    <p>Email: {{ user.email }}</p>
    <p>Joined: {{ user.date_joined|date:"F d, Y" }}</p>
{% endif %}
```

## Step 8: Password Reset

Django provides password reset views. We already added them:

### In `blog_cms/urls.py`:

```python
urlpatterns = [
    # Password reset
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='blog/password_reset.html'
         ), 
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='blog/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='blog/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='blog/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]
```

**The flow:**

1. **Password Reset** (`password_reset.html`):
   - User enters email
   - System sends email with reset link

2. **Password Reset Done** (`password_reset_done.html`):
   - Confirms email sent

3. **Password Reset Confirm** (`password_reset_confirm.html`):
   - User clicks link in email
   - Enters new password

4. **Password Reset Complete** (`password_reset_complete.html`):
   - Password changed successfully

### Password Reset Template:

```html
{% extends 'blog/base.html' %}

{% block title %}Reset Password{% endblock %}

{% block content %}
<div class="auth-container">
    <h2>Reset Password</h2>
    <p>Enter your email address and we'll send you a link to reset your password.</p>
    
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Send Reset Link</button>
    </form>
</div>
{% endblock %}
```

### Configure Email (for development):

In `settings.py`:

```python
# Development: Print emails to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Production: Use real email
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-password'
```

## Step 9: Sessions

Django uses sessions to remember logged-in users.

### How it works:

1. User logs in
2. Django creates session ID
3. Session ID stored in cookie
4. Cookie sent with every request
5. Django loads user from session

### Session data:

```python
# In view
request.session['favorite_color'] = 'blue'

# Later
color = request.session.get('favorite_color')  # 'blue'

# Delete
del request.session['favorite_color']
```

### Session settings:

```python
# In settings.py
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = False
```

## Step 10: User Profile (Advanced)

To add more user fields, create a Profile model:

```python
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'

# Create profile when user registers
from django.db.models.signals import post_save

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_profile, sender=User)
```

### Access profile:

```python
# In view
user = request.user
bio = user.profile.bio

# In template
{{ user.profile.bio }}
{{ user.profile.avatar.url }}
```

## Authentication Helpers

### In Python:

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
else:
    print('Anonymous')

# Check staff
if request.user.is_staff:
    print('Staff member')

# Check superuser
if request.user.is_superuser:
    print('Superuser')
```

### Decorators:

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

Django has built-in permissions:

```python
# Check permission
if user.has_perm('blog.add_post'):
    # Can add posts
    pass

# Add permission in model
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

1. **Never store passwords in plain text**
   - Django hashes automatically
   
2. **Use HTTPS in production**
   ```python
   # settings.py
   SECURE_SSL_REDIRECT = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   ```

3. **Set strong password validators**
   ```python
   AUTH_PASSWORD_VALIDATORS = [
       {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
       {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
       {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
       {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
   ]
   ```

4. **Protect views**
   - Use `@login_required`
   - Check permissions

5. **Logout properly**
   ```python
   logout(request)
   ```

## Common Patterns

### Pattern: Login and redirect to next

```python
from django.contrib.auth import login

def login_view(request):
    if request.method == 'POST':
        # ... authenticate user
        if user:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
```

### Pattern: Remember me

```python
def login_view(request):
    if request.method == 'POST':
        remember = request.POST.get('remember_me')
        if not remember:
            request.session.set_expiry(0)  # Browser close
```

### Pattern: Account activation

```python
user = form.save(commit=False)
user.is_active = False
user.save()
# Send activation email
```

## Troubleshooting

### Issue: "User is not authenticated"
Check:
- `@login_required` decorator?
- Logged in?
- Session working?

### Issue: Password reset email not received
Check:
- Email backend configured?
- Check console (development)
- Check spam folder

### Issue: Redirect loop
Check:
- `LOGIN_URL` and `LOGIN_REDIRECT_URL`
- View not protected when it should be

### Issue: "CSRF token missing"
- Add `{% csrf_token %}` in form
- Check middleware enabled

## Testing Authentication

```python
from django.test import TestCase
from django.contrib.auth.models import User

class AuthTest(TestCase):
    def test_register(self):
        response = self.client.post('/register/', {
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        self.assertEqual(User.objects.count(), 1)
    
    def test_login(self):
        user = User.objects.create_user('test', 'test@test.com', 'pass')
        logged_in = self.client.login(username='test', password='pass')
        self.assertTrue(logged_in)
    
    def test_protected_view(self):
        # Without login
        response = self.client.get('/post/create/')
        self.assertEqual(response.status_code, 302)  # Redirect
        
        # With login
        self.client.login(username='test', password='pass')
        response = self.client.get('/post/create/')
        self.assertEqual(response.status_code, 200)  # OK
```

## Checklist

Before moving on, verify:

- ✅ Login view working
- ✅ Registration working
- ✅ Logout working
- ✅ Password reset configured
- ✅ `@login_required` protecting views
- ✅ Permissions checked in views
- ✅ Auth status shown in templates
- ✅ User created and can log in

## What You've Learned

- Django's User model
- Login and logout views
- Registration with UserCreationForm
- Customizing registration
- `@login_required` decorator
- Checking permissions
- Password reset flow
- Sessions
- Security best practices

## Next Steps

Authentication is complete! Now let's learn about styling the application.

**→ Continue to [09 - Styling with CSS](./09-styling-with-css.md)**

---

## Additional Resources

- [Authentication Documentation](https://docs.djangoproject.com/en/stable/topics/auth/)
- [User Model Reference](https://docs.djangoproject.com/en/stable/ref/contrib/auth/)
- [Password Reset Tutorial](https://docs.djangoproject.com/en/stable/topics/auth/default/#all-authentication-views)
