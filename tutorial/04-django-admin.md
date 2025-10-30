# Tutorial 04: Django Admin

## What You'll Learn

- Register models in Django admin
- Customize admin interface
- Add search and filtering
- Create custom admin actions
- Organize admin layout

## Why Use Django Admin?

Django admin is a powerful, production-ready interface for managing your data. It's like having a full content management system (CMS) with zero code!

**Without admin:** You'd need to build forms, views, and templates for CRUD operations.

**With admin:** You get it all automatically!

## Step 1: Register Basic Models

Open `blog/admin.py` and replace the contents:

```python
from django.contrib import admin
from .models import Category, Post, Comment


# Simple registration
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
```

### Test It

1. Start your server: `python manage.py runserver`
2. Go to: `http://127.0.0.1:8000/admin/`
3. Log in with your superuser credentials
4. You'll see your three models!

**Try it:**
- Click "Categories" → "Add Category"
- Fill in name and description
- Click "Save"
- Notice the slug was auto-generated!

## Step 2: Customize Category Admin

Let's make the admin more powerful. Replace the simple registration:

```python
from django.contrib import admin
from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "description"]
```

### Understanding the Code

**`@admin.register(Category)`**
- Python decorator that registers the model
- Alternative to `admin.site.register()`

**`list_display`**
```python
list_display = ["name", "slug", "created_at"]
```
Shows these columns in the list view. Before, you only saw "Category object (1)".

**`prepopulated_fields`**
```python
prepopulated_fields = {"slug": ("name",)}
```
Auto-fills slug field as you type the name in the admin form.

**`search_fields`**
```python
search_fields = ["name", "description"]
```
Adds a search box to find categories.

### Test It

Refresh the admin page:
- You now see a nice table with name, slug, and date
- Click "Add Category" - type a name and watch the slug auto-fill!
- Try the search box

## Step 3: Customize Post Admin

Posts need more customization:

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "status", "published_at", "created_at"]
    list_filter = ["status", "category", "created_at", "published_at"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ["-published_at", "-created_at"]
    raw_id_fields = ["author"]
    
    fieldsets = (
        ("Post Information", {
            "fields": ("title", "slug", "author", "category")
        }),
        ("Content", {
            "fields": ("content", "excerpt", "featured_image")
        }),
        ("Publication", {
            "fields": ("status", "published_at")
        }),
    )
```

### Understanding New Options

**`list_filter`**
```python
list_filter = ["status", "category", "created_at", "published_at"]
```
Adds filter sidebar to narrow down results:
- Filter by status (draft/published)
- Filter by category
- Filter by date

**`date_hierarchy`**
```python
date_hierarchy = "published_at"
```
Adds date drill-down navigation at the top (2025 → October → 30).

**`ordering`**
```python
ordering = ["-published_at", "-created_at"]
```
Default sort order. `-` means descending (newest first).

**`raw_id_fields`**
```python
raw_id_fields = ["author"]
```
Instead of dropdown with all users, shows a searchable popup. Better for many users.

**`fieldsets`**
```python
fieldsets = (
    ("Section Title", {
        "fields": ("field1", "field2")
    }),
)
```
Organizes the form into collapsible sections.

### Test It

Go to Posts in admin:
- See the enhanced list view with status indicators
- Use filters to show only published posts
- Use date hierarchy to find posts by month
- Click "Add Post" - see organized sections

## Step 4: Customize Comment Admin with Actions

Comments need approval, so let's add bulk actions:

```python
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "author", "created_at", "approved"]
    list_filter = ["approved", "created_at"]
    search_fields = ["content", "author__username", "post__title"]
    actions = ["approve_comments", "unapprove_comments"]
    raw_id_fields = ["post", "author"]
    
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Approve selected comments"
    
    def unapprove_comments(self, request, queryset):
        queryset.update(approved=False)
    unapprove_comments.short_description = "Unapprove selected comments"
```

### Understanding Actions

**Custom Actions**
```python
def approve_comments(self, request, queryset):
    queryset.update(approved=True)
```
- `self`: The admin class
- `request`: HTTP request object
- `queryset`: Selected objects

**Action Description**
```python
approve_comments.short_description = "Approve selected comments"
```
What appears in the actions dropdown.

**Search with Relations**
```python
search_fields = ["author__username", "post__title"]
```
- `author__username`: Search comment author's username
- `post__title`: Search the post title
- `__` (double underscore) traverses relationships!

### Test It

Go to Comments in admin:
1. Create a few comments (or do it in Django shell)
2. Select multiple comments (checkboxes)
3. Choose "Approve selected comments" from actions dropdown
4. Click "Go"
5. Comments are now approved!

## Step 5: Enhance with List Editing

Make the comment admin even better:

```python
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "author", "content_preview", "created_at", "approved"]
    list_filter = ["approved", "created_at"]
    list_editable = ["approved"]  # Add this
    search_fields = ["content", "author__username", "post__title"]
    actions = ["approve_comments", "unapprove_comments"]
    raw_id_fields = ["post", "author"]
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Content"
    
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Approve selected comments"
    
    def unapprove_comments(self, request, queryset):
        queryset.update(approved=False)
    unapprove_comments.short_description = "Unapprove selected comments"
```

### Understanding New Features

**`list_editable`**
```python
list_editable = ["approved"]
```
Makes the "approved" field editable directly in the list view! No need to click into each comment.

**Custom Display Method**
```python
def content_preview(self, obj):
    return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
content_preview.short_description = "Content"
```
- Custom method to show truncated content
- `obj` is the Comment instance
- `short_description` sets the column header

### Test It

Refresh comments admin:
- "Approved" column now has checkboxes
- Toggle them directly in list view
- Click "Save" at bottom
- See content preview instead of full text

## Step 6: Customize the Admin Site

Make the admin feel more like yours. Create a new file `blog_cms/admin.py`:

```python
from django.contrib import admin

# Customize admin site
admin.site.site_header = "Blog CMS Administration"
admin.site.site_title = "Blog CMS Admin"
admin.site.index_title = "Welcome to Blog CMS"
```

Import it in `blog_cms/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

# Import admin customization
from . import admin as custom_admin  # Add this

urlpatterns = [
    path('admin/', admin.site.urls),
    # ... other patterns
]
```

### Test It

Refresh admin - see your custom branding!

## Complete admin.py File

Here's your complete `blog/admin.py`:

```python
from django.contrib import admin
from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "description"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "status", "published_at", "created_at"]
    list_filter = ["status", "category", "created_at", "published_at"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ["-published_at", "-created_at"]
    raw_id_fields = ["author"]
    
    fieldsets = (
        ("Post Information", {
            "fields": ("title", "slug", "author", "category")
        }),
        ("Content", {
            "fields": ("content", "excerpt", "featured_image")
        }),
        ("Publication", {
            "fields": ("status", "published_at")
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "author", "content_preview", "created_at", "approved"]
    list_filter = ["approved", "created_at"]
    list_editable = ["approved"]
    search_fields = ["content", "author__username", "post__title"]
    actions = ["approve_comments", "unapprove_comments"]
    raw_id_fields = ["post", "author"]
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Content"
    
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Approve selected comments"
    
    def unapprove_comments(self, request, queryset):
        queryset.update(approved=False)
    unapprove_comments.short_description = "Unapprove selected comments"
```

## Common Admin Options Reference

### List View Options

```python
class MyModelAdmin(admin.ModelAdmin):
    # What columns to show
    list_display = ["field1", "field2", "method"]
    
    # Which fields can be edited in list
    list_editable = ["field1"]
    
    # Add filters sidebar
    list_filter = ["field1", "date_field"]
    
    # Add search box
    search_fields = ["field1", "related__field"]
    
    # Default sorting
    ordering = ["-date_field"]
    
    # How many per page
    list_per_page = 50
    
    # Show select all checkbox
    list_select_related = ["foreign_key"]
```

### Form Options

```python
class MyModelAdmin(admin.ModelAdmin):
    # Auto-fill fields
    prepopulated_fields = {"slug": ("title",)}
    
    # Use popup for foreign keys
    raw_id_fields = ["foreign_key"]
    
    # Organize into sections
    fieldsets = (
        ("Section", {
            "fields": ("field1", "field2"),
            "classes": ("collapse",)  # Collapsible
        }),
    )
    
    # Which fields to show
    fields = ["field1", "field2"]
    
    # Which fields to exclude
    exclude = ["field3"]
    
    # Read-only fields
    readonly_fields = ["created_at", "updated_at"]
```

### Other Options

```python
class MyModelAdmin(admin.ModelAdmin):
    # Date drill-down
    date_hierarchy = "pub_date"
    
    # Filter by related field
    list_filter = ["category", "author__username"]
    
    # Inline related models
    inlines = [RelatedModelInline]
    
    # Custom actions
    actions = ["custom_action"]
    
    # Save buttons on top
    save_on_top = True
```

## Advanced: Inline Comments

Show comments when editing a post:

```python
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0  # Don't show empty forms
    readonly_fields = ["author", "content", "created_at"]
    can_delete = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # ... previous settings ...
    inlines = [CommentInline]
```

Now when editing a post, you see its comments at the bottom!

## Admin Best Practices

1. **Always use `list_display`**: Makes lists actually useful
2. **Add search and filters**: Essential for many records
3. **Use `raw_id_fields`**: For ForeignKeys with many options
4. **Prepopulate slugs**: Save time and reduce errors
5. **Create custom actions**: For bulk operations
6. **Use `readonly_fields`**: For auto-generated fields
7. **Organize with fieldsets**: Makes forms cleaner

## Troubleshooting

### Issue: "No module named blog.admin"
Make sure `blog` is in `INSTALLED_APPS` in settings.py

### Issue: Models not showing in admin
Make sure you registered them:
```python
admin.site.register(Model)
# or
@admin.register(Model)
```

### Issue: "Can't edit in list view"
Check both `list_display` and `list_editable` include the field

### Issue: Slug not auto-filling
Check `prepopulated_fields` spelling and syntax

### Issue: Search not working
Verify fields in `search_fields` exist in the model

## Testing Your Admin

Create some test data through the admin:

1. **Create 3 categories:**
   - Technology
   - Programming  
   - Web Development

2. **Create 5 posts:**
   - Assign to different categories
   - Mix of draft and published
   - Add featured images (optional)

3. **Add comments to posts:**
   - Approve some, leave others unapproved
   - Test bulk approve action

4. **Test admin features:**
   - ✅ Search for posts by title
   - ✅ Filter posts by status
   - ✅ Use date hierarchy
   - ✅ Edit comment approval in list view
   - ✅ Bulk approve comments

## Checklist

Before moving on, verify:

- ✅ All three models registered in admin
- ✅ List displays show useful columns
- ✅ Search and filters working
- ✅ Slug auto-population working
- ✅ Custom actions for comments working
- ✅ Can create categories, posts, and comments
- ✅ Post fieldsets organized
- ✅ List editing enabled for comments

## What You've Learned

- How to register models in admin
- Customizing list views with `list_display`
- Adding search and filters
- Auto-populating fields
- Creating custom admin actions
- Organizing forms with fieldsets
- Making fields editable in lists
- Using raw_id_fields for relationships

## Next Steps

Now that you can manage data through the admin, let's create views to display it on the website!

**→ Continue to [05 - Views and URLs](./05-views-and-urls.md)**

---

## Additional Resources

- [Django Admin Documentation](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)
- [Admin Actions](https://docs.djangoproject.com/en/stable/ref/contrib/admin/actions/)
- [ModelAdmin Options](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#modeladmin-options)
