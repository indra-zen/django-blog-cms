# Tutorial 07: Forms

## Apa yang Bakal Lo Pelajari

- Django Forms framework
- Bikin ModelForms dari model
- Form validation
- Handle form data & file uploads
- Custom widgets dan styling

## Apa Itu Django Forms?

Django Forms handle:

- **Rendering:** Convert Python to HTML
- **Validation:** Check data correct
- **Cleaning:** Convert to Python types
- **Security:** CSRF protection, XSS prevention

### Analogi JavaScript

**Tanpa Forms (Manual):**
```html
<!-- Ribet, ga ada validation -->
<input type="text" name="title">
<input type="text" name="content">
```

**Dengan Django Forms:**
```python
# Automatic HTML, validation, security!
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
```

Kayak pake library form di React (Formik, React Hook Form), tapi built-in!

## Dua Tipe Forms

### 1. Form (Base Class)

```python
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
```
Define fields manual. Buat forms yang ga related ke model.

### 2. ModelForm (From Model)

```python
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
```
Fields auto from model! **Use this buat CRUD operations.**

## Step 1: Bikin Forms File

Create `blog/forms.py`:

```python
from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    """Form buat create dan edit blog posts"""
    
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
                'rows': 10
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Short summary...'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

class CommentForm(forms.ModelForm):
    """Form buat add comments ke posts"""
    
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

### Penjelasan Code

**Meta Class:**
```python
class Meta:
    model = Post
    fields = ['title', 'content']
```

**Widgets:**
```python
widgets = {
    'title': forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter post title'
    }),
}
```
Controls HTML rendering. `attrs` = HTML attributes (class, placeholder, dll).

**Widget Types:**
- `TextInput` → `<input type="text">`
- `Textarea` → `<textarea>`
- `Select` → `<select>` dropdown
- `CheckboxInput` → `<input type="checkbox">`
- `FileInput` → `<input type="file">`
- `DateInput` → Date picker
- `EmailInput` → Email field

**Custom Labels:**
```python
labels = {
    'content': 'Your Comment'
}
```

## Step 2: Form Validation

Tambahin custom validation ke PostForm:

```python
class PostForm(forms.ModelForm):
    """Form buat create dan edit blog posts"""
    
    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'excerpt', 'featured_image', 'status']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10
            }),
        }
    
    def clean_title(self):
        """Validate title bukan cuma whitespace"""
        title = self.cleaned_data.get('title')
        if title and not title.strip():
            raise forms.ValidationError('Title cannot be empty or just whitespace.')
        return title
    
    def clean_content(self):
        """Validate content ada minimum length"""
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

### Penjelasan Validation

**Field-level Validation:**
```python
def clean_FIELDNAME(self):
    value = self.cleaned_data.get('fieldname')
    if not valid:
        raise forms.ValidationError('Error message')
    return value
```
Pattern: `clean_` + field name

**Form-level Validation:**
```python
def clean(self):
    cleaned_data = super().clean()
    return cleaned_data
```

**Kapan Validation Run:**
```python
form = PostForm(request.POST)
if form.is_valid():
    form.save()
```

## Step 3: Pake Forms di Views

Kita udah bikin views di Chapter 5, tapi mari kita pahami gimana works:

### Create View

```python
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'blog/create_post.html', {'form': form})
```

**Key Points:**
- `request.POST` - Form data
- `request.FILES` - Uploaded files (WAJIB buat file uploads!)
- `form.is_valid()` - Triggers validation
- `commit=False` - Don't save yet (set relationships first)

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
        form = PostForm(instance=post)
    
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})
```

**Key difference:** `instance=post` pre-fills form!

## Step 4: Display Forms di Templates

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

### Display Errors

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
forms.CharField()
forms.TextField()
forms.EmailField()
forms.URLField()
forms.SlugField()

# Numeric fields
forms.IntegerField()
forms.FloatField()
forms.DecimalField()

# Choice fields
forms.BooleanField()
forms.ChoiceField(choices=...)
forms.MultipleChoiceField()

# Date/Time fields
forms.DateField()
forms.TimeField()
forms.DateTimeField()

# File fields
forms.FileField()
forms.ImageField()

# Other
forms.RegexField(regex=...)
forms.JSONField()
```

## Step 6: Field Arguments

```python
forms.CharField(
    max_length=200,
    min_length=5,
    required=True,
    initial='Default',
    label='Post Title',
    help_text='Enter title',
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Title...'
    }),
    error_messages={
        'required': 'Please enter a title!',
        'max_length': 'Too long!'
    },
    validators=[...]
)
```

## Step 7: Custom Validators

Bikin reusable validators:

```python
from django.core.exceptions import ValidationError

def validate_no_profanity(value):
    bad_words = ['spam', 'badword']
    for word in bad_words:
        if word.lower() in value.lower():
            raise ValidationError('Please avoid using inappropriate language.')

class PostForm(forms.ModelForm):
    title = forms.CharField(
        validators=[validate_no_profanity]
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content']
```

## Step 8: Advanced - Dynamic Forms

Forms yang berubah based on user:

```python
class PostForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if user and not user.is_staff:
            self.fields['status'].choices = [
                ('draft', 'Draft'),
            ]

# In view
form = PostForm(request.POST, user=request.user)
```

**Keren!** Form beda tergantung user role!

## Step 9: Form Sets (Multiple Forms)

Buat edit multiple objects sekaligus:

```python
from django.forms import modelformset_factory

PostFormSet = modelformset_factory(
    Post,
    fields=['title', 'status'],
    extra=2
)

if request.method == 'POST':
    formset = PostFormSet(request.POST)
    if formset.is_valid():
        formset.save()
else:
    formset = PostFormSet()
```

## Best Practices

### 1. Always Use ModelForms

```python
# ✅ GOOD
class PostForm(forms.ModelForm):
    pass

# ❌ BAD
class PostForm(forms.Form):
    title = forms.CharField(max_length=200)
```

### 2. Add Validation untuk Business Logic

```python
def clean_content(self):
    content = self.cleaned_data.get('content')
    if content and len(content) < 50:
        raise forms.ValidationError('Content too short!')
    return content
```

### 3. Use Widgets buat Customize HTML

```python
widgets = {
    'content': forms.Textarea(attrs={'rows': 10})
}
```

### 4. Handle File Uploads

```python
form = PostForm(request.POST, request.FILES)
```

### 5. Use commit=False

```python
post = form.save(commit=False)
post.author = request.user
post.save()
```

### 6. Display Errors

```django
{% if form.errors %}
    <div class="errors">{{ form.errors }}</div>
{% endif %}
```

## Troubleshooting

### Form Ga Validate

```python
form = PostForm(request.POST)
if not form.is_valid():
    print(form.errors)
```

### File Upload Ga Work

```django
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
</form>
```

```python
form = PostForm(request.POST, request.FILES)
```

### "Field is required" tapi Shouldn't Be

```python
class Post(models.Model):
    excerpt = models.TextField(blank=True)
```

## Kesimpulan

Lo udah belajar:

✅ Django Forms vs ModelForms
✅ Bikin forms dari models
✅ Form fields dan widgets
✅ Validation (field-level dan form-level)
✅ Handle forms di views
✅ Display forms di templates
✅ Custom validators
✅ File upload handling

**Django Forms powerful!** Automatic validation, security, dan HTML generation. Ga perlu setup library kayak Formik!

## Next Steps

Forms selesai! Sekarang tambahin user authentication.

**→ Continue to [08 - Authentication](./08-authentication.md)**

## Additional Resources

- [Django Forms Documentation](https://docs.djangoproject.com/en/stable/topics/forms/)
- [ModelForm Reference](https://docs.djangoproject.com/en/stable/topics/forms/modelforms/)
- [Form Validation](https://docs.djangoproject.com/en/stable/ref/forms/validation/)
