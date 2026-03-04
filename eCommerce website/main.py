import stripe
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

stripe.api_key = "SECRET_KEY"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    cart_items = relationship("CartItem", back_populates="user")

class Product(db.Model):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    cart_items = relationship("CartItem", back_populates="product")

class CartItem(db.Model):
    __tablename__ = "cart_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")


with app.app_context():
    db.create_all()
    if not db.session.execute(db.select(Product)).scalars().all():
        p1 = Product(name="Osprey Fairview Unisex Reiserucksack", description="Cool backpack for traveling.", price=128.00, img_url="https://m.media-amazon.com/images/I/51KIK-cMSxL._AC_SX522_.jpg")
        p2 = Product(name="Charging Cable", description="USB A to USB C Braided Cable Compatible with iPhone 17/16/16E/15, 16 15 Plus, 17/16 15 Pro Max, Air Charging Cable, AirPods 4/AirPods Pro 2.", price=9.99, img_url="https://m.media-amazon.com/images/I/61qsnd0I-XL._SX522_.jpg")
        db.session.add_all([p1, p2])
        db.session.commit()


@app.route('/')
def home():
    result = db.session.execute(db.select(Product))
    all_products = result.scalars().all()
    return render_template("store.html", products=all_products, current_user=current_user)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if existing_user:
            flash("User with this email already exists.")
            return redirect(url_for("login"))
        hashed_pw = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8)
        new_user = User(email=form.email.data, name=form.name.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html", form=form, current_user=current_user)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if not user or not check_password_hash(user.password, form.password.data):
            flash('Invalid email or password, please try again.')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('home'))
    return render_template("login.html", form=form, current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    if not current_user.is_authenticated:
        flash("Please log in to add items to your cart.")
        return redirect(url_for('login'))
    product = db.get_or_404(Product, product_id)
    existing_item = db.session.execute(db.select(CartItem).where(CartItem.user_id == current_user.id, CartItem.product_id == product.id)).scalar()
    if existing_item:
        existing_item.quantity += 1
    else:
        new_item = CartItem(user_id=current_user.id, product_id=product.id, quantity=1)
        db.session.add(new_item)
    db.session.commit()
    flash(f"{product.name} added to cart!")
    return redirect(url_for('home'))

@app.route('/cart')
def cart():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    cart_items = db.session.execute(db.select(CartItem).where(CartItem.user_id == current_user.id)).scalars().all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render_template("cart.html", cart_items=cart_items, total_price=total_price, current_user=current_user)


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    cart_items = db.session.execute(db.select(CartItem).where(CartItem.user_id == current_user.id)).scalars().all()
    if not cart_items:
        return redirect(url_for('cart'))

    line_items = []
    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': item.product.name},
                'unit_amount': int(item.product.price * 100),
            },
            'quantity': item.quantity,
        })

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=url_for('success', _external=True),
            cancel_url=url_for('cancel', _external=True),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e)

@app.route('/success')
def success():
    cart_items = db.session.execute(db.select(CartItem).where(CartItem.user_id == current_user.id)).scalars().all()
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()
    flash("Payment successful! Thank you for your purchase.")
    return redirect(url_for('home'))

@app.route('/cancel')
def cancel():
    flash("Payment cancelled.")
    return redirect(url_for('cart'))

if __name__ == "__main__":
    app.run(debug=True, port=5002)