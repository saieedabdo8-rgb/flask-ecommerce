import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, Admin, Product, Order

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change-this-secret-key-in-production')

instance_path = os.path.join(app.root_path, 'instance')
os.makedirs(instance_path, exist_ok=True)
db_path = os.path.join(instance_path, 'shop.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Admin, int(user_id))


with app.app_context():
    db.create_all()
    admin = Admin.query.first()
    if admin:
        admin.username = 'Abdelrhman'
        admin.set_password('saieedabdo')
    else:
        admin = Admin(username='Abdelrhman')
        admin.set_password('saieedabdo')
        db.session.add(admin)
    db.session.commit()


@app.route('/')
def index():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('index.html', products=products)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        flash('المنتج غير موجود', 'error')
        return redirect(url_for('index'))
    return render_template('product_detail.html', product=product)


@app.route('/order/<int:product_id>', methods=['POST'])
def place_order(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        flash('المنتج غير موجود', 'error')
        return redirect(url_for('index'))

    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    address = request.form.get('address', '').strip()

    if not name or not phone or not address:
        flash('يرجى ملء جميع الحقول', 'error')
        return redirect(url_for('product_detail', product_id=product_id))

    order = Order(
        customer_name=name,
        customer_phone=phone,
        customer_address=address,
        product_id=product_id
    )
    db.session.add(order)
    db.session.commit()
    flash('تم إرسال طلبك بنجاح! سنتواصل معك قريباً', 'success')
    return redirect(url_for('index'))


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
    return render_template('admin_login.html')


@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))


@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    products = Product.query.order_by(Product.created_at.desc()).all()
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin_dashboard.html', products=products, orders=orders)


@app.route('/admin/products/add', methods=['POST'])
@login_required
def add_product():
    title = request.form.get('title', '').strip()
    price = request.form.get('price', '').strip()
    description = request.form.get('description', '').strip()
    image_url = request.form.get('image_url', '').strip()

    if not title or not price:
        flash('عنوان المنتج والسعر مطلوبان', 'error')
        return redirect(url_for('admin_dashboard'))

    try:
        price = float(price)
    except ValueError:
        flash('السعر يجب أن يكون رقماً', 'error')
        return redirect(url_for('admin_dashboard'))

    product = Product(title=title, price=price, description=description, image_url=image_url)
    db.session.add(product)
    db.session.commit()
    flash('تم إضافة المنتج بنجاح', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/products/edit/<int:product_id>', methods=['POST'])
@login_required
def edit_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        flash('المنتج غير موجود', 'error')
        return redirect(url_for('admin_dashboard'))

    product.title = request.form.get('title', product.title).strip()
    product.price = float(request.form.get('price', product.price))
    product.description = request.form.get('description', product.description or '').strip()
    product.image_url = request.form.get('image_url', product.image_url or '').strip()
    db.session.commit()
    flash('تم تحديث المنتج بنجاح', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = db.session.get(Product, product_id)
    if product:
        Order.query.filter_by(product_id=product_id).delete()
        db.session.delete(product)
        db.session.commit()
        flash('تم حذف المنتج', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/orders/delete/<int:order_id>', methods=['POST'])
@login_required
def delete_order(order_id):
    order = db.session.get(Order, order_id)
    if order:
        db.session.delete(order)
        db.session.commit()
        flash('تم حذف الطلب', 'success')
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
