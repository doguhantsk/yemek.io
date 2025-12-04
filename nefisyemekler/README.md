# Nefis Yemekler - Yemek Tarifi Sitesi

Flask tabanlı dinamik yemek tarifi paylaşım platformu.

## Özellikler

- ✅ Kullanıcı kayıt ve giriş sistemi
- ✅ Tarif ekleme, düzenleme ve silme (CRUD)
- ✅ Kategori bazlı tarif organizasyonu
- ✅ Yorum ve puanlama sistemi
- ✅ Dosya yükleme (resim)
- ✅ Admin panel (kullanıcı, tarif, kategori, yorum yönetimi)
- ✅ Responsive tasarım (Bootstrap 5)
- ✅ SQLAlchemy ORM ile veritabanı yönetimi

## Kurulum

### 1. Virtual Environment Oluşturma

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# veya
.venv\Scripts\activate  # Windows
```

### 2. Gerekli Paketleri Yükleme

```bash
pip install -r requirements.txt
```

### 3. Veritabanını Oluşturma ve Seed Verilerini Ekleme

```bash
python seed.py
```

Bu komut:
- Veritabanı tablolarını oluşturur
- Örnek admin ve kullanıcı hesapları ekler
- 6 kategori ekler (Kahvaltı, Öğle Yemeği, Akşam Yemeği, Tatlılar, Çorbalar, Salatalar)
- 6 örnek tarif ekler
- Örnek yorumlar ve puanlar ekler
- 2 sayfa ekler (Hakkımızda, İletişim)

### 4. Uygulamayı Çalıştırma

```bash
python app.py
```

veya

```bash
flask run
```

Tarayıcınızda `http://127.0.0.1:5000` adresini açın.

## Giriş Bilgileri

### Admin Hesabı
- **Kullanıcı Adı:** admin
- **Şifre:** admin123

### Normal Kullanıcılar
- **Kullanıcı Adı:** ayse | **Şifre:** 12345
- **Kullanıcı Adı:** mehmet | **Şifre:** 12345

## Veritabanı Şeması

### Tablolar

1. **users** - Kullanıcı bilgileri
   - id, username, password_hash, is_admin, created_at

2. **categories** - Tarif kategorileri
   - id, name, slug, description, created_at

3. **recipes** - Tarifler
   - id, title, content, ingredients, instructions, prep_time, cook_time, servings, image, category_id, user_id, created_at, updated_at

4. **comments** - Yorumlar ve puanlar
   - id, recipe_id, user_id, body, rating, created_at

5. **pages** - CMS sayfaları
   - id, slug, title, content, created_at, updated_at

6. **images** - Ek görsel galerisi
   - id, filename, recipe_id, created_at

## Klasör Yapısı

```
nefisyemekler/
├── app.py                 # Ana Flask uygulaması
├── models.py              # SQLAlchemy modelleri
├── seed.py               # Veritabanı seed scripti
├── requirements.txt      # Python bağımlılıkları
├── .env                  # Çevre değişkenleri
├── .gitignore           # Git ignore dosyası
├── static/
│   ├── css/
│   │   └── style.css    # Özel CSS
│   ├── js/
│   │   └── main.js      # JavaScript
│   └── uploads/         # Yüklenen resimler
└── templates/
    ├── base.html         # Ana şablon
    ├── index.html        # Ana sayfa
    ├── login.html        # Giriş
    ├── register.html     # Kayıt
    ├── about.html        # Hakkımızda
    ├── contact.html      # İletişim
    ├── testimonials.html # Yorumlar
    ├── category.html     # Kategori sayfası
    ├── recipe_detail.html # Tarif detay
    ├── add_recipe.html   # Tarif ekleme
    ├── edit_recipe.html  # Tarif düzenleme
    ├── my_recipes.html   # Kullanıcı tarifleri
    └── admin/
        ├── dashboard.html      # Admin ana sayfa
        ├── recipes.html        # Tarif yönetimi
        ├── categories.html     # Kategori yönetimi
        ├── add_category.html   # Kategori ekleme
        ├── edit_category.html  # Kategori düzenleme
        ├── users.html          # Kullanıcı yönetimi
        ├── comments.html       # Yorum yönetimi
        ├── pages.html          # Sayfa yönetimi
        ├── add_page.html       # Sayfa ekleme
        └── edit_page.html      # Sayfa düzenleme
```

## Admin Panel İşlevleri

Admin paneline erişmek için admin hesabıyla giriş yapın ve menüden "Admin Panel" seçeneğine tıklayın.

### Dashboard
- Toplam kullanıcı, tarif, kategori ve yorum sayıları

### Tarifler
- Tüm tarifleri görüntüleme
- Tarif düzenleme ve silme

### Kategoriler
- Kategori ekleme, düzenleme ve silme
- Kategori slug yönetimi

### Kullanıcılar
- Kullanıcı listesi
- Admin yetkisi verme/alma
- Kullanıcı silme

### Yorumlar
- Tüm yorumları görüntüleme ve moderasyon
- Yorum silme

### Sayfalar
- CMS sayfa yönetimi
- HTML içerik düzenleme

## Teknolojiler

- **Backend:** Flask 3.0
- **Database:** SQLite (SQLAlchemy ORM)
- **Authentication:** Flask-Login
- **Frontend:** Bootstrap 5, Font Awesome
- **Template Engine:** Jinja2

## Özellik Detayları

### Kullanıcı İşlevleri
- Kayıt olma ve giriş yapma
- Tarif ekleme (resim yükleme dahil)
- Kendi tariflerini düzenleme ve silme
- Tariflere yorum yapma ve puan verme
- Kendi tariflerini görüntüleme

### Genel İşlevler
- Kategori bazlı tarif filtreleme
- Tarif arama ve listeleme
- Tarif detay görüntüleme
- Yıldız bazlı puanlama sistemi
- Responsive mobil uyumlu tasarım

### Admin İşlevleri
- Tüm içerikleri yönetme (CRUD)
- Kullanıcı yetkilendirme
- İçerik moderasyonu
- Site ayarları ve sayfa yönetimi

## Güvenlik

- Şifreler hash'lenerek saklanır (Werkzeug)
- Flask-Login ile oturum yönetimi
- CSRF koruması
- Dosya yükleme güvenliği (dosya tipi kontrolü)
- SQL injection koruması (SQLAlchemy ORM)

## Geliştirme Notları

- `.env` dosyasındaki `SECRET_KEY` production'da mutlaka değiştirilmeli
- Dosya yükleme boyutu limiti: 16MB
- İzin verilen resim formatları: PNG, JPG, JPEG, GIF, WEBP

## Lisans

Bu proje eğitim amaçlı geliştirilmiştir.
