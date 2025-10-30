# Tutorial 03: Creating Models

## What You'll Learn

- What Django models are and how they work
- Create database models for Blog, Comment, and Category
- Understand field types and relationships
- Create and apply database migrations
- Test models in Django shell

## What Are Models?

Models are Python classes that represent database tables. Django's ORM (Object-Relational Mapping) converts these classes into SQL automatically.

**Example:**
```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
```

Django creates this SQL:
```sql
CREATE TABLE blog_post (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200),
    content TEXT
);
```

## Understanding Relationships

Our blog has three main entities with relationships:

```
┌──────────┐         ┌──────────┐         ┌──────────┐
│ Category │         │   Post   │         │ Comment  │
└─────┬────┘         └────┬─────┘         └────┬─────┘
      │                   │                     │
      │                   │                     │
      │    One-to-Many    │    One-to-Many     │
      └───────────────────┤                     │
                          │                     │
                          └─────────────────────┘
                          
┌─────────┐
│  User   │ (Django built-in)
└────┬────┘
     │  One-to-Many
     │
     ▼
  Post & Comment
```

- **Category → Posts:** One category has many posts
- **Post → Comments:** One post has many comments  
- **User → Posts:** One user writes many posts
- **User → Comments:** One user writes many comments

## Step 1: Create the Category Model

Open `blog/models.py` and start fresh:

```python
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Category model for organizing blog posts"""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category_posts", kwargs={"slug": self.slug})
```

### Understanding the Category Model

**Fields:**
- `name`: Category name (e.g., "Technology")
  - `max_length=100`: Maximum 100 characters
  - `unique=True`: No duplicate names
  
- `slug`: URL-friendly version (e.g., "technology")
  - `SlugField`: Only allows letters, numbers, hyphens
  - `blank=True`: Can be empty in forms
  
- `description`: Optional description
  - `TextField`: Unlimited text
  - `blank=True`: Optional field
  
- `created_at`: When category was created
  - `auto_now_add=True`: Set automatically on creation

**Meta class:**
- `verbose_name_plural`: How it appears in admin (fixes "Categorys")
- `ordering`: Default sort order

**Methods:**
- `__str__()`: How object appears in admin (shows name)
- `save()`: Automatically creates slug from name
- `get_absolute_url()`: Returns URL for this category

## Step 2: Create the Post Model

Add this after the Category model:

```python
class Post(models.Model):
    """Blog post model"""
    
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    content = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True)
    featured_image = models.ImageField(upload_to="posts/%Y/%m/%d/", blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["-published_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    @property
    def approved_comments(self):
        return self.comments.filter(approved=True)
```

### Understanding the Post Model

**New Field Types:**

- `ForeignKey`: Relationship to another model
  ```python
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  ```
  - Links to Django's User model
  - `on_delete=models.CASCADE`: Delete posts if user is deleted
  - `related_name="posts"`: Access user's posts with `user.posts.all()`

- `ImageField`: Stores images
  ```python
  featured_image = models.ImageField(upload_to="posts/%Y/%m/%d/")
  ```
  - `upload_to`: Where to save (e.g., `posts/2025/10/30/image.jpg`)
  - Requires Pillow library

- `ChoiceField`: Dropdown with predefined choices
  ```python
  status = models.CharField(choices=STATUS_CHOICES)
  ```

**Special Fields:**
- `auto_now_add=True`: Set once on creation
- `auto_now=True`: Update on every save
- `null=True`: Database can store NULL
- `blank=True`: Form can be empty

**Indexes:**
```python
indexes = [
    models.Index(fields=["-published_at"]),
]
```
Makes queries faster (like a book index).

**Property:**
```python
@property
def approved_comments(self):
    return self.comments.filter(approved=True)
```
Use like: `post.approved_comments` (no parentheses!)

## Step 3: Create the Comment Model

Add this after the Post model:

```python
class Comment(models.Model):
    """Comment model for blog posts"""
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=1000)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["post", "approved"]),
        ]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
```

### Understanding the Comment Model

**Key Features:**

- `BooleanField`: True/False field
  ```python
  approved = models.BooleanField(default=False)
  ```
  Comments need approval by default

- Multiple ForeignKeys: Comments relate to both Post and User

- Complex `__str__`: Shows who commented on what

## Step 4: Create Database Migrations

Migrations are Django's way of tracking database changes.

### Create Migration Files

```bash
python manage.py makemigrations
```

You'll see:
```
Migrations for 'blog':
  blog/migrations/0001_initial.py
    - Create model Category
    - Create model Post
    - Create model Comment
    - Create indexes
```

### View the Migration

Open `blog/migrations/0001_initial.py` to see what Django created. It's Python code that creates tables!

### Apply Migrations

```bash
python manage.py migrate
```

Output:
```
Running migrations:
  Applying blog.0001_initial... OK
```

**What happened?** Django created three tables in the database:
- `blog_category`
- `blog_post`
- `blog_comment`

## Step 5: Test Models in Django Shell

Django shell lets you interact with models directly:

```bash
python manage.py shell
```

### Test 1: Create a Category

```python
from blog.models import Category

# Create a category
tech = Category.objects.create(
    name="Technology",
    description="All about tech"
)

print(tech.name)        # Technology
print(tech.slug)        # technology (auto-generated!)
print(tech.created_at)  # Current datetime
```

### Test 2: Create a Post

```python
from blog.models import Post
from django.contrib.auth.models import User

# Get your admin user
user = User.objects.first()

# Create a post
post = Post.objects.create(
    title="My First Post",
    content="This is the content of my first post!",
    author=user,
    category=tech,
    status="published"
)

print(post.slug)  # my-first-post
```

### Test 3: Test Relationships

```python
# Get all posts in tech category
tech_posts = tech.posts.all()
print(tech_posts)

# Get post's category
print(post.category.name)  # Technology

# Get author's posts
user_posts = user.posts.all()
print(user_posts)
```

### Test 4: Create a Comment

```python
from blog.models import Comment

comment = Comment.objects.create(
    post=post,
    author=user,
    content="Great post!",
    approved=True
)

# Get all comments on post
print(post.comments.all())

# Get approved comments
print(post.approved_comments)
```

Exit the shell:
```python
exit()
```

## Understanding ORM Queries

Django ORM translates Python to SQL:

```python
# Python
Post.objects.filter(status="published")

# SQL generated
SELECT * FROM blog_post WHERE status = 'published';
```

Common query methods:

```python
# Get all objects
Post.objects.all()

# Filter objects
Post.objects.filter(status="published")

# Get one object
Post.objects.get(id=1)

# Create object
Post.objects.create(title="Test", ...)

# Count objects
Post.objects.count()

# Order objects
Post.objects.order_by("-created_at")

# Related objects
post.comments.all()
user.posts.filter(status="published")
```

## Common Model Field Types

```python
# Text fields
CharField(max_length=100)          # Short text
TextField()                         # Long text
SlugField(max_length=50)           # URL-friendly text
EmailField()                        # Email validation

# Numeric fields
IntegerField()                      # Integers
DecimalField(max_digits=10, decimal_places=2)  # Decimals
FloatField()                        # Floating point

# Date/Time fields
DateField()                         # Date only
TimeField()                         # Time only
DateTimeField()                     # Date and time

# Other fields
BooleanField()                      # True/False
FileField(upload_to="files/")      # File upload
ImageField(upload_to="images/")    # Image upload
URLField()                          # URL validation

# Relationships
ForeignKey(Model, on_delete=...)   # Many-to-one
ManyToManyField(Model)             # Many-to-many
OneToOneField(Model, on_delete=...) # One-to-one
```

## Field Options

```python
# Common options
null=True          # Database allows NULL
blank=True         # Form allows empty
default="value"    # Default value
unique=True        # Must be unique
choices=CHOICES    # Dropdown options
db_index=True      # Create database index

# Auto fields
auto_now=True          # Update on every save
auto_now_add=True      # Set once on creation
editable=False         # Hide from forms
```

## on_delete Options

What happens when related object is deleted?

```python
# CASCADE: Delete this object too
author = models.ForeignKey(User, on_delete=models.CASCADE)
# If user deleted → delete all their posts

# SET_NULL: Set to NULL
category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
# If category deleted → set post.category = NULL

# PROTECT: Prevent deletion
# Can't delete if related objects exist

# SET_DEFAULT: Set to default value
# Requires default= parameter

# DO_NOTHING: Do nothing (dangerous!)
```

## Model Meta Options

```python
class Meta:
    # Sorting
    ordering = ["-created_at"]         # Newest first
    ordering = ["name"]                # Alphabetical
    
    # Display names
    verbose_name = "Blog Post"
    verbose_name_plural = "Blog Posts"
    
    # Database
    db_table = "custom_table_name"
    indexes = [models.Index(fields=["field"])]
    
    # Uniqueness
    unique_together = [["field1", "field2"]]
```

## Troubleshooting

### Issue: "No module named 'PIL'"
```bash
pip install Pillow
```

### Issue: Migration errors
```bash
# Delete migrations and database
rm blog/migrations/0*.py
rm db.sqlite3

# Recreate
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Issue: "related_name conflicts"
Each ForeignKey needs unique `related_name` or it conflicts.

### Issue: Can't create object in shell
Make sure you imported the model:
```python
from blog.models import Post, Category, Comment
```

## Best Practices

1. **Always use `__str__`**: Makes admin and shell readable
2. **Use `related_name`**: Makes reverse queries clear
3. **Add indexes**: For fields you filter/search often
4. **Use `blank=True` wisely**: Only for truly optional fields
5. **Create slugs**: Better URLs than IDs
6. **Validate in model**: Don't rely only on forms

## Checklist

Before moving on, verify:

- ✅ Three models created (Category, Post, Comment)
- ✅ Relationships working (ForeignKeys)
- ✅ Migrations created and applied
- ✅ Models tested in Django shell
- ✅ Can create categories, posts, and comments
- ✅ Auto-slug generation works
- ✅ Related queries work (post.comments.all())

## Next Steps

Now that we have our database structure, let's register these models in the Django admin panel!

**→ Continue to [04 - Django Admin](./04-django-admin.md)**

---

## Additional Resources

- [Django Model Field Reference](https://docs.djangoproject.com/en/stable/ref/models/fields/)
- [QuerySet API Reference](https://docs.djangoproject.com/en/stable/ref/models/querysets/)
- [Model Meta Options](https://docs.djangoproject.com/en/stable/ref/models/options/)
