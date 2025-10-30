# Django Blog & CMS

A full-featured blog and content management system built with Django.

## 🎉 Quick Start

The application is now running at: **http://localhost:8000/**

### Test Accounts

Sample accounts have been created for testing:

**Admin Account (Full Access)**
- Username: `admin`
- Password: `admin123`
- Access: http://localhost:8000/admin/

**Author Account (Regular User)**
- Username: `author`
- Password: `author123`

### What's Included

✅ **5 Sample Blog Posts** with different categories  
✅ **4 Categories:** Technology, Programming, Web Development, Data Science  
✅ **Sample Comments** on each post (approved)  
✅ **Full Authentication System** (login, register, password reset)  
✅ **Responsive Design** with modern CSS

## Features

- **User Authentication**: Registration, login, logout, and password reset
- **Blog Posts**: Create, edit, delete, and publish blog posts
- **Categories**: Organize posts into categories
- **Comments**: Users can comment on posts (with admin approval)
- **Search**: Search through blog posts
- **Admin Panel**: Full Django admin interface for content management
- **Responsive Design**: Mobile-friendly layout

## Installation & Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings if needed
   ```

3. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create sample data** (optional but recommended):
   ```bash
   python manage.py create_sample_data
   ```
   This creates test users, categories, posts, and comments.

5. **Create additional superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   - Main site: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/

## Usage Guide

### For Users
1. ✍️ Register for an account or use test account (`author` / `author123`)
2. 🔐 Log in to access posting features
3. ✨ Create blog posts with featured images
4. 💬 Add comments to posts
5. 📝 Manage your own posts (edit/delete)

### For Admins
1. 🎛️ Access the admin panel at `/admin/` (use `admin` / `admin123`)
2. ✅ Approve/reject comments
3. 🗂️ Manage categories
4. 📝 Edit/delete any posts
5. 👥 Manage users

## Project Structure

```
/workspace/
├── blog/                   # Main blog application
│   ├── models.py          # Database models (Post, Comment, Category)
│   ├── views.py           # View functions
│   ├── forms.py           # Django forms
│   ├── urls.py            # URL patterns
│   ├── admin.py           # Admin configuration
│   └── templates/         # HTML templates
│       └── blog/
├── blog_cms/              # Project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI configuration
├── static/                # Static files (CSS, JS, images)
│   └── css/
│       └── style.css
├── media/                 # User-uploaded files
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Models

### Post
- Title, slug, content, excerpt
- Author (ForeignKey to User)
- Category (ForeignKey to Category)
- Featured image
- Status (draft/published)
- Timestamps

### Comment
- Post (ForeignKey to Post)
- Author (ForeignKey to User)
- Content
- Approved status
- Timestamps

### Category
- Name, slug, description
- Timestamp

## Configuration

### Database
By default, the project uses SQLite. To use PostgreSQL:

1. Update `.env`:
   ```
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=blog_cms_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

2. Ensure PostgreSQL is running and the database exists

### Static Files
- Development: Static files served automatically by Django
- Production: Run `python manage.py collectstatic` and configure web server

### Media Files
User-uploaded files (post images) are stored in the `media/` directory

## Development

### Common Commands

```bash
# Create sample data
python manage.py create_sample_data

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver
```

### Running Tests
```bash
python manage.py test
```

### Code Formatting
```bash
black .
```

### Linting
```bash
pylint blog/
```

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Update `ALLOWED_HOSTS` with your domain
3. Set a strong `SECRET_KEY`
4. Configure a production database (PostgreSQL recommended)
5. Set up a web server (nginx/Apache) with Gunicorn/uWSGI
6. Configure static and media file serving
7. Set up SSL/TLS certificates

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests.
