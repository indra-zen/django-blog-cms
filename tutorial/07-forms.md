# Tutorial 07: Forms

## What You'll Learn

- Django Forms framework
- Creating ModelForms
- Form validation
- Handling form data
- Custom form widgets and styling
- File upload handling

## Understanding Django Forms

Django Forms handle:
- **Rendering:** Convert Python to HTML
- **Validation:** Check data is correct
- **Cleaning:** Convert to Python types
- **Security:** CSRF protection, XSS prevention

**Without Forms:**
```html
<!-- Manual HTML, no validation -->
<input type="text" name="title">
```

**With Forms:**
```python
# Automatic HTML, validation, security
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
```

## Two Types of Forms

### Form (Base class)
```python
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
```
Define fields manually.

### ModelForm (From model)
```python
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
```
Fields automatically from model!

## Step 1: Create Forms File

Create `blog/forms.py`:

```python
from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Form for creating and editing blog posts"""

    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'excerpt', 'featured_image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your post content here...'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of your post (optional)'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class CommentForm(forms.ModelForm):
    """Form for adding comments to posts"""

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            }),
        }
        labels = {
            'content': 'Your Comment'
        }
```

### Understanding the Code

**Meta Class:**
```python
class Meta:
    model = Post
    fields = ['title', 'content']
```
- `model`: Which model to use
- `fields`: Which fields to include

**Widgets:**
```python
widgets = {
    'title': forms.TextInput(attrs={...})
}
```
- Controls HTML rendering
- `attrs`: HTML attributes (class, placeholder, etc.)

**Widget Types:**
- `TextInput`: `<input type="text">`
- `Textarea`: `<textarea>`
- `Select`: `<select>` dropdown
- `CheckboxInput`: `<input type="checkbox">`
- `FileInput`: `<input type="file">`
- `DateInput`: Date picker
- `EmailInput`: Email field

**Custom Labels:**
```python
labels = {
    'content': 'Your Comment'
}
```
Changes form label text.

## Step 2: Form Validation

Add custom validation to PostForm:

```python
class PostForm(forms.ModelForm):
    """Form for creating and editing blog posts"""

    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'excerpt', 'featured_image', 'status']
        widgets = {
            # ... (same as before)
        }
    
    def clean_title(self):
        """Validate title is not just whitespace"""
        title = self.cleaned_data.get('title')
        if title and not title.strip():
            raise forms.ValidationError('Title cannot be empty or just whitespace.')
        return title
    
    def clean_content(self):
        """Validate content has minimum length"""
        content = self.cleaned_data.get('content')
        if content and len(content) < 50:
            raise forms.ValidationError('Content must be at least 50 characters long.')
        return content
    
    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        content = cleaned_data.get('content')
        
        if status == 'published' and not content:
            raise forms.ValidationError('Cannot publish a post without content.')
        
        return cleaned_data
```

### Understanding Validation

**Field-level Validation:**
```python
def clean_FIELDNAME(self):
    value = self.cleaned_data.get('fieldname')
    # Validate
    if not valid:
        raise forms.ValidationError('Error message')
    return value  # Must return!
```

**Form-level Validation:**
```python
def clean(self):
    cleaned_data = super().clean()
    # Cross-field validation
    return cleaned_data
```

**When Validation Runs:**
```python
form = PostForm(request.POST)
if form.is_valid():  # Validation happens here!
    form.save()
```

## Step 3: Using Forms in Views

We already created views, but let's understand how they work with forms:

### Create View

```python
def create_post(request):
    if request.method == 'POST':
        # Submitted form
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        # Empty form
        form = PostForm()
    
    return render(request, 'blog/create_post.html', {'form': form})
```

**Key Points:**
- `request.POST`: Form data
- `request.FILES`: Uploaded files
- `form.is_valid()`: Triggers validation
- `commit=False`: Don't save yet (set relationships first)

### Edit View

```python
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)  # Pre-fill!
    
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})
```

**Key difference:** `instance=post` pre-fills form with existing data.

## Step 4: Displaying Forms in Templates

### Method 1: as_p (Paragraphs)

```django
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>
```

Renders:
```html
<p>
    <label for="id_title">Title:</label>
    <input type="text" name="title" id="id_title">
</p>
```

### Method 2: as_table

```django
<form method="post">
    {% csrf_token %}
    <table>
        {{ form.as_table }}
    </table>
    <button type="submit">Submit</button>
</form>
```

### Method 3: as_ul

```django
<form method="post">
    {% csrf_token %}
    <ul>
        {{ form.as_ul }}
    </ul>
    <button type="submit">Submit</button>
</form>
```

### Method 4: Manual (Most Control)

```django
<form method="post">
    {% csrf_token %}
    
    <div class="form-group">
        <label for="{{ form.title.id_for_label }}">Title:</label>
        {{ form.title }}
        {% if form.title.errors %}
            <div class="error">{{ form.title.errors }}</div>
        {% endif %}
    </div>
    
    <div class="form-group">
        <label for="{{ form.content.id_for_label }}">Content:</label>
        {{ form.content }}
        {% if form.content.errors %}
            <div class="error">{{ form.content.errors }}</div>
        {% endif %}
    </div>
    
    <button type="submit">Submit</button>
</form>
```

### Displaying Errors

**All Errors:**
```django
{% if form.errors %}
    <div class="errors">
        {{ form.errors }}
    </div>
{% endif %}
```

**Per Field:**
```django
{% if form.title.errors %}
    <div class="error">
        {{ form.title.errors }}
    </div>
{% endif %}
```

**Non-field Errors:**
```django
{% if form.non_field_errors %}
    <div class="error">
        {{ form.non_field_errors }}
    </div>
{% endif %}
```

## Step 5: Form Field Reference

```python
# Text fields
forms.CharField()                  # Text input
forms.TextField()                  # Textarea
forms.EmailField()                 # Email input
forms.URLField()                   # URL input
forms.SlugField()                  # Slug field

# Numeric fields
forms.IntegerField()               # Integer
forms.FloatField()                 # Float
forms.DecimalField()               # Decimal

# Choice fields
forms.BooleanField()               # Checkbox
forms.ChoiceField(choices=...)     # Dropdown
forms.MultipleChoiceField()        # Multi-select

# Date/Time fields
forms.DateField()                  # Date
forms.TimeField()                  # Time
forms.DateTimeField()              # Date & Time

# File fields
forms.FileField()                  # File upload
forms.ImageField()                 # Image upload

# Other
forms.RegexField(regex=...)        # Regex validation
forms.JSONField()                  # JSON data
```

## Step 6: Field Arguments

```python
forms.CharField(
    max_length=100,           # Max characters
    min_length=3,             # Min characters
    required=True,            # Required field?
    initial='Default',        # Default value
    label='Custom Label',     # Form label
    help_text='Help text',    # Help text
    error_messages={          # Custom errors
        'required': 'This field is required!',
        'max_length': 'Too long!'
    },
    widget=forms.TextInput(   # Widget type
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter text'
        }
    ),
    validators=[...]          # Custom validators
)
```

## Step 7: Custom Validators

Create reusable validators:

```python
from django.core.exceptions import ValidationError

def validate_no_profanity(value):
    """Check for profanity"""
    bad_words = ['badword1', 'badword2']
    for word in bad_words:
        if word in value.lower():
            raise ValidationError(f'Please avoid using inappropriate language.')

class PostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        validators=[validate_no_profanity]
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content']
```

## Step 8: Advanced: Dynamic Forms

Forms that change based on user:

```python
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'status']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Only staff can publish immediately
        if user and not user.is_staff:
            self.fields['status'].choices = [
                ('draft', 'Draft'),
            ]

# In view
form = PostForm(request.POST, user=request.user)
```

## Step 9: Form Sets (Multiple Forms)

For editing multiple objects:

```python
from django.forms import modelformset_factory

# Create formset
PostFormSet = modelformset_factory(Post, fields=['title', 'status'], extra=2)

# In view
if request.method == 'POST':
    formset = PostFormSet(request.POST)
    if formset.is_valid():
        formset.save()
else:
    formset = PostFormSet()

# In template
<form method="post">
    {% csrf_token %}
    {{ formset.management_form }}
    {% for form in formset %}
        {{ form.as_p }}
    {% endfor %}
    <button type="submit">Save All</button>
</form>
```

## Best Practices

1. **Always use ModelForms** when working with models
2. **Add validation** for business logic
3. **Use widgets** to customize HTML
4. **Handle file uploads** with `request.FILES`
5. **Use `commit=False`** when setting relationships
6. **Display errors** to help users
7. **Test validation** thoroughly

## Common Patterns

### Pattern: Form with Success Message

```python
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'create.html', {'form': form})
```

### Pattern: Form with Initial Data

```python
form = PostForm(initial={
    'status': 'draft',
    'category': default_category,
})
```

### Pattern: Exclude Fields

```python
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'slug', 'created_at']
```

## Troubleshooting

### Issue: Form not validating
```python
form = PostForm(request.POST)
if not form.is_valid():
    print(form.errors)  # Debug!
```

### Issue: File upload not working
- Include `enctype="multipart/form-data"` in `<form>`
- Pass `request.FILES` to form

### Issue: "Field is required" but it shouldn't be
```python
class Meta:
    model = Post
    fields = ['title']
    # In model:
    # title = models.CharField(blank=True)  # Add blank=True
```

### Issue: Custom validation not running
- Method name must be `clean_FIELDNAME`
- Must return cleaned value
- Must call `form.is_valid()` in view

## Testing Forms

```python
from blog.forms import PostForm
from blog.models import Category

# Test valid form
data = {
    'title': 'Test Post',
    'content': 'A' * 100,  # 100 characters
    'status': 'draft'
}
form = PostForm(data)
assert form.is_valid()

# Test invalid form
data = {'title': ''}
form = PostForm(data)
assert not form.is_valid()
assert 'title' in form.errors
```

## Checklist

Before moving on, verify:

- ✅ PostForm created with all fields
- ✅ CommentForm created
- ✅ Custom validation working
- ✅ Widgets styling forms
- ✅ Forms validated in views
- ✅ Errors displaying in templates
- ✅ File uploads working
- ✅ Can create and edit posts

## What You've Learned

- Django Forms vs ModelForms
- Creating forms from models
- Form fields and widgets
- Validation (field-level and form-level)
- Handling forms in views
- Displaying forms in templates
- Custom validators
- File upload handling

## Next Steps

Forms are complete! Now let's add user authentication.

**→ Continue to [08 - Authentication](./08-authentication.md)**

---

## Additional Resources

- [Django Forms Documentation](https://docs.djangoproject.com/en/stable/topics/forms/)
- [ModelForm Reference](https://docs.djangoproject.com/en/stable/topics/forms/modelforms/)
- [Form Validation](https://docs.djangoproject.com/en/stable/ref/forms/validation/)
