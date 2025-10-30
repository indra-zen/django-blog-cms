# Tutorial 06: Templates dan UI

## Apa yang Bakal Lo Pelajari

- Template language Django (bukan React/Vue, tapi powerful juga!)
- Template inheritance buat reusable layout
- Template tags dan filters
- Display dynamic data
- Forms di templates
- Navigation dan layout

## Apa Itu Templates?

Templates itu HTML files dengan special syntax Django buat:
- Nampilin variables: `{{ variable }}`
- Logic/loops: `{% if %} {% for %}`
- Inheritance: `{% extends %} {% block %}`

### Analogi

Bayangin lo bikin website pake JavaScript:
```javascript
// Di JS lo pake template literals
const html = `
  <h1>${title}</h1>
  <p>${content}</p>
`;
```

Di Django templates:
```django
<h1>{{ title }}</h1>
<p>{{ content }}</p>
```

**Mirip kan?** Bedanya Django render di **server**, bukan di browser!

## Struktur Directory Templates

```
blog/templates/blog/
├── base.html              # Base layout (kayak App.js di React)
├── home.html              # Homepage
├── post_detail.html       # Post detail
├── create_post.html       # Create post
├── edit_post.html         # Edit post
├── delete_post.html       # Delete confirmation
├── user_posts.html        # User's posts
├── category_posts.html    # Category posts
├── login.html             # Login page
├── register.html          # Register page
└── password_reset*.html   # Password reset pages
```

**Kenapa `blog/templates/blog/`?**
- Django cari templates di semua apps
- Double nesting prevents name conflicts
- Best practice Django!

## Step 1: Bikin Base Template

Ini kayak **layout utama** yang dipake semua page.

Create `blog/templates/blog/base.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Blog CMS{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <div class="nav-brand">
                <a href="{% url 'home' %}">Blog CMS</a>
            </div>
            <div class="nav-menu">
                <a href="{% url 'home' %}">Home</a>
                {% if user.is_authenticated %}
                    <a href="{% url 'create_post' %}">Create Post</a>
                    <a href="{% url 'user_posts' %}">My Posts</a>
                    <a href="{% url 'admin:index' %}">Admin</a>
                    <span class="nav-user">Hello, {{ user.username }}</span>
                    <a href="{% url 'logout' %}">Logout</a>
                {% else %}
                    <a href="{% url 'login' %}">Login</a>
                    <a href="{% url 'register' %}">Register</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <main class="main-content">
        <div class="container">
            {% if messages %}
                <div class="messages">
                    {% for message in messages %}
                        <div class="message {{ message.tags }}">
                            {{ message }}
                        </div>
                    {% endfor %}
                </div>
            {% endif %}

            {% block content %}
            {% endblock %}
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2025 Blog CMS. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
```

### Penjelasan Base Template

**1. Load Static Files**
```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```
Loads CSS dari `static/css/style.css`.

**Analogi JavaScript:**
```javascript
import './style.css';  // Di React
```

**2. Block Tags**
```django
{% block title %}Blog CMS{% endblock %}
```
Child templates bisa override block ini!

**Analogi React:**
```jsx
// Base component
function Layout({ title, children }) {
  return (
    <>
      <title>{title || 'Blog CMS'}</title>
      {children}
    </>
  );
}
```

**3. URL Tag**
```django
<a href="{% url 'home' %}">Home</a>
```
Generate URL dari name (NO HARDCODING!).

**Kenapa?** Kalo lo ganti `/home/` jadi `/homepage/`, cukup update URLs.py. Template ga perlu diubah!

**4. If Statement**
```django
{% if user.is_authenticated %}
    <span>Hello, {{ user.username }}</span>
{% else %}
    <a href="{% url 'login' %}">Login</a>
{% endif %}
```

**Analogi JavaScript:**
```jsx
{user.isAuthenticated ? (
  <span>Hello, {user.username}</span>
) : (
  <a href="/login">Login</a>
)}
```

**5. For Loop**
```django
{% for message in messages %}
    <div>{{ message }}</div>
{% endfor %}
```

**Analogi JavaScript:**
```jsx
{messages.map(message => (
  <div key={message.id}>{message}</div>
))}
```

**6. Variables**
```django
{{ user.username }}
```
Display variable value. Auto-escaped untuk security!

## Step 2: Bikin Home Template

Create `blog/templates/blog/home.html`:

```django
{% extends 'blog/base.html' %}

{% block title %}Home - Blog CMS{% endblock %}

{% block content %}
<div class="home-page">
    <div class="search-bar">
        <form method="get" action="{% url 'home' %}">
            <input type="text" name="q" placeholder="Search posts..." value="{{ search_query }}">
            <button type="submit">Search</button>
        </form>
    </div>

    <div class="categories">
        <h3>Categories</h3>
        <ul class="category-list">
            <li><a href="{% url 'home' %}" {% if not category_slug %}class="active"{% endif %}>All</a></li>
            {% for category in categories %}
                <li>
                    <a href="?category={{ category.slug }}" 
                       {% if category_slug == category.slug %}class="active"{% endif %}>
                        {{ category.name }}
                    </a>
                </li>
            {% endfor %}
        </ul>
    </div>

    <div class="posts-list">
        <h1>Latest Posts</h1>
        
        {% if page_obj %}
            {% for post in page_obj %}
                <article class="post-card">
                    {% if post.featured_image %}
                        <div class="post-image">
                            <img src="{{ post.featured_image.url }}" alt="{{ post.title }}">
                        </div>
                    {% endif %}
                    <div class="post-content">
                        <h2><a href="{% url 'post_detail' post.slug %}">{{ post.title }}</a></h2>
                        <div class="post-meta">
                            <span class="author">By {{ post.author.username }}</span>
                            <span class="date">{{ post.published_at|date:"F d, Y" }}</span>
                            {% if post.category %}
                                <span class="category">
                                    <a href="?category={{ post.category.slug }}">{{ post.category.name }}</a>
                                </span>
                            {% endif %}
                        </div>
                        {% if post.excerpt %}
                            <p class="excerpt">{{ post.excerpt }}</p>
                        {% else %}
                            <p class="excerpt">{{ post.content|truncatewords:30 }}</p>
                        {% endif %}
                        <a href="{% url 'post_detail' post.slug %}" class="read-more">Read More →</a>
                    </div>
                </article>
            {% endfor %}

            {% if page_obj.has_other_pages %}
                <div class="pagination">
                    {% if page_obj.has_previous %}
                        <a href="?page=1{% if search_query %}&q={{ search_query }}{% endif %}{% if category_slug %}&category={{ category_slug }}{% endif %}">First</a>
                        <a href="?page={{ page_obj.previous_page_number }}{% if search_query %}&q={{ search_query }}{% endif %}{% if category_slug %}&category={{ category_slug }}{% endif %}">Previous</a>
                    {% endif %}

                    <span class="current-page">
                        Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
                    </span>

                    {% if page_obj.has_next %}
                        <a href="?page={{ page_obj.next_page_number }}{% if search_query %}&q={{ search_query }}{% endif %}{% if category_slug %}&category={{ category_slug }}{% endif %}">Next</a>
                        <a href="?page={{ page_obj.paginator.num_pages }}{% if search_query %}&q={{ search_query }}{% endif %}{% if category_slug %}&category={{ category_slug }}{% endif %}">Last</a>
                    {% endif %}
                </div>
            {% endif %}
        {% else %}
            <p class="no-posts">No posts available yet. Be the first to create one!</p>
        {% endif %}
    </div>
</div>
{% endblock %}
```

### Penjelasan Home Template

**1. Template Inheritance**
```django
{% extends 'blog/base.html' %}
```
Inherit dari `base.html`. Content masuk ke `{% block content %}`.

**2. Accessing Nested Attributes**
```django
{{ post.author.username }}
{{ post.category.name }}
```
Pake dot notation buat access related objects!

**Analogi JavaScript:**
```javascript
post.author.username
post.category.name
```

**3. Template Filters**
```django
{{ post.published_at|date:"F d, Y" }}
{{ post.content|truncatewords:30 }}
```

Filters = pipe (`|`) function buat transform data.

- `|date:"F d, Y"` → Format date jadi "October 30, 2025"
- `|truncatewords:30` → Ambil 30 kata pertama

**Analogi JavaScript:**
```javascript
// date filter
new Date(post.published_at).toLocaleDateString('en-US', {
  year: 'numeric',
  month: 'long',
  day: 'numeric'
});

// truncatewords filter
post.content.split(' ').slice(0, 30).join(' ');
```

**4. Form dengan GET**
```django
<form method="get" action="{% url 'home' %}">
    <input type="text" name="q" value="{{ search_query }}">
</form>
```

Sends data as URL parameters: `?q=django&category=tech`

**5. Pagination**
```django
{% if page_obj.has_other_pages %}
    {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
    {% endif %}
{% endif %}
```

Django paginator provides:
- `page_obj.number` - Current page
- `page_obj.paginator.num_pages` - Total pages
- `page_obj.has_previous/has_next` - Boolean
- `page_obj.previous_page_number/next_page_number` - Page numbers

## Step 3: Bikin Post Detail Template

Create `blog/templates/blog/post_detail.html`:

```django
{% extends 'blog/base.html' %}

{% block title %}{{ post.title }} - Blog CMS{% endblock %}

{% block content %}
<article class="post-detail">
    <header class="post-header">
        <h1>{{ post.title }}</h1>
        <div class="post-meta">
            <span class="author">By {{ post.author.username }}</span>
            <span class="date">{{ post.published_at|date:"F d, Y" }}</span>
            {% if post.category %}
                <span class="category">
                    <a href="{% url 'category_posts' post.category.slug %}">{{ post.category.name }}</a>
                </span>
            {% endif %}
        </div>
        
        {% if user == post.author or user.is_staff %}
            <div class="post-actions">
                <a href="{% url 'edit_post' post.slug %}" class="btn btn-secondary">Edit</a>
                <a href="{% url 'delete_post' post.slug %}" class="btn btn-danger">Delete</a>
            </div>
        {% endif %}
    </header>

    {% if post.featured_image %}
        <div class="post-featured-image">
            <img src="{{ post.featured_image.url }}" alt="{{ post.title }}">
        </div>
    {% endif %}

    <div class="post-content">
        {{ post.content|linebreaks }}
    </div>

    <div class="post-footer">
        <p class="updated-date">Last updated: {{ post.updated_at|date:"F d, Y" }}</p>
    </div>
</article>

<section class="comments-section">
    <h2>Comments ({{ comments.count }})</h2>

    {% if user.is_authenticated %}
        <div class="comment-form">
            <h3>Leave a Comment</h3>
            <form method="post">
                {% csrf_token %}
                {{ comment_form.as_p }}
                <button type="submit" class="btn btn-primary">Submit Comment</button>
            </form>
        </div>
    {% else %}
        <p class="login-prompt">
            <a href="{% url 'login' %}?next={{ request.path }}">Login</a> to leave a comment.
        </p>
    {% endif %}

    <div class="comments-list">
        {% for comment in comments %}
            <div class="comment">
                <div class="comment-header">
                    <strong>{{ comment.author.username }}</strong>
                    <span class="comment-date">{{ comment.created_at|date:"F d, Y" }}</span>
                </div>
                <div class="comment-body">
                    {{ comment.content|linebreaks }}
                </div>
            </div>
        {% empty %}
            <p class="no-comments">No comments yet. Be the first to comment!</p>
        {% endfor %}
    </div>
</section>
{% endblock %}
```

### Penjelasan Post Detail

**1. Permission Check**
```django
{% if user == post.author or user.is_staff %}
    <a href="{% url 'edit_post' post.slug %}">Edit</a>
{% endif %}
```
Cuma author atau staff yang bisa edit!

**2. CSRF Token**
```django
<form method="post">
    {% csrf_token %}
    ...
</form>
```

**WAJIB!** Buat semua POST forms. Prevents CSRF attacks.

**Apa itu CSRF?** Cross-Site Request Forgery = orang jahat bikin form palsu buat submit data atas nama lo.

CSRF token = unique random token yang di-generate Django. Kalo ga match, request ditolak!

**3. Display Form**
```django
{{ comment_form.as_p }}
```
Renders all form fields wrapped in `<p>` tags.

Options lain:
- `form.as_table` - Wrapped in `<tr>` tags
- `form.as_ul` - Wrapped in `<li>` tags
- Manual: `{{ form.field_name }}`

**4. Empty For Loop**
```django
{% for comment in comments %}
    {{ comment.content }}
{% empty %}
    <p>No comments yet!</p>
{% endfor %}
```

**Keren!** Ga perlu if statement terpisah buat check empty.

**Analogi JavaScript:**
```jsx
{comments.length > 0 ? (
  comments.map(c => <div>{c.content}</div>)
) : (
  <p>No comments yet!</p>
)}
```

**5. linebreaks Filter**
```django
{{ post.content|linebreaks }}
```
Converts line breaks to `<br>` or `<p>` tags.

**Input:**
```
Hello world
This is a test
```

**Output:**
```html
<p>Hello world<br>This is a test</p>
```

**6. Login with Redirect**
```django
<a href="{% url 'login' %}?next={{ request.path }}">Login</a>
```

After login, Django redirects ke URL di `next` parameter. User ga perlu navigate lagi!

## Step 4: Bikin Form Templates

### Create Post

Create `blog/templates/blog/create_post.html`:

```django
{% extends 'blog/base.html' %}

{% block title %}Create Post - Blog CMS{% endblock %}

{% block content %}
<div class="create-post-page">
    <h1>Create New Post</h1>
    
    <form method="post" enctype="multipart/form-data" class="post-form">
        {% csrf_token %}
        {{ form.as_p }}
        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Create Post</button>
            <a href="{% url 'home' %}" class="btn btn-secondary">Cancel</a>
        </div>
    </form>
</div>
{% endblock %}
```

**PENTING:** `enctype="multipart/form-data"` **WAJIB** buat file uploads!

Tanpa ini, file uploads ga bakal work! 😱

### Edit Post

Create `blog/templates/blog/edit_post.html`:

```django
{% extends 'blog/base.html' %}

{% block title %}Edit Post - Blog CMS{% endblock %}

{% block content %}
<div class="edit-post-page">
    <h1>Edit Post</h1>
    
    <form method="post" enctype="multipart/form-data" class="post-form">
        {% csrf_token %}
        {{ form.as_p }}
        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Update Post</button>
            <a href="{% url 'post_detail' post.slug %}" class="btn btn-secondary">Cancel</a>
        </div>
    </form>
</div>
{% endblock %}
```

### Delete Confirmation

Create `blog/templates/blog/delete_post.html`:

```django
{% extends 'blog/base.html' %}

{% block title %}Delete Post - Blog CMS{% endblock %}

{% block content %}
<div class="delete-post-page">
    <h1>Delete Post</h1>
    
    <div class="delete-warning">
        <p>Are you sure you want to delete the post "<strong>{{ post.title }}</strong>"?</p>
        <p class="warning-text">This action cannot be undone.</p>
    </div>
    
    <form method="post">
        {% csrf_token %}
        <div class="form-actions">
            <button type="submit" class="btn btn-danger">Yes, Delete</button>
            <a href="{% url 'post_detail' post.slug %}" class="btn btn-secondary">Cancel</a>
        </div>
    </form>
</div>
{% endblock %}
```

Best practice: **Always confirm** sebelum delete! User bisa salah klik.

## Step 5: User Templates

### My Posts

Create `blog/templates/blog/user_posts.html`:

```django
{% extends 'blog/base.html' %}

{% block title %}My Posts - Blog CMS{% endblock %}

{% block content %}
<div class="user-posts-page">
    <h1>My Posts</h1>
    
    <div class="posts-list">
        {% if page_obj %}
            <table class="posts-table">
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Category</th>
                        <th>Status</th>
                        <th>Created</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for post in page_obj %}
                        <tr>
                            <td><a href="{% url 'post_detail' post.slug %}">{{ post.title }}</a></td>
                            <td>{{ post.category|default:"Uncategorized" }}</td>
                            <td>
                                <span class="status-badge status-{{ post.status }}">
                                    {{ post.get_status_display }}
                                </span>
                            </td>
                            <td>{{ post.created_at|date:"M d, Y" }}</td>
                            <td class="actions">
                                <a href="{% url 'edit_post' post.slug %}" class="btn-small">Edit</a>
                                <a href="{% url 'delete_post' post.slug %}" class="btn-small btn-danger">Delete</a>
                            </td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>

            {% if page_obj.has_other_pages %}
                <div class="pagination">
                    {% if page_obj.has_previous %}
                        <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
                    {% endif %}
                    <span class="current-page">
                        Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
                    </span>
                    {% if page_obj.has_next %}
                        <a href="?page={{ page_obj.next_page_number }}">Next</a>
                    {% endif %}
                </div>
            {% endif %}
        {% else %}
            <p class="no-posts">You haven't created any posts yet.</p>
            <a href="{% url 'create_post' %}" class="btn btn-primary">Create Your First Post</a>
        {% endif %}
    </div>
</div>
{% endblock %}
```

**Penjelasan baru:**
- `{{ post.get_status_display }}` - Shows "Published" instead of "published" (human-readable!)
- `{{ post.category|default:"Uncategorized" }}` - Shows default kalo value None

### Category Posts

Create `blog/templates/blog/category_posts.html`:

```django
{% extends 'blog/base.html' %}

{% block title %}{{ category.name }} - Blog CMS{% endblock %}

{% block content %}
<div class="category-posts-page">
    <h1>{{ category.name }}</h1>
    {% if category.description %}
        <p class="category-description">{{ category.description }}</p>
    {% endif %}
    
    <div class="posts-list">
        {% if page_obj %}
            {% for post in page_obj %}
                <article class="post-card">
                    {% if post.featured_image %}
                        <div class="post-image">
                            <img src="{{ post.featured_image.url }}" alt="{{ post.title }}">
                        </div>
                    {% endif %}
                    <div class="post-content">
                        <h2><a href="{% url 'post_detail' post.slug %}">{{ post.title }}</a></h2>
                        <div class="post-meta">
                            <span class="author">By {{ post.author.username }}</span>
                            <span class="date">{{ post.published_at|date:"F d, Y" }}</span>
                        </div>
                        {% if post.excerpt %}
                            <p class="excerpt">{{ post.excerpt }}</p>
                        {% else %}
                            <p class="excerpt">{{ post.content|truncatewords:30 }}</p>
                        {% endif %}
                        <a href="{% url 'post_detail' post.slug %}" class="read-more">Read More →</a>
                    </div>
                </article>
            {% endfor %}

            {% if page_obj.has_other_pages %}
                <div class="pagination">
                    {% if page_obj.has_previous %}
                        <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
                    {% endif %}
                    <span class="current-page">
                        Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
                    </span>
                    {% if page_obj.has_next %}
                        <a href="?page={{ page_obj.next_page_number }}">Next</a>
                    {% endif %}
                </div>
            {% endif %}
        {% else %}
            <p class="no-posts">No posts in this category yet.</p>
        {% endif %}
    </div>
</div>
{% endblock %}
```

## Step 6: Authentication Templates

### Login

Create `blog/templates/blog/login.html`:

```django
{% extends 'blog/base.html' %}

{% block title %}Login - Blog CMS{% endblock %}

{% block content %}
<div class="auth-page">
    <h1>Login</h1>
    
    <form method="post" class="auth-form">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">Login</button>
    </form>
    
    <div class="auth-links">
        <p>Don't have an account? <a href="{% url 'register' %}">Register here</a></p>
        <p><a href="{% url 'password_reset' %}">Forgot your password?</a></p>
    </div>
</div>
{% endblock %}
```

### Register

Create `blog/templates/blog/register.html`:

```django
{% extends 'blog/base.html' %}

{% block title %}Register - Blog CMS{% endblock %}

{% block content %}
<div class="auth-page">
    <h1>Register</h1>
    
    <form method="post" class="auth-form">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">Register</button>
    </form>
    
    <div class="auth-links">
        <p>Already have an account? <a href="{% url 'login' %}">Login here</a></p>
    </div>
</div>
{% endblock %}
```

### Password Reset Templates

Create 4 files buat password reset flow:

**1. `blog/templates/blog/password_reset.html`:**
```django
{% extends 'blog/base.html' %}
{% block title %}Password Reset - Blog CMS{% endblock %}
{% block content %}
<div class="auth-page">
    <h1>Password Reset</h1>
    <p>Enter your email address to receive password reset instructions.</p>
    <form method="post" class="auth-form">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">Send Reset Link</button>
    </form>
    <div class="auth-links">
        <p><a href="{% url 'login' %}">Back to Login</a></p>
    </div>
</div>
{% endblock %}
```

**2. `blog/templates/blog/password_reset_done.html`:**
```django
{% extends 'blog/base.html' %}
{% block title %}Password Reset Sent - Blog CMS{% endblock %}
{% block content %}
<div class="auth-page">
    <h1>Password Reset Email Sent</h1>
    <p>We've sent you instructions for resetting your password.</p>
    <div class="auth-links">
        <p><a href="{% url 'login' %}">Back to Login</a></p>
    </div>
</div>
{% endblock %}
```

**3. `blog/templates/blog/password_reset_confirm.html`:**
```django
{% extends 'blog/base.html' %}
{% block title %}Set New Password - Blog CMS{% endblock %}
{% block content %}
<div class="auth-page">
    <h1>Set New Password</h1>
    <form method="post" class="auth-form">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="btn btn-primary">Reset Password</button>
    </form>
</div>
{% endblock %}
```

**4. `blog/templates/blog/password_reset_complete.html`:**
```django
{% extends 'blog/base.html' %}
{% block title %}Password Reset Complete - Blog CMS{% endblock %}
{% block content %}
<div class="auth-page">
    <h1>Password Reset Complete</h1>
    <p>Your password has been successfully reset.</p>
    <div class="auth-links">
        <p><a href="{% url 'login' %}" class="btn btn-primary">Go to Login</a></p>
    </div>
</div>
{% endblock %}
```

## Template Tags & Filters Cheat Sheet

### Template Tags

```django
{% load static %}              # Load static files
{% url 'name' %}               # Reverse URL
{% url 'name' arg %}           # URL dengan argument
{% csrf_token %}               # CSRF protection
{% if condition %}...{% endif %} # Conditional
{% for item in list %}...{% endfor %} # Loop
{% extends 'base.html' %}      # Inherit template
{% block name %}...{% endblock %} # Define block
{% include 'partial.html' %}   # Include template
{% with var=value %}...{% endwith %} # Set variable
{% comment %}...{% endcomment %} # Comment
```

### Filters

```django
{{ value|default:"text" }}     # Default kalo None
{{ text|truncatewords:30 }}    # 30 kata pertama
{{ text|linebreaks }}          # Convert breaks to <br>
{{ date|date:"F d, Y" }}       # Format date
{{ text|length }}              # Length
{{ text|lower }}               # Lowercase
{{ text|upper }}               # Uppercase
{{ text|title }}               # Title Case
{{ text|capfirst }}            # Capitalize first
{{ number|add:5 }}             # Add 5
{{ list|join:", " }}           # Join dengan comma
{{ text|safe }}                # Mark as safe HTML
{{ text|escape }}              # Escape HTML
```

## Template Best Practices

### 1. Always Use {% csrf_token %} di POST Forms
```django
# ❌ BAD - Security risk!
<form method="post">
    {{ form.as_p }}
</form>

# ✅ GOOD
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
</form>
```

### 2. Use {% url %} Instead of Hard-Coded Paths
```django
# ❌ BAD - Hard to maintain
<a href="/posts/create/">Create</a>

# ✅ GOOD - Dynamic
<a href="{% url 'create_post' %}">Create</a>
```

### 3. Use Template Inheritance (DRY!)
```django
# ❌ BAD - Repeat header/footer di setiap file
<!DOCTYPE html>
<html>
  <head>...</head>
  <body>
    <nav>...</nav>
    <!-- Content here -->
    <footer>...</footer>
  </body>
</html>

# ✅ GOOD - Inherit dari base
{% extends 'blog/base.html' %}
{% block content %}
  <!-- Content here -->
{% endblock %}
```

### 4. Keep Logic di Views, Bukan Templates
```django
# ❌ BAD - Complex logic di template
{% if user.is_authenticated and user.is_staff or user == post.author and post.status == 'published' %}
  ...
{% endif %}

# ✅ GOOD - Logic di view
# view.py
context['can_edit'] = user_can_edit_post(user, post)

# template
{% if can_edit %}
  ...
{% endif %}
```

### 5. Use Descriptive Block Names
```django
# ❌ BAD
{% block b1 %}...{% endblock %}

# ✅ GOOD
{% block main_content %}...{% endblock %}
```

### 6. Comment Complex Template Logic
```django
{# Loop through published posts and display featured ones first #}
{% for post in posts %}
  ...
{% endfor %}
```

### 7. Escape User Input (Django Does This by Default!)
```django
# By default, Django auto-escapes:
{{ user_input }}  # <script> becomes &lt;script&gt;

# Only use |safe kalo lo YAKIN HTML-nya safe:
{{ trusted_html|safe }}
```

## Troubleshooting

### TemplateDoesNotExist
**Error:** `TemplateDoesNotExist at /posts/`

**Solusi:**
1. Check file path: `blog/templates/blog/filename.html` (double nesting!)
2. Verify app ada di `INSTALLED_APPS`
3. Check template name di `render()` call

### Static Files Ga Load
**Error:** CSS/images ga muncul

**Solusi:**
1. Run: `python manage.py collectstatic`
2. Check `STATIC_URL` dan `STATIC_ROOT` di settings
3. Pastiin `{% load static %}` ada di top of template

### Images Ga Displaying
**Error:** Featured images not showing

**Solusi:**
1. Check `MEDIA_URL` dan `MEDIA_ROOT` di settings
2. Verify media URLs added di `urls.py`
3. Use `{{ post.featured_image.url }}` not `{{ post.featured_image }}`

### CSRF Token Missing
**Error:** `CSRF verification failed`

**Solusi:**
1. Add `{% csrf_token %}` inside `<form method="post">`
2. Pastiin form pake POST method
3. Check `django.middleware.csrf.CsrfViewMiddleware` ada di settings

### URL Reverse Not Found
**Error:** `NoReverseMatch at /posts/create/`

**Solusi:**
1. Check URL name di `urls.py` matches template
2. Verify app URLs included di main `urls.py`
3. Check argument count matches

## Testing Your Templates

1. **Homepage:** Should show posts list with pagination
2. **Post detail:** Should show full post + comments
3. **Login/register:** Should work and redirect
4. **Create post:** Form should validate
5. **Edit/delete:** Only owner/staff can access
6. **Responsive:** Resize browser window

## Checklist

Before moving on:

- ✅ Base template created dengan navigation
- ✅ All page templates created
- ✅ Template inheritance working
- ✅ Static files loading
- ✅ URLs generating correctly
- ✅ Forms displaying properly
- ✅ Messages showing up
- ✅ Authentication templates work
- ✅ CSRF tokens di semua POST forms

## Kesimpulan

Lo udah belajar:

✅ Django template language syntax  
✅ Template inheritance (extends/blocks)  
✅ Template tags (url, if, for, dll)  
✅ Template filters (date, truncate, dll)  
✅ Display forms di templates  
✅ CSRF protection  
✅ Navigation dan layout structure  
✅ Conditional rendering  

**Template system Django powerful!** Ga perlu React/Vue buat dynamic pages. Django templates cukup buat most use cases!

## Next Steps

Templates done! Sekarang bikin forms buat create/edit posts.

**→ Continue to [07 - Forms](./07-forms.md)**

## Additional Resources

- [Django Template Language](https://docs.djangoproject.com/en/stable/ref/templates/language/)
- [Built-in Template Tags](https://docs.djangoproject.com/en/stable/ref/templates/builtins/)
- [Template Inheritance](https://docs.djangoproject.com/en/stable/ref/templates/language/#template-inheritance)
