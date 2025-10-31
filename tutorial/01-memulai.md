# Tutorial 01: Memulai dengan Django

## Overview

Di bagian ini, lo bakal setup development environment dan pahamin konsep dasar Django web development.

## Apa itu Django?

Bayangin gini - lo udah bisa bikin website pake HTML, CSS, dan JavaScript kan? Nah, itu artinya lo bisa bikin tampilan website yang keren. Tapi ada masalahnya:

- **Data dari mana?** Lo bikin HTML statis, kontennya ga bisa berubah-ubah
- **User gimana login?** JavaScript doang ga cukup buat handle authentication yang aman
- **Database gimana?** Lo perlu simpan data user, post blog, dll

**Nah, di sinilah Django masuk!**

Django itu framework Python buat bikin website yang **dinamis** dan **full-stack**. Artinya:
- Lo bisa simpan dan ambil data dari database
- Lo bisa handle user login/logout dengan aman
- Lo bisa generate HTML secara otomatis dengan data yang berubah-ubah
- Lo bisa bikin API buat frontend lo

### Analogi Sederhana

Kalo lo bikin website pake HTML/CSS/JS doang, itu kayak:
- **HTML/CSS/JS** = Toko offline yang tampilan-nya bagus tapi datanya tetap (statis)

Kalo pake Django:
- **Django** = Toko online lengkap dengan database barang, sistem login, shopping cart, dll (dinamis)
- **HTML/CSS/JS** = Masih dipake buat tampilan, tapi sekarang kontennya bisa berubah dari database

## Apa yang Django Kasih ke Lo?

Django include banyak hal yang udah jadi:

1. **ORM (Object-Relational Mapping):** Kerja sama database pake Python, ga perlu nulis SQL
2. **Admin Interface:** Dashboard admin gratis buat manage konten
3. **Authentication System:** User login/logout udah built-in
4. **URL Routing:** Atur URL website lo dengan gampang
5. **Template Engine:** Bikin HTML yang dinamis (kayak variabel di HTML)
6. **Security Features:** Proteksi dari hacking (SQL injection, XSS, CSRF, dll)

## Arsitektur: MTV Pattern (Model-Template-View)

Lo mungkin denger MVC (Model-View-Controller) di JavaScript framework. Django pake **MTV** yang mirip tapi beda nama:

```
┌─────────────────────────────────────────┐
│         Browser (User)                   │
│    "Gue mau lihat halaman blog"         │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│            URLs                          │
│    "OK, request ini ke View mana ya?"   │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│            Views                         │
│  "Ambil data dari Model, terus kasih    │
│   ke Template buat di-render"           │
└────┬───────────────────────────┬────────┘
     │                           │
     ▼                           ▼
┌─────────┐               ┌──────────┐
│ Models  │               │Templates │
│(Database)               │  (HTML)  │
│ "Data   │               │ "Tampilin│
│  blog"  │               │  data"   │
└─────────┘               └──────────┘
```

### Jelasin Lebih Detail:

1. **Models (Database)** 
   - Tempat lo define struktur data (kayak table di database)
   - Contoh: Model `BlogPost` punya field `title`, `content`, `author`, dll
   - Lo ga perlu nulis SQL, tinggal pake Python aja

2. **Templates (HTML Dinamis)**
   - File HTML lo yang bisa punya **variabel** dan **logic**
   - Contoh: `<h1>{{ post.title }}</h1>` - title diambil dari database
   - Kayak HTML biasa tapi bisa ada variabel Python di dalamnya

3. **Views (Logic/Controller)**
   - Fungsi Python yang handle request dari user
   - Ambil data dari Model, terus kirim ke Template
   - Contoh: Ambil semua blog post dari database, terus render ke halaman

### Contoh Flow:

1. User buka `http://website.com/blog/`
2. Django liat di **URLs**: "Oh, `/blog/` harus ke view `blog_list`"
3. **View** `blog_list` jalan:
   - Ambil semua blog post dari **Model** (database)
   - Kirim data itu ke **Template** `blog_list.html`
4. **Template** render HTML dengan data dari database
5. User liat halaman blog dengan list semua post

## Perbandingan dengan Yang Lo Udah Tau

### HTML/CSS/JavaScript Biasa:
```html
<!-- index.html - STATIS -->
<h1>Welcome to My Blog</h1>
<div class="post">
  <h2>Post Title 1</h2>
  <p>Konten post...</p>
</div>
<div class="post">
  <h2>Post Title 2</h2>
  <p>Konten post...</p>
</div>
```
**Masalah:** Harus edit HTML manual tiap kali ada post baru!

### Dengan Django:
```html
<!-- blog_list.html - DINAMIS -->
<h1>Welcome to My Blog</h1>
{% for post in posts %}
  <div class="post">
    <h2>{{ post.title }}</h2>
    <p>{{ post.content }}</p>
  </div>
{% endfor %}
```
**Keuntungan:** Post diambil dari database otomatis! Tinggal tambahin di admin panel.

## Setup Environment

### Step 1: Check Python Installation

Buka terminal/command prompt lo, terus cek Python udah ada belum:

```bash
python --version
# atau
python3 --version
```

Lo perlu **Python 3.8 atau lebih baru**. Kalo belum ada, download di [python.org](https://www.python.org/).

**Note buat temen lo yang baru belajar:** Python itu bahasa programming yang gampang dipelajari. Kalo belum ngerti Python, belajar basic-nya dulu sekitar 1-2 minggu (variables, functions, loops, classes).

### Step 2: Bikin Folder Project

```bash
mkdir django-blog-tutorial
cd django-blog-tutorial
```

**Penjelasan:**
- `mkdir` = make directory (bikin folder)
- `cd` = change directory (masuk ke folder)

### Step 3: Bikin Virtual Environment

Virtual environment itu kayak "kotak terpisah" buat install package Python. Kenapa perlu?
- Tiap project punya dependencies sendiri
- Ga ganggu project lain
- Gampang manage versi package

```bash
# Bikin virtual environment
python -m venv venv

# Aktifin
# Di macOS/Linux:
source venv/bin/activate

# Di Windows:
venv\Scripts\activate
```

Kalo berhasil, lo bakal liat `(venv)` di awal baris terminal lo.

**Tips:** Setiap kali lo buka terminal baru, harus aktifin venv lagi pake command di atas!

### Step 4: Install Django

```bash
pip install --upgrade pip
pip install Django
```

**Penjelasan:**
- `pip` = package manager Python (kayak npm di JavaScript)
- Command di atas install Django versi terbaru

Verify instalasi:

```bash
python -m django --version
```

Harusnya keluar versi Django (misal: 4.2.7)

## Django Project Structure

Sebelum kita mulai coding, lo perlu ngerti struktur project Django. Di [Tutorial 02](./02-setup-project.md), lo bakal setup project lengkap dengan configuration yang production-ready. 

Tapi buat sekarang, cukup tau konsep dasarnya:

**Project vs App:**
- **Project** = Keseluruhan website (misal: blog_cms)
- **App** = Komponen/modul tertentu (misal: blog, users, products)

**File-file penting:**
- **`manage.py`** - Tool buat jalanin command Django (runserver, migrate, dll)
- **`settings.py`** - Konfigurasi project (database, apps, security)
- **`urls.py`** - URL routing (misal: `/blog/` ke mana)
- **`models.py`** - Define struktur database
- **`views.py`** - Logic yang handle request
- **`templates/`** - File HTML

**Note:** Tutorial ini fokus ke konsep. Di Tutorial 02, lo bakal hands-on bikin project lengkap!

## Contoh Simpel: Views dan Templates

Cukup ngerti konsep dasarnya dulu. Nanti di tutorial selanjutnya, lo bakal praktek langsung bikin views dan templates.

**View = Fungsi Python**
```python
def home(request):
    return render(request, 'home.html', {'data': 'Hello!'})
```

**Template = HTML + Variabel**
```html
<h1>{{ data }}</h1>  <!-- Prints: Hello! -->
```

**URL Routing**
```python
urlpatterns = [
    path('', views.home, name='home'),
]
```

**Flow:** User buka `/` → Django panggil `views.home` → Render `home.html` dengan data → User liat HTML

Simpel kan? Sekarang lo udah ngerti **konsepnya**. Di Tutorial 02-10, lo bakal **praktik** bikin blog lengkap!

## Kesimpulan Chapter 1

Lo udah belajar **KONSEP DASAR** Django:

✅ Apa itu Django dan kenapa perlu framework  
✅ Arsitektur MTV (Model-Template-View)  
✅ Setup development environment (Python, venv, Django)  
✅ Perbedaan Project vs App  
✅ Konsep Views, Templates, dan URL routing  
✅ Template syntax (variables, loops)  

**Ini chapter pengenalan!** Lo baru ngerti konsepnya aja. Mulai Chapter 2, lo bakal **hands-on** bikin project blog lengkap step by step.

### Yang Lo Perlu Sekarang:

1. ✅ Python installed (version 3.8+)
2. ✅ Virtual environment ready
3. ✅ Django installed
4. ✅ Paham konsep MTV

Udah? Bagus! Lanjut ke praktik!  

### Hubungan dengan HTML/CSS/JS yang Lo Udah Tau

- **HTML/CSS** - Masih lo pake di templates, ga berubah!
- **JavaScript** - Bisa lo tambahin di templates buat interactivity
- **Django** - Handle backend: database, authentication, logic

Django **ga ngeganti** skill HTML/CSS/JS lo - malah **ngeboost** dengan kemampuan backend!

## Next Steps

Di [Chapter 2](./02-setup-project.md), lo bakal belajar lebih dalam tentang:
- Request/Response cycle detail
- Settings dan configuration
- Best practices Django
- Project structure yang bener

Siap lanjut? Let's go! 🚀

## Troubleshooting

### Error: "python: command not found"
**Solusi:** Install Python dulu dari python.org

### Error: "No module named django"
**Solusi:** Pastiin venv udah diaktifin, terus `pip install Django`

### Server ga jalan
**Solusi:** Check ada error message ga. Biasanya karena:
- Port 8000 udah dipake (coba `python manage.py runserver 8001`)
- Ada syntax error di code lo

### Template not found
**Solusi:** 
- Check nama file template bener ga
- Pastiin folder structure: `blog/templates/blog/home.html`
- Check app udah di-register di `INSTALLED_APPS`
