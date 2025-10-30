# Tutorial 09: Styling with CSS

## What You'll Learn

- CSS fundamentals for Django apps
- Organizing static files
- Responsive design
- Mobile-first approach
- Flexbox and Grid
- Common UI patterns

## Understanding Static Files

Django serves static files (CSS, JavaScript, images) differently than templates.

### Static Files Structure

```
blog/
├── static/
│   └── blog/
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   └── main.js
│       └── images/
│           └── logo.png
```

**Why nested?** `blog/static/blog/` prevents name conflicts when multiple apps have static files.

### In Settings

```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Additional static directories
STATIC_ROOT = BASE_DIR / 'staticfiles'     # For production (collectstatic)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'            # User uploads
```

### Using Static Files in Templates

```django
{% load static %}

<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{% static 'blog/css/style.css' %}">
</head>
<body>
    <img src="{% static 'blog/images/logo.png' %}" alt="Logo">
    <script src="{% static 'blog/js/main.js' %}"></script>
</body>
</html>
```

**Key:** `{% load static %}` must be at the top!

## Our CSS File Structure

Let's understand our `static/css/style.css`:

### 1. CSS Reset and Base Styles

```css
/* Reset default browser styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f5f5;
}
```

**Why?**
- `box-sizing: border-box`: Width includes padding/border
- System fonts: Fast, native appearance
- `line-height: 1.6`: Readable text spacing

### 2. Container and Layout

```css
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}
```

**Pattern:** Centered, responsive container
- `max-width`: Limits width on large screens
- `margin: 0 auto`: Centers horizontally
- `padding: 0 20px`: Breathing room on small screens

### 3. Header and Navigation

```css
header {
    background-color: #2c3e50;
    color: white;
    padding: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
}

nav a {
    color: white;
    text-decoration: none;
    padding: 0.5rem 1rem;
    transition: background-color 0.3s;
}

nav a:hover {
    background-color: #34495e;
    border-radius: 4px;
}
```

**Flexbox Layout:**
- `display: flex`: Enables flexbox
- `justify-content: space-between`: Spreads items
- `align-items: center`: Vertical centering
- `flex-wrap: wrap`: Wraps on small screens

**Transitions:**
```css
transition: background-color 0.3s;
```
Smooth hover effect over 0.3 seconds.

### 4. Card Layout

```css
.post-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: transform 0.3s, box-shadow 0.3s;
}

.post-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}
```

**Card Pattern:**
- `border-radius`: Rounded corners
- `box-shadow`: Subtle depth
- `transform: translateY()`: Lift on hover

### 5. Grid Layout

```css
.post-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
}
```

**CSS Grid:**
- `repeat(auto-fill, ...)`: Dynamic columns
- `minmax(300px, 1fr)`: Min 300px, max equal width
- `gap`: Spacing between items

### 6. Forms

```css
.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #2c3e50;
}

.form-control {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
    transition: border-color 0.3s;
}

.form-control:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}
```

**Form Styling:**
- `display: block`: Label above input
- `:focus`: Custom focus state
- `outline: none`: Remove default, add custom

### 7. Buttons

```css
.btn {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.3s;
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

.btn-danger:hover {
    background-color: #c0392b;
}
```

**Button Pattern:**
- Base `.btn` class
- Modifier classes (`.btn-primary`, `.btn-danger`)
- Consistent spacing and transitions

### 8. Responsive Design

```css
/* Mobile First */
@media (max-width: 768px) {
    nav {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .post-grid {
        grid-template-columns: 1fr;
    }
    
    .container {
        padding: 0 10px;
    }
}

/* Tablet */
@media (min-width: 769px) and (max-width: 1024px) {
    .post-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* Desktop */
@media (min-width: 1025px) {
    .post-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}
```

**Media Queries:**
- Mobile: `max-width: 768px` (1 column)
- Tablet: `769px - 1024px` (2 columns)
- Desktop: `1025px+` (3 columns)

## CSS Best Practices

### 1. Use CSS Variables

```css
:root {
    --primary-color: #3498db;
    --secondary-color: #2c3e50;
    --danger-color: #e74c3c;
    --success-color: #27ae60;
    --border-radius: 4px;
    --box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.btn-primary {
    background-color: var(--primary-color);
    border-radius: var(--border-radius);
}
```

**Benefits:**
- Single source of truth
- Easy theme changes
- Consistent values

### 2. BEM Naming Convention

```css
/* Block */
.post-card {}

/* Element */
.post-card__title {}
.post-card__content {}
.post-card__author {}

/* Modifier */
.post-card--featured {}
.post-card--draft {}
```

**Pattern:** `block__element--modifier`

### 3. Mobile-First Approach

```css
/* Mobile default */
.container {
    padding: 0 10px;
}

/* Desktop enhancement */
@media (min-width: 768px) {
    .container {
        padding: 0 20px;
    }
}
```

**Why?** Easier to enhance than to remove.

### 4. Utility Classes

```css
/* Spacing */
.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }

/* Text */
.text-center { text-align: center; }
.text-muted { color: #6c757d; }

/* Display */
.d-none { display: none; }
.d-block { display: block; }
.d-flex { display: flex; }
```

Use in HTML:
```html
<div class="post-card mt-2 mb-2">
    <h2 class="text-center">Title</h2>
</div>
```

## Flexbox Patterns

### Pattern 1: Centered Content

```css
.center {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}
```

### Pattern 2: Space Between

```css
.navbar {
    display: flex;
    justify-content: space-between;
}
```

### Pattern 3: Column Layout

```css
.sidebar-layout {
    display: flex;
    gap: 2rem;
}

.sidebar {
    flex: 0 0 250px;  /* Don't grow, don't shrink, 250px */
}

.content {
    flex: 1;  /* Take remaining space */
}
```

### Pattern 4: Responsive Wrap

```css
.card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
}

.card {
    flex: 1 1 300px;  /* Grow, shrink, min 300px */
}
```

## Grid Patterns

### Pattern 1: Auto-Fit Grid

```css
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}
```

### Pattern 2: Fixed Columns

```css
.three-column {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 1rem;
}
```

### Pattern 3: Sidebar Layout

```css
.layout {
    display: grid;
    grid-template-columns: 250px 1fr;
    gap: 2rem;
}
```

### Pattern 4: Complex Layout

```css
.layout {
    display: grid;
    grid-template-areas:
        "header header header"
        "sidebar content content"
        "footer footer footer";
    grid-template-columns: 200px 1fr 1fr;
    gap: 1rem;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.content { grid-area: content; }
.footer { grid-area: footer; }
```

## Common UI Components

### 1. Alert Messages

```css
.alert {
    padding: 1rem;
    border-radius: 4px;
    margin-bottom: 1rem;
}

.alert-success {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
}

.alert-danger {
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    color: #721c24;
}
```

### 2. Badges

```css
.badge {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    font-size: 0.75rem;
    border-radius: 4px;
    font-weight: 600;
}

.badge-primary {
    background-color: #3498db;
    color: white;
}

.badge-success {
    background-color: #27ae60;
    color: white;
}
```

### 3. Pagination

```css
.pagination {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
    margin: 2rem 0;
}

.pagination a,
.pagination .current {
    padding: 0.5rem 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    text-decoration: none;
    color: #333;
}

.pagination .current {
    background-color: #3498db;
    color: white;
    border-color: #3498db;
}

.pagination a:hover {
    background-color: #f5f5f5;
}
```

### 4. Card with Image

```css
.image-card {
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.image-card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
}

.image-card-body {
    padding: 1.5rem;
}
```

## Animation Examples

### 1. Fade In

```css
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.post-card {
    animation: fadeIn 0.5s ease-out;
}
```

### 2. Pulse

```css
@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.05);
    }
}

.btn:active {
    animation: pulse 0.3s;
}
```

### 3. Slide In

```css
@keyframes slideIn {
    from {
        transform: translateX(-100%);
    }
    to {
        transform: translateX(0);
    }
}

.sidebar {
    animation: slideIn 0.3s ease-out;
}
```

## Accessibility in CSS

### 1. Focus Styles

```css
a:focus,
button:focus,
input:focus {
    outline: 2px solid #3498db;
    outline-offset: 2px;
}
```

### 2. Contrast Ratios

```css
/* Good contrast */
.text {
    color: #333;           /* Dark on light */
    background: white;
}

/* Bad contrast */
.text-bad {
    color: #ccc;           /* Too light */
    background: white;
}
```

Use tools: [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

### 3. Hidden but Accessible

```css
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    border: 0;
}
```

Use for screen readers:
```html
<button>
    <span class="sr-only">Close menu</span>
    <span aria-hidden="true">×</span>
</button>
```

## Dark Mode

```css
:root {
    --bg-color: white;
    --text-color: #333;
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg-color: #1a1a1a;
        --text-color: #f5f5f5;
    }
}

body {
    background-color: var(--bg-color);
    color: var(--text-color);
}
```

## Performance Tips

### 1. Minimize Repaints

```css
/* Bad: Causes reflow */
.element {
    width: 100px;
    margin-left: 10px;
}

/* Good: Uses transform */
.element {
    transform: translateX(10px);
}
```

### 2. Use CSS Instead of Images

```css
/* CSS triangle */
.triangle {
    width: 0;
    height: 0;
    border-left: 50px solid transparent;
    border-right: 50px solid transparent;
    border-bottom: 100px solid #3498db;
}

/* CSS circle */
.circle {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background-color: #3498db;
}
```

### 3. Will-Change

```css
.animated {
    will-change: transform;
}
```

Tells browser to optimize, but use sparingly!

## Debugging CSS

### 1. Border Trick

```css
* {
    border: 1px solid red;  /* See all boxes */
}
```

### 2. Background Colors

```css
.container {
    background-color: lightblue;
}
.sidebar {
    background-color: lightgreen;
}
.content {
    background-color: lightyellow;
}
```

### 3. Browser DevTools

- Right-click → Inspect
- See computed styles
- Test changes live
- View box model

## Production Checklist

Before deploying:

1. **Minify CSS**
   ```bash
   # Use tools like cssnano
   npm install cssnano
   ```

2. **Remove unused CSS**
   ```bash
   # Use PurgeCSS
   npm install purgecss
   ```

3. **Optimize images**
   - Compress with tools
   - Use appropriate formats (WebP)

4. **Add vendor prefixes**
   ```bash
   # Use Autoprefixer
   npm install autoprefixer
   ```

5. **Check browser support**
   - [Can I Use](https://caniuse.com/)

## Troubleshooting

### Issue: Styles not applying

**Check:**
1. `{% load static %}` in template?
2. File path correct?
3. Clear browser cache (Ctrl+Shift+R)
4. Check browser console for 404

### Issue: Layout breaking on mobile

**Check:**
1. Viewport meta tag:
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   ```
2. Media queries
3. `max-width` instead of `width`

### Issue: Flexbox not working

**Check:**
1. Parent has `display: flex`?
2. Check `flex-direction`
3. Use DevTools to debug

### Issue: Z-index not working

**Needs:**
- `position: relative/absolute/fixed`
- Higher z-index than competitors

## Checklist

Before moving on, verify:

- ✅ CSS file created and linked
- ✅ Static files configured
- ✅ Responsive design working
- ✅ Forms styled
- ✅ Buttons styled
- ✅ Navigation working
- ✅ Cards displaying correctly
- ✅ Tested on mobile

## What You've Learned

- Static files structure
- CSS fundamentals
- Flexbox and Grid
- Responsive design
- Media queries
- Common UI patterns
- Animations
- Accessibility
- Dark mode
- Performance optimization

## Next Steps

Styling is complete! Now let's learn about testing and deployment.

**→ Continue to [10 - Testing & Deployment](./10-testing-deployment.md)**

---

## Additional Resources

- [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [CSS Tricks](https://css-tricks.com/)
- [Flexbox Froggy](https://flexboxfroggy.com/) - Learn Flexbox
- [Grid Garden](https://cssgridgarden.com/) - Learn Grid
- [Can I Use](https://caniuse.com/) - Browser support
