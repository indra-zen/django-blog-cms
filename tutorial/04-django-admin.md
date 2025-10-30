# Tutorial 04: Django Admin Panel

## Apa yang Bakal Lo Pelajari

- Register models di Django admin
- Customisasi interface admin
- Tambahin search dan filtering
- Bikin custom admin actions
- Organisir layout admin

## Kenapa Pake Django Admin?

Django admin itu interface yang powerful dan production-ready buat manage data lo. Kayak punya CMS (Content Management System) lengkap dengan **ZERO CODE**!

**Tanpa admin:** Lo harus bikin forms, views, templates manual buat CRUD operations. Ribet!

**Dengan admin:** Lo dapet semuanya **OTOMATIS**! 🎉

### Analogi

Bayangin lo bikin toko online:
- **Tanpa admin:** Harus bikin halaman buat add product, edit product, delete product, dll (banyak coding!)
- **Dengan admin:** Django udah siapin semua interface-nya. Tinggal pake!

## Step 1: Register Models Dasar

Buka `blog/admin.py` dan ganti isinya:

```python
from django.contrib import admin
from .models import Category, Post, Comment

# Simple registration
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
```

### Test

1. Jalanin server: `python manage.py runserver`
2. Buka: `http://127.0.0.1:8000/admin/`
3. Login pake superuser lo
4. Lo bakal liat 3 model lo ada di sini!

**Coba:**
- Klik "Categories" → "Add Category"
- Isi name dan description
- Klik "Save"
- Notice slug-nya auto-generate!

**Keren kan?** Lo udah punya interface buat manage Category tanpa nulis HTML/CSS sama sekali!

## Step 2: Customisasi Category Admin

Mari kita bikin admin lebih powerful. Ganti registration sederhana tadi:

```python
from django.contrib import admin
from .models import Category, Post, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "description"]
    list_per_page = 20
```

### Penjelasan Code

**`@admin.register(Category)`**
- Python decorator buat register model
- Alternative dari `admin.site.register()`
- Lebih clean dan modern

**`list_display`**
```python
list_display = ["name", "slug", "created_at"]
```
Tampilkan kolom-kolom ini di list view.

**Sebelum:**
```
Category object (1)
Category object (2)
```

**Sesudah:**
```
Name         | Slug        | Created At
Technology   | technology  | Oct 30, 2025
Programming  | programming | Oct 30, 2025
```

**`prepopulated_fields`**
```python
prepopulated_fields = {"slug": ("name",)}
```
Auto-fill slug dari name saat lo ngetik di form.

Contoh: Ketik "Web Development" → slug otomatis jadi "web-development"

**`search_fields`**
```python
search_fields = ["name", "description"]
```
Tambahin search box buat cari categories by name atau description.

### Test

Refresh admin page:
- ✅ Lo sekarang liat tabel rapi dengan kolom name, slug, date
- ✅ Klik "Add Category" - ketik name dan liat slug auto-fill!
- ✅ Coba search box - cari category by name

## Step 3: Customisasi Post Admin

Posts butuh customisasi lebih banyak karena lebih complex:

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "status", "published_at", "created_at"]
    list_filter = ["status", "category", "created_at", "published_at"]
    search_fields = ["title", "content", "excerpt"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ["-published_at", "-created_at"]
    raw_id_fields = ["author"]
    list_per_page = 25
    
    fieldsets = (
        ("Informasi Post", {
            "fields": ("title", "slug", "author", "category")
        }),
        ("Konten", {
            "fields": ("content", "excerpt", "featured_image")
        }),
        ("Publikasi", {
            "fields": ("status", "published_at")
        }),
    )
```

### Penjelasan Options Baru

**`list_filter`**
```python
list_filter = ["status", "category", "created_at", "published_at"]
```
Tambahin filter sidebar di kanan:
- Filter by status (draft/published)
- Filter by category
- Filter by tanggal

**Analogi:** Kayak filter di e-commerce (filter by price, brand, category, dll)

**`date_hierarchy`**
```python
date_hierarchy = "published_at"
```
Tambahin navigasi date drill-down di atas:
```
2025 → October → Day 30
```

**`ordering`**
```python
ordering = ["-published_at", "-created_at"]
```
Urutan default. Tanda `-` = descending (terbaru dulu).

**`raw_id_fields`**
```python
raw_id_fields = ["author"]
```
Instead of dropdown dengan semua users (bisa jadi ribuan!), pake popup yang searchable.

**Kenapa?** Kalo lo punya 10,000 users, dropdown bakal lambat banget. Popup lebih efficient!

**`fieldsets`**
```python
fieldsets = (
    ("Informasi Post", {
        "fields": ("title", "slug", "author", "category")
    }),
    ("Konten", {
        "fields": ("content", "excerpt", "featured_image")
    }),
    ("Publikasi", {
        "fields": ("status", "published_at")
    }),
)
```

Organisir form fields ke dalam sections dengan headers.

**Sebelum:** Semua field dicampur jadi satu.

**Sesudah:** Fields dikelompokkin logically:
```
┌─ Informasi Post ────────┐
│ Title: [__________]     │
│ Slug: [__________]      │
│ Author: [________]      │
│ Category: [_______]     │
└─────────────────────────┘

┌─ Konten ────────────────┐
│ Content: [___________]  │
│ Excerpt: [___________]  │
│ Image: [Browse...]      │
└─────────────────────────┘

┌─ Publikasi ─────────────┐
│ Status: [Published ▼]   │
│ Published: [Date...]    │
└─────────────────────────┘
```

Lebih rapi dan user-friendly!

## Step 4: Customisasi Comment Admin

```python
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["get_comment_preview", "author", "post", "is_approved", "created_at"]
    list_filter = ["is_approved", "created_at"]
    search_fields = ["content", "author__username", "post__title"]
    actions = ["approve_comments", "unapprove_comments"]
    date_hierarchy = "created_at"
    
    def get_comment_preview(self, obj):
        """Show preview dari comment content"""
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    get_comment_preview.short_description = "Comment"
    
    def approve_comments(self, request, queryset):
        """Bulk approve comments"""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} comment(s) approved.")
    approve_comments.short_description = "Approve selected comments"
    
    def unapprove_comments(self, request, queryset):
        """Bulk unapprove comments"""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f"{updated} comment(s) unapproved.")
    unapprove_comments.short_description = "Unapprove selected comments"
```

### Fitur Baru: Custom Methods & Actions

**Custom display method:**
```python
def get_comment_preview(self, obj):
    return obj.content[:50] + "..."
get_comment_preview.short_description = "Comment"
```
Bikin kolom custom di list view. Instead of showing full comment (panjang!), cuma show 50 karakter pertama.

**Custom admin actions:**
```python
actions = ["approve_comments", "unapprove_comments"]

def approve_comments(self, request, queryset):
    updated = queryset.update(is_approved=True)
    self.message_user(request, f"{updated} comment(s) approved.")
```

Tambahin actions di dropdown buat bulk operations:
1. Select multiple comments
2. Choose action: "Approve selected comments"
3. Click "Go"
4. All selected comments approved! ��

**Analogi:** Kayak select multiple emails di Gmail terus pilih "Mark as read" atau "Delete".

**`search_fields` dengan relationships:**
```python
search_fields = ["content", "author__username", "post__title"]
```

Double underscore (`__`) buat traverse relationships:
- `author__username` - Cari by username dari related User
- `post__title` - Cari by title dari related Post

## Step 5: Inline Editing (Advanced!)

Inline editing = Edit related objects tanpa pindah page.

Contoh: Edit comments langsung dari Post detail page.

Update `PostAdmin`:

```python
from django.contrib import admin
from .models import Category, Post, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ["author", "content", "created_at"]
    can_delete = True

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "status", "published_at", "created_at"]
    list_filter = ["status", "category", "created_at", "published_at"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ["-published_at", "-created_at"]
    raw_id_fields = ["author"]
    
    inlines = [CommentInline]
    
    fieldsets = (
        ("Informasi Post", {
            "fields": ("title", "slug", "author", "category")
        }),
        ("Konten", {
            "fields": ("content", "excerpt", "featured_image")
        }),
        ("Publikasi", {
            "fields": ("status", "published_at")
        }),
    )
```

### Penjelasan Inline

**`TabularInline`** - Tampilan table (row per row)
**`StackedInline`** - Tampilan stacked (vertical)

**`extra = 0`** - Berapa blank form ditampilkan buat add new comment

**`readonly_fields`** - Field yang ga bisa diedit

Sekarang pas lo edit Post, lo bisa:
- Liat semua comments di post itu
- Approve/unapprove comments
- Edit comment content
- Delete comments
- All in one page! 🔥

## Step 6: Customisasi Admin Site

Personalisasi admin site header dan title.

Di `blog/admin.py`, tambahin di bawah:

```python
# Customisasi admin site
admin.site.site_header = "Blog CMS Admin"
admin.site.site_title = "Blog Admin Portal"
admin.site.index_title = "Welcome to Blog Admin"
```

Refresh admin - sekarang header-nya branded! 🎨

## Kesimpulan

Lo udah belajar:

✅ Register models di admin
✅ Customisasi list display
✅ Tambahin search & filters
✅ Organisir forms dengan fieldsets
✅ Bikin custom admin actions
✅ Inline editing
✅ Personalisasi admin site

### Admin Panel Sekarang Punya:

- 📊 **List view** yang informative dengan banyak kolom
- 🔍 **Search box** buat cari data
- 🎚️ **Filters** buat narrow down results
- 📅 **Date hierarchy** buat navigasi by date
- ⚡ **Bulk actions** buat approve/delete banyak items sekaligus
- 📝 **Inline editing** buat edit related objects
- 🎨 **Custom branding**

**All without writing a single line of HTML/CSS!** 🎉

## Tips & Best Practices

### 1. Always Use list_display

```python
# ❌ BAD - User ga tau apa isi objectnya
list_display = ["__str__"]

# ✅ GOOD - Clear dan informative
list_display = ["title", "author", "status", "created_at"]
```

### 2. Add Search untuk User Experience

```python
search_fields = ["title", "content", "author__username"]
```

### 3. Use Filters buat Data Banyak

```python
list_filter = ["status", "category", "created_at"]
```

### 4. Readonly Fields buat Data yang Ga Boleh Diubah

```python
readonly_fields = ["created_at", "updated_at", "slug"]
```

### 5. Prepopulated Fields buat Slug

```python
prepopulated_fields = {"slug": ("title",)}
```

## Next Steps

Di [Chapter 5](./05-views-urls.md), lo bakal belajar:

- Bikin views buat display posts
- URL routing
- Template rendering
- Context data

Ready? Let's build the frontend! 🚀

## Troubleshooting

### Admin panel ga muncul
**Solusi:** Pastiin `django.contrib.admin` ada di `INSTALLED_APPS`

### Model ga muncul di admin
**Solusi:**
- Check lo udah register di `admin.py`
- Restart Django server

### Error saat save
**Solusi:** Check validasi di model (required fields, unique constraints)

### Slug ga auto-generate
**Solusi:** Pastiin `prepopulated_fields` spelling-nya bener dan field exist di model
