# Django Blog & CMS

Blog dan sistem manajemen konten yang lengkap, dibikin pake Django.

## 📚 Belajar Django

**Baru kenal Django?** Cek tutorial lengkap kita:

**→ [Tutorial Step-by-Step Lengkap](./tutorial/TUTORIAL.md)** ←  
**→ [Panduan Mulai Belajar - Dari Frontend ke Full-Stack!](./MULAI_DI_SINI.md)** ←

Tutorial ini mencakup:
- Dasar-dasar Django dan arsitekturnya (10 chapter)
- Bikin aplikasi blog ini dari awal
- Penjelasan step-by-step dengan contoh kode
- Best practice dan troubleshooting
- Dari development sampai deployment

**Cocok banget buat temen kuliah yang baru belajar HTML/CSS/JS!** Dijelasin dengan bahasa santai, banyak analogi, dan perbandingan dengan JavaScript yang lo udah tau.

## 🎉 Mulai Cepat

Aplikasinya udah jalan di: **http://localhost:8000/**

### Akun Testing

Udah ada sample akun buat testing:

**Akun Admin (Akses Penuh)**
- Username: `admin`
- Password: `admin123`
- Akses: http://localhost:8000/admin/

**Akun Author (User Biasa)**
- Username: `author`
- Password: `author123`

### Apa Aja yang Ada

✅ **5 Post Blog Sample** dengan kategori berbeda  
✅ **4 Kategori:** Teknologi, Programming, Web Development, Data Science  
✅ **Komentar Sample** di setiap post (udah disetujui)  
✅ **Sistem Authentication Lengkap** (login, register, reset password)  
✅ **Responsive Design** dengan CSS modern

## Fitur-fitur

- **Autentikasi User**: Daftar, login, logout, dan reset password
- **Post Blog**: Bikin, edit, hapus, dan publish post blog
- **Kategori**: Organisir post berdasarkan kategori
- **Komentar**: User bisa komentar di post (harus disetujui admin)
- **Search**: Cari post blog
- **Panel Admin**: Interface admin Django lengkap buat manage konten
- **Responsive Design**: Tampilan mobile-friendly

## Instalasi & Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env kalo perlu
   ```

3. **Jalanin migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Bikin sample data** (opsional tapi recommended):
   ```bash
   python manage.py create_sample_data
   ```
   Ini bakal bikin test users, kategori, post, dan komentar.

5. **Bikin superuser tambahan** (opsional):
   ```bash
   python manage.py createsuperuser
   ```

6. **Jalanin development server**:
   ```bash
   python manage.py runserver
   ```

7. **Akses aplikasinya**:
   - Website utama: http://localhost:8000/
   - Panel admin: http://localhost:8000/admin/

## Cara Pake

### Buat User Biasa
1. ✍️ Daftar akun atau pake test account (`author` / `author123`)
2. 🔐 Login buat akses fitur posting
3. ✨ Bikin post blog dengan featured image
4. 💬 Tambahin komentar di post
5. 📝 Manage post lo sendiri (edit/hapus)

### Buat Admin
1. 🎛️ Akses panel admin di `/admin/` (pake `admin` / `admin123`)
2. ✅ Setujui/tolak komentar
3. 🗂️ Manage kategori
4. 📝 Edit/hapus semua post
5. 👥 Manage users

## Struktur Project

```
/workspace/
├── blog/                   # Aplikasi blog utama
│   ├── models.py          # Model database (Post, Comment, Category)
│   ├── views.py           # Fungsi view
│   ├── forms.py           # Form Django
│   ├── urls.py            # Pola URL
│   ├── admin.py           # Konfigurasi admin
│   └── templates/         # Template HTML
│       └── blog/
├── blog_cms/              # Settings project
│   ├── settings.py        # Settings Django
│   ├── urls.py            # Konfigurasi root URL
│   └── wsgi.py            # Konfigurasi WSGI
├── static/                # File static (CSS, JS, gambar)
│   └── css/
│       └── style.css
├── media/                 # File yang diupload user
├── manage.py              # Script management Django
└── requirements.txt       # Dependencies Python
```

## Model Database

### Post
- Title, slug, konten, excerpt
- Author (ForeignKey ke User)
- Category (ForeignKey ke Category)
- Featured image
- Status (draft/published)
- Timestamps

### Comment
- Post (ForeignKey ke Post)
- Author (ForeignKey ke User)
- Content
- Status approved
- Timestamps

### Category
- Name, slug, deskripsi
- Timestamp

## Konfigurasi

### Database
Defaultnya pake SQLite. Kalo mau pake PostgreSQL:

1. Update `.env`:
   ```
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=blog_cms_db
   DB_USER=postgres
   DB_PASSWORD=password_lo
   DB_HOST=localhost
   DB_PORT=5432
   ```

2. Pastiin PostgreSQL udah jalan dan databasenya udah ada

### File Static
- Development: File static di-serve otomatis sama Django
- Production: Jalanin `python manage.py collectstatic` dan configure web server

### File Media
File yang diupload user (gambar post) disimpan di folder `media/`

## Development

### Command yang Sering Dipake

```bash
# Bikin sample data
python manage.py create_sample_data

# Jalanin migrations
python manage.py makemigrations
python manage.py migrate

# Bikin superuser
python manage.py createsuperuser

# Collect static files (buat production)
python manage.py collectstatic --noinput

# Jalanin development server
python manage.py runserver
```

### Jalanin Tests
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

1. Set `DEBUG=False` di `.env`
2. Update `ALLOWED_HOSTS` dengan domain lo
3. Set `SECRET_KEY` yang kuat
4. Configure production database (PostgreSQL recommended)
5. Setup web server (nginx/Apache) dengan Gunicorn/uWSGI
6. Configure serving file static dan media
7. Setup SSL/TLS certificates

## License

Project ini open source dan tersedia di bawah MIT License.

## Contributing

Kontribusi welcome banget! Silakan submit pull request.
