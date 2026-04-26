from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Category, Product, Order, Payment, Review, Wishlist, Message, Report

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'  # In production, use env variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campusino.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Error Handlers ---
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('404.html'), 500

# --- Public Routes ---
@app.route('/')
def index():
    products = Product.query.filter_by(Status='AVAILABLE').all()
    categories = Category.query.all()
    return render_template('index.html', products=products, categories=categories)

@app.route('/category/<int:category_id>')
def category_products(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(CategoryID=category_id, Status='AVAILABLE').all()
    categories = Category.query.all()
    return render_template('index.html', products=products, categories=categories, current_category=category)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

# --- Auth Routes ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')

        user = User.query.filter_by(Email=email).first()
        if user:
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))

        new_user = User(
            Name=name,
            Email=email,
            Phone=int(phone),
            Password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(Email=email).first()

        if not user or not check_password_hash(user.Password, password):
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))

        login_user(user, remember=remember)
        flash(f'Welcome back, {user.Name}!', 'success')
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# --- Product Routes ---
@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        category_id = request.form.get('category_id')
        type_ = request.form.get('type')
        condition = request.form.get('condition')

        try:
            price = float(price)
            if price <= 0:
                raise ValueError
        except ValueError:
            flash('Invalid price. Must be greater than 0.', 'error')
            return redirect(url_for('add_product'))

        new_product = Product(
            Title=title,
            Description=description,
            Price=price,
            Type=type_,
            Condition=condition,
            CategoryID=category_id,
            SellerID=current_user.UserID
        )
        db.session.add(new_product)
        db.session.commit()

        flash('Product listed successfully!', 'success')
        return redirect(url_for('product_detail', product_id=new_product.ProductID))

    categories = Category.query.all()
    return render_template('add_product.html', categories=categories)

# --- Order Routes ---
@app.route('/order/<int:product_id>', methods=['POST'])
@login_required
def place_order(product_id):
    product = Product.query.get_or_404(product_id)
    if product.Status != 'AVAILABLE':
        flash('This product is no longer available.', 'error')
        return redirect(url_for('product_detail', product_id=product.ProductID))

    if product.SellerID == current_user.UserID:
        flash('You cannot buy your own product.', 'error')
        return redirect(url_for('product_detail', product_id=product.ProductID))

    payment_method = request.form.get('payment_method')
    if not payment_method:
        flash('Payment method is required.', 'error')
        return redirect(url_for('product_detail', product_id=product.ProductID))

    try:
        order = Order(BuyerID=current_user.UserID, ProductID=product.ProductID)
        db.session.add(order)
        db.session.flush()

        payment = Payment(
            PaymentMethod=payment_method,
            PaymentStatus='SUCCESS',
            OrderID=order.OrderID
        )
        db.session.add(payment)

        product.Status = 'SOLD'
        order.OrderStatus = 'CONFIRMED'

        db.session.commit()
        flash('Order placed successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while processing your order.', 'error')

    return redirect(url_for('orders'))

@app.route('/orders')
@login_required
def orders():
    my_orders = Order.query.filter_by(BuyerID=current_user.UserID).all()
    my_sales = Order.query.join(Product).filter(Product.SellerID == current_user.UserID).all()
    return render_template('orders.html', orders=my_orders, sales=my_sales)

# --- Wishlist Routes ---
@app.route('/wishlist')
@login_required
def wishlist():
    items = Wishlist.query.filter_by(UserID=current_user.UserID).all()
    return render_template('wishlist.html', items=items)

@app.route('/wishlist/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    product = Product.query.get_or_404(product_id)
    existing = Wishlist.query.filter_by(UserID=current_user.UserID, ProductID=product.ProductID).first()
    if existing:
        flash('Already in your wishlist.', 'info')
    else:
        item = Wishlist(UserID=current_user.UserID, ProductID=product.ProductID)
        db.session.add(item)
        db.session.commit()
        flash('Added to wishlist!', 'success')
    return redirect(url_for('product_detail', product_id=product.ProductID))

@app.route('/wishlist/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_wishlist(item_id):
    item = Wishlist.query.get_or_404(item_id)
    if item.UserID == current_user.UserID:
        db.session.delete(item)
        db.session.commit()
        flash('Removed from wishlist.', 'success')
    return redirect(url_for('wishlist'))

# --- Review Routes ---
@app.route('/review/<int:product_id>', methods=['POST'])
@login_required
def add_review(product_id):
    product = Product.query.get_or_404(product_id)
    rating = request.form.get('rating')
    comment = request.form.get('comment')

    if not rating:
        flash('Rating is required.', 'error')
        return redirect(url_for('product_detail', product_id=product.ProductID))

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError
    except ValueError:
        flash('Rating must be between 1 and 5.', 'error')
        return redirect(url_for('product_detail', product_id=product.ProductID))

    has_bought = Order.query.filter_by(BuyerID=current_user.UserID, ProductID=product.ProductID, OrderStatus='CONFIRMED').first()
    if not has_bought:
        flash('You can only review products you have purchased.', 'error')
        return redirect(url_for('product_detail', product_id=product.ProductID))

    existing = Review.query.filter_by(UserID=current_user.UserID, ProductID=product.ProductID).first()
    if existing:
        flash('You have already reviewed this product.', 'info')
        return redirect(url_for('product_detail', product_id=product.ProductID))

    review = Review(Rating=rating, Comment=comment, UserID=current_user.UserID, ProductID=product.ProductID)
    db.session.add(review)
    db.session.commit()
    flash('Review submitted!', 'success')
    return redirect(url_for('product_detail', product_id=product.ProductID))

# --- Message Routes ---
@app.route('/messages', methods=['GET'])
@login_required
def messages():
    received = Message.query.filter_by(ReceiverID=current_user.UserID).order_by(Message.Timestamp.desc()).all()
    sent = Message.query.filter_by(SenderID=current_user.UserID).order_by(Message.Timestamp.desc()).all()
    users = User.query.filter(User.UserID != current_user.UserID).all()
    return render_template('messages.html', received=received, sent=sent, users=users)

@app.route('/message/send', methods=['POST'])
@login_required
def send_message():
    receiver_id = request.form.get('receiver_id')
    product_id = request.form.get('product_id')
    content = request.form.get('content')

    if not receiver_id or not content or not product_id:
        flash('All fields are required.', 'error')
        return redirect(url_for('messages'))

    receiver = User.query.get(receiver_id)
    if not receiver:
        flash('Receiver not found.', 'error')
        return redirect(url_for('messages'))

    product = Product.query.get(product_id)
    if not product:
        flash('Product not found.', 'error')
        return redirect(url_for('messages'))

    message = Message(SenderID=current_user.UserID, ReceiverID=receiver.UserID, ProductID=product.ProductID, MessageText=content)
    db.session.add(message)
    db.session.commit()
    flash('Message sent!', 'success')
    return redirect(url_for('messages'))

# --- Report Route ---
@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    if request.method == 'POST':
        reason = request.form.get('reason')
        product_id = request.form.get('product_id')

        if not reason or not product_id:
            flash('All fields are required.', 'error')
            return redirect(url_for('report'))

        product_id = int(product_id)

        report = Report(Reason=reason, UserID=current_user.UserID, ProductID=product_id)
        db.session.add(report)
        db.session.commit()
        flash('Report submitted. Thank you!', 'success')
        return redirect(url_for('index'))

    products = Product.query.all()
    return render_template('report.html', products=products)

# --- Profile Route ---
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
