# Tutorial 09: Styling dengan CSS

## Apa yang Bakal Lo Pelajari

- Setup static files di Django
- Organisir CSS
- Responsive design
- Framework CSS (optional)

## Static Files di Django

Static files = CSS, JavaScript, images yang ga berubah.

Di `settings.py` (sudah configured):

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Development only
STATICFILES_DIRS = [BASE_DIR / 'static']
```

**Structure:**
```
static/
  css/
    style.css
  js/
    script.js
  images/
    logo.png
```

**Load di template:**
```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

## Bikin Style.css

Create `static/css/style.css`:

```css
/* Reset & Base */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f4f4f4;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Navigation */
.navbar {
    background-color: #2c3e50;
    color: white;
    padding: 1rem 0;
}

.nav-brand a {
    color: white;
    text-decoration: none;
    font-size: 1.5rem;
    font-weight: bold;
}

.nav-menu {
    display: flex;
    gap: 1.5rem;
    align-items: center;
}

.nav-menu a {
    color: white;
    text-decoration: none;
    transition: color 0.3s;
}

.nav-menu a:hover {
    color: #3498db;
}

/* Post Cards */
.post-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.post-card h2 a {
    color: #2c3e50;
    text-decoration: none;
}

.post-card h2 a:hover {
    color: #3498db;
}

.post-meta {
    color: #7f8c8d;
    font-size: 0.9rem;
    margin: 0.5rem 0;
}

.read-more {
    color: #3498db;
    text-decoration: none;
    font-weight: bold;
}

/* Forms */
.form-control {
    width: 100%;
    padding: 0.5rem;
    margin-bottom: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
}

.btn {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    text-decoration: none;
    display: inline-block;
}

.btn-primary {
    background-color: #3498db;
    color: white;
}

.btn-primary:hover {
    background-color: #2980b9;
}

.btn-danger {
    background-color: #e74c3c;
    color: white;
}

/* Responsive */
@media (max-width: 768px) {
    .nav-menu {
        flex-direction: column;
    }
    
    .post-card {
        padding: 1rem;
    }
}
```

**Lo udah tau CSS!** Ini cuma styling basic Django templates.

## Tips CSS di Django

### 1. Organisir CSS by Component

```
static/css/
  base.css          # Layout, typography
  forms.css         # Form styling
  posts.css         # Post-specific
  responsive.css    # Media queries
```

Load multiple:
```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/base.css' %}">
<link rel="stylesheet" href="{% static 'css/forms.css' %}">
```

### 2. Use CSS Variables

```css
:root {
    --primary-color: #3498db;
    --secondary-color: #2c3e50;
    --text-color: #333;
    --bg-color: #f4f4f4;
}

.btn-primary {
    background-color: var(--primary-color);
}
```

### 3. Mobile-First Approach

```css
/* Mobile first */
.container {
    padding: 1rem;
}

/* Then desktop */
@media (min-width: 768px) {
    .container {
        padding: 2rem;
    }
}
```

## Framework CSS (Optional)

### Bootstrap
```django
{# Di base.html #}
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
```

### Tailwind CSS
Setup lebih complex, tapi powerful!

## Collectstatic (Production)

Sebelum deploy:

```bash
python manage.py collectstatic
```

Ini collect semua static files ke `STATIC_ROOT` buat production server.

## Kesimpulan

✅ Setup static files  
✅ Bikin custom CSS  
✅ Responsive design  
✅ Ready untuk production!

**Lo udah tau HTML/CSS!** Django cuma serve files-nya aja.

## Next Steps

**→ Continue to [10 - Testing & Deployment](./10-testing-deployment.md)**
