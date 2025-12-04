import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from models import db, User, Category, Recipe, Comment, Page, Image
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///nefisyemekler.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Lütfen giriş yapın.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# ============= PUBLIC ROUTES =============

@app.route('/')
def index():
    """Ana sayfa - En yeni tarifler"""
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(12).all()
    categories = Category.query.all()
    return render_template('index.html', recipes=recipes, categories=categories)

@app.route('/category/<slug>')
def category(slug):
    """Kategori sayfası"""
    category = Category.query.filter_by(slug=slug).first_or_404()
    recipes = Recipe.query.filter_by(category_id=category.id).order_by(Recipe.created_at.desc()).all()
    categories = Category.query.all()
    return render_template('category.html', category=category, recipes=recipes, categories=categories)

@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    """Tarif detay sayfası"""
    recipe = Recipe.query.get_or_404(recipe_id)
    comments = Comment.query.filter_by(recipe_id=recipe_id).order_by(Comment.created_at.desc()).all()
    related_recipes = Recipe.query.filter(
        Recipe.category_id == recipe.category_id,
        Recipe.id != recipe_id
    ).limit(4).all()
    return render_template('recipe_detail.html', recipe=recipe, comments=comments, related_recipes=related_recipes)

@app.route('/recipe/<int:recipe_id>/comment', methods=['POST'])
@login_required
def add_comment(recipe_id):
    """Yorum ekleme"""
    recipe = Recipe.query.get_or_404(recipe_id)
    body = request.form.get('body')
    rating = request.form.get('rating', type=int)
    
    if not body:
        flash('Yorum boş olamaz.', 'danger')
        return redirect(url_for('recipe_detail', recipe_id=recipe_id))
    
    comment = Comment(
        recipe_id=recipe_id,
        user_id=current_user.id,
        body=body,
        rating=rating
    )
    db.session.add(comment)
    db.session.commit()
    
    flash('Yorumunuz eklendi.', 'success')
    return redirect(url_for('recipe_detail', recipe_id=recipe_id))

@app.route('/about')
def about():
    """Hakkımızda sayfası"""
    page = Page.query.filter_by(slug='about').first()
    return render_template('about.html', page=page)

@app.route('/testimonials')
def testimonials():
    """Referanslar/Yorumlar sayfası"""
    comments = Comment.query.order_by(Comment.created_at.desc()).limit(20).all()
    return render_template('testimonials.html', comments=comments)

@app.route('/contact')
def contact():
    """İletişim sayfası"""
    return render_template('contact.html')

# ============= AUTH ROUTES =============

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Kullanıcı kaydı"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        if not username or not password:
            flash('Kullanıcı adı ve şifre gerekli.', 'danger')
            return redirect(url_for('register'))
        
        if password != password_confirm:
            flash('Şifreler eşleşmiyor.', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash('Bu kullanıcı adı zaten alınmış.', 'danger')
            return redirect(url_for('register'))
        
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Kullanıcı girişi"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            flash('Giriş başarılı!', 'success')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('Kullanıcı adı veya şifre hatalı.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Çıkış"""
    logout_user()
    flash('Çıkış yapıldı.', 'info')
    return redirect(url_for('index'))

# ============= USER ROUTES =============

@app.route('/my-recipes')
@login_required
def my_recipes():
    """Kullanıcının tarifleri"""
    recipes = Recipe.query.filter_by(user_id=current_user.id).order_by(Recipe.created_at.desc()).all()
    return render_template('my_recipes.html', recipes=recipes)

@app.route('/recipe/add', methods=['GET', 'POST'])
@login_required
def add_recipe():
    """Tarif ekleme"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        category_id = request.form.get('category_id', type=int)
        prep_time = request.form.get('prep_time', type=int)
        cook_time = request.form.get('cook_time', type=int)
        servings = request.form.get('servings', type=int)
        
        if not title or not content or not category_id:
            flash('Başlık, açıklama ve kategori gerekli.', 'danger')
            return redirect(url_for('add_recipe'))
        
        # Ana resmi yükle
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                image_filename = f"{timestamp}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        
        recipe = Recipe(
            title=title,
            content=content,
            ingredients=ingredients,
            instructions=instructions,
            category_id=category_id,
            user_id=current_user.id,
            image=image_filename,
            prep_time=prep_time,
            cook_time=cook_time,
            servings=servings
        )
        db.session.add(recipe)
        db.session.commit()
        
        flash('Tarif eklendi!', 'success')
        return redirect(url_for('recipe_detail', recipe_id=recipe.id))
    
    categories = Category.query.all()
    return render_template('add_recipe.html', categories=categories)

@app.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    """Tarif düzenleme"""
    recipe = Recipe.query.get_or_404(recipe_id)
    
    if recipe.user_id != current_user.id and not current_user.is_admin:
        flash('Bu tarifi düzenleme yetkiniz yok.', 'danger')
        return redirect(url_for('recipe_detail', recipe_id=recipe_id))
    
    if request.method == 'POST':
        recipe.title = request.form.get('title')
        recipe.content = request.form.get('content')
        recipe.ingredients = request.form.get('ingredients')
        recipe.instructions = request.form.get('instructions')
        recipe.category_id = request.form.get('category_id', type=int)
        recipe.prep_time = request.form.get('prep_time', type=int)
        recipe.cook_time = request.form.get('cook_time', type=int)
        recipe.servings = request.form.get('servings', type=int)
        
        # Yeni resim yükleme
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                image_filename = f"{timestamp}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
                recipe.image = image_filename
        
        db.session.commit()
        flash('Tarif güncellendi!', 'success')
        return redirect(url_for('recipe_detail', recipe_id=recipe_id))
    
    categories = Category.query.all()
    return render_template('edit_recipe.html', recipe=recipe, categories=categories)

@app.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    """Tarif silme"""
    recipe = Recipe.query.get_or_404(recipe_id)
    
    if recipe.user_id != current_user.id and not current_user.is_admin:
        flash('Bu tarifi silme yetkiniz yok.', 'danger')
        return redirect(url_for('recipe_detail', recipe_id=recipe_id))
    
    db.session.delete(recipe)
    db.session.commit()
    flash('Tarif silindi.', 'info')
    return redirect(url_for('my_recipes'))

# ============= ADMIN ROUTES =============

def admin_required(f):
    """Admin kontrolü decorator"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Bu sayfaya erişim yetkiniz yok.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """Admin panel ana sayfa"""
    stats = {
        'users': User.query.count(),
        'recipes': Recipe.query.count(),
        'categories': Category.query.count(),
        'comments': Comment.query.count()
    }
    return render_template('admin/dashboard.html', stats=stats)

# ============= ADMIN - RECIPES =============

@app.route('/admin/recipes')
@login_required
@admin_required
def admin_recipes():
    """Admin - Tarifler listesi"""
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return render_template('admin/recipes.html', recipes=recipes)

@app.route('/admin/recipes/<int:recipe_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_recipe(recipe_id):
    """Admin - Tarif silme"""
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    flash('Tarif silindi.', 'success')
    return redirect(url_for('admin_recipes'))

# ============= ADMIN - CATEGORIES =============

@app.route('/admin/categories')
@login_required
@admin_required
def admin_categories():
    """Admin - Kategoriler listesi"""
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/categories/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_category():
    """Admin - Kategori ekleme"""
    if request.method == 'POST':
        name = request.form.get('name')
        slug = request.form.get('slug')
        description = request.form.get('description')
        
        if not name or not slug:
            flash('İsim ve slug gerekli.', 'danger')
            return redirect(url_for('admin_add_category'))
        
        if Category.query.filter_by(slug=slug).first():
            flash('Bu slug zaten kullanılıyor.', 'danger')
            return redirect(url_for('admin_add_category'))
        
        category = Category(name=name, slug=slug, description=description)
        db.session.add(category)
        db.session.commit()
        
        flash('Kategori eklendi!', 'success')
        return redirect(url_for('admin_categories'))
    
    return render_template('admin/add_category.html')

@app.route('/admin/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_category(category_id):
    """Admin - Kategori düzenleme"""
    category = Category.query.get_or_404(category_id)
    
    if request.method == 'POST':
        category.name = request.form.get('name')
        category.slug = request.form.get('slug')
        category.description = request.form.get('description')
        
        db.session.commit()
        flash('Kategori güncellendi!', 'success')
        return redirect(url_for('admin_categories'))
    
    return render_template('admin/edit_category.html', category=category)

@app.route('/admin/categories/<int:category_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_category(category_id):
    """Admin - Kategori silme"""
    category = Category.query.get_or_404(category_id)
    
    if category.recipes:
        flash('Bu kategoriye ait tarifler var, önce onları silin veya taşıyın.', 'danger')
        return redirect(url_for('admin_categories'))
    
    db.session.delete(category)
    db.session.commit()
    flash('Kategori silindi.', 'success')
    return redirect(url_for('admin_categories'))

# ============= ADMIN - USERS =============

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    """Admin - Kullanıcılar listesi"""
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def admin_toggle_user_admin(user_id):
    """Admin - Kullanıcı admin durumunu değiştir"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('Kendi admin durumunuzu değiştiremezsiniz.', 'danger')
        return redirect(url_for('admin_users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f"Kullanıcı {'admin yapıldı' if user.is_admin else 'admin değil'}", 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_user(user_id):
    """Admin - Kullanıcı silme"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('Kendi hesabınızı silemezsiniz.', 'danger')
        return redirect(url_for('admin_users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('Kullanıcı silindi.', 'success')
    return redirect(url_for('admin_users'))

# ============= ADMIN - COMMENTS =============

@app.route('/admin/comments')
@login_required
@admin_required
def admin_comments():
    """Admin - Yorumlar listesi"""
    comments = Comment.query.order_by(Comment.created_at.desc()).all()
    return render_template('admin/comments.html', comments=comments)

@app.route('/admin/comments/<int:comment_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_comment(comment_id):
    """Admin - Yorum silme"""
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Yorum silindi.', 'success')
    return redirect(url_for('admin_comments'))

# ============= ADMIN - PAGES =============

@app.route('/admin/pages')
@login_required
@admin_required
def admin_pages():
    """Admin - Sayfalar listesi"""
    pages = Page.query.all()
    return render_template('admin/pages.html', pages=pages)

@app.route('/admin/pages/add', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_add_page():
    """Admin - Sayfa ekleme"""
    if request.method == 'POST':
        slug = request.form.get('slug')
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not slug or not title:
            flash('Slug ve başlık gerekli.', 'danger')
            return redirect(url_for('admin_add_page'))
        
        if Page.query.filter_by(slug=slug).first():
            flash('Bu slug zaten kullanılıyor.', 'danger')
            return redirect(url_for('admin_add_page'))
        
        page = Page(slug=slug, title=title, content=content)
        db.session.add(page)
        db.session.commit()
        
        flash('Sayfa eklendi!', 'success')
        return redirect(url_for('admin_pages'))
    
    return render_template('admin/add_page.html')

@app.route('/admin/pages/<int:page_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_page(page_id):
    """Admin - Sayfa düzenleme"""
    page = Page.query.get_or_404(page_id)
    
    if request.method == 'POST':
        page.slug = request.form.get('slug')
        page.title = request.form.get('title')
        page.content = request.form.get('content')
        
        db.session.commit()
        flash('Sayfa güncellendi!', 'success')
        return redirect(url_for('admin_pages'))
    
    return render_template('admin/edit_page.html', page=page)

@app.route('/admin/pages/<int:page_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_page(page_id):
    """Admin - Sayfa silme"""
    page = Page.query.get_or_404(page_id)
    db.session.delete(page)
    db.session.commit()
    flash('Sayfa silindi.', 'success')
    return redirect(url_for('admin_pages'))

# ============= ERROR HANDLERS =============

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# ============= CONTEXT PROCESSORS =============

@app.context_processor
def inject_categories():
    """Tüm template'lerde kategorileri kullanılabilir yap"""
    return dict(all_categories=Category.query.all())

# ============= CLI COMMANDS =============

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized.')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
