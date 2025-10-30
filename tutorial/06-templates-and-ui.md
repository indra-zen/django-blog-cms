# Tutorial 06: Templates and UI

## What You'll Learn

- Django template language basics
- Template inheritance with base templates
- Template tags and filters
- Creating reusable templates
- Displaying dynamic data
- Working with forms in templates
- Creating navigation and layout

## Understanding Templates

Templates are HTML files with special Django syntax for:
- Displaying variables: `{{ variable }}`
- Logic/loops: `{% if %} {% for %}`
- Template inheritance: `{% extends %} {% block %}`

## Template Directory Structure

```
blog/templates/blog/
├── base.html              # Base layout
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

## Step 1: Create Base Template

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

### Understanding Base Template

**Load Static Files:**
```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```
Loads static file from `static/css/style.css`.

**Block Tags:**
```django
{% block title %}Blog CMS{% endblock %}
```
Child templates can override this block.

**URL Tag:**
```django
<a href="{% url 'home' %}">Home</a>
```
Generates URL from URL name (no hard-coding!).

**If Statement:**
```django
{% if user.is_authenticated %}
    ...
{% else %}
    ...
{% endif %}
```
Show different content for logged-in users.

**For Loop:**
```django
{% for message in messages %}
    {{ message }}
{% endfor %}
```
Loop through messages from views.

**Variables:**
```django
{{ user.username }}
```
Display variable value.

## Step 2: Create Home Template

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

### Understanding Home Template

**Template Inheritance:**
```django
{% extends 'blog/base.html' %}
```
This template inherits from `base.html`.

**Accessing Nested Attributes:**
```django
{{ post.author.username }}
{{ post.category.name }}
```
Dot notation accesses related objects.

**Template Filters:**
```django
{{ post.published_at|date:"F d, Y" }}
{{ post.content|truncatewords:30 }}
```
- `|date:"format"`: Format date
- `|truncatewords:30`: Show first 30 words

**Form with GET:**
```django
<form method="get" action="{% url 'home' %}">
    <input type="text" name="q" value="{{ search_query }}">
</form>
```
Sends data as URL parameters.

**Pagination:**
```django
{% if page_obj.has_other_pages %}
    {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
    {% endif %}
{% endif %}
```

## Step 3: Create Post Detail Template

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

### Understanding Post Detail

**Permission Check:**
```django
{% if user == post.author or user.is_staff %}
    <a href="{% url 'edit_post' post.slug %}">Edit</a>
{% endif %}
```
Only show edit button to author or staff.

**CSRF Token:**
```django
<form method="post">
    {% csrf_token %}
    ...
</form>
```
Required for all POST forms! Prevents CSRF attacks.

**Display Form:**
```django
{{ comment_form.as_p }}
```
Renders form fields wrapped in `<p>` tags.

**Empty For Loop:**
```django
{% for comment in comments %}
    {{ comment.content }}
{% empty %}
    <p>No comments yet!</p>
{% endfor %}
```
Shows "No comments" if list is empty.

**linebreaks Filter:**
```django
{{ post.content|linebreaks }}
```
Converts line breaks to `<br>` tags.

**Login with Redirect:**
```django
<a href="{% url 'login' %}?next={{ request.path }}">Login</a>
```
After login, redirect back to this page.

## Step 4: Create Form Templates

### Create Post Template

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

**Important:** `enctype="multipart/form-data"` is required for file uploads!

### Edit Post Template

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

## Step 5: Create User Templates

### User Posts Template

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

**Understanding:**
- `{{ post.get_status_display }}`: Shows "Published" instead of "published"
- `{{ post.category|default:"Uncategorized" }}`: Shows default if None

### Category Posts Template

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

### Login Template

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

### Register Template

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

Create these four files for password reset flow:

**`blog/templates/blog/password_reset.html`:**
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

**`blog/templates/blog/password_reset_done.html`:**
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

**`blog/templates/blog/password_reset_confirm.html`:**
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

**`blog/templates/blog/password_reset_complete.html`:**
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

## Common Template Tags & Filters

### Template Tags

```django
{% load static %}              # Load static files
{% url 'name' %}               # Reverse URL
{% url 'name' arg %}           # URL with argument
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
{{ value|default:"text" }}     # Default if None
{{ text|truncatewords:30 }}    # First 30 words
{{ text|linebreaks }}          # Convert breaks to <br>
{{ date|date:"F d, Y" }}       # Format date
{{ text|length }}              # Length
{{ text|lower }}               # Lowercase
{{ text|upper }}               # Uppercase
{{ text|title }}               # Title Case
{{ text|capfirst }}            # Capitalize first
{{ number|add:5 }}             # Add 5
{{ list|join:", " }}           # Join with comma
{{ text|safe }}                # Mark as safe HTML
{{ text|escape }}              # Escape HTML
```

## Template Best Practices

1. **Always use {% csrf_token %}** in POST forms
2. **Use {% url %}** instead of hard-coded paths
3. **Use template inheritance** (DRY principle)
4. **Keep logic in views**, not templates
5. **Use descriptive block names**
6. **Comment complex template logic**
7. **Escape user input** (Django does this by default)

## Troubleshooting

### Issue: "TemplateDoesNotExist"
- Check file path: `blog/templates/blog/filename.html`
- Verify app is in `INSTALLED_APPS`
- Check template name in `render()` call

### Issue: Static files not loading
- Run: `python manage.py collectstatic`
- Check `STATIC_URL` and `STATIC_ROOT` in settings
- Make sure `{% load static %}` is at top of template

### Issue: Images not displaying
- Check `MEDIA_URL` and `MEDIA_ROOT` in settings
- Verify media URLs are in `urls.py`
- Use `{{ post.featured_image.url }}` not just `{{ post.featured_image }}`

### Issue: CSRF token missing
- Add `{% csrf_token %}` inside `<form method="post">`
- Make sure form uses POST method

### Issue: URL reverse not found
- Check URL name in `urls.py` matches template
- Verify app URLs are included in main `urls.py`

## Testing Your Templates

1. **Visit homepage:** Should show posts list
2. **Click on a post:** Should show post detail
3. **Try logging in:** Should redirect properly
4. **Create a post:** Form should work
5. **Check responsive:** Resize browser window

## Checklist

Before moving on, verify:

- ✅ Base template created with navigation
- ✅ All page templates created
- ✅ Template inheritance working
- ✅ Static files loading
- ✅ URLs generating correctly
- ✅ Forms displaying properly
- ✅ Messages showing up
- ✅ Authentication templates work

## What You've Learned

- Django template language syntax
- Template inheritance with extends/blocks
- Template tags (url, if, for, etc.)
- Template filters (date, truncate, etc.)
- Displaying forms in templates
- CSRF protection
- Navigation and layout structure
- Conditional rendering

## Next Steps

Templates are done! Now let's create the forms for creating and editing posts.

**→ Continue to [07 - Forms](./07-forms.md)**

---

## Additional Resources

- [Django Template Language](https://docs.djangoproject.com/en/stable/ref/templates/language/)
- [Built-in Template Tags](https://docs.djangoproject.com/en/stable/ref/templates/builtins/)
- [Template Inheritance](https://docs.djangoproject.com/en/stable/ref/templates/language/#template-inheritance)
