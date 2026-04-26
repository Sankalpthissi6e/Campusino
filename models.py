from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timezone

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Password = db.Column(db.String(256), nullable=False)
    Phone = db.Column(db.BigInteger, nullable=False)
    Role = db.Column(db.String(10), default='USER')
    CreatedAt = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    products = db.relationship('Product', backref='seller', lazy=True)
    orders = db.relationship('Order', backref='buyer', lazy=True)
    wishlist_items = db.relationship('Wishlist', backref='user', lazy=True)
    reviews_left = db.relationship('Review', backref='reviewer', lazy=True)
    messages_sent = db.relationship('Message', foreign_keys='Message.SenderID', backref='sender', lazy=True)
    messages_received = db.relationship('Message', foreign_keys='Message.ReceiverID', backref='receiver', lazy=True)
    
    def get_id(self):
        return str(self.UserID)

class Category(db.Model):
    __tablename__ = 'Category'
    CategoryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CategoryName = db.Column(db.String(100), unique=True, nullable=False)
    Description = db.Column(db.String(255))

    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    __tablename__ = 'Product'
    ProductID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(150), nullable=False)
    Description = db.Column(db.String(500), nullable=False)
    Price = db.Column(db.Numeric(10, 2), nullable=False)
    Type = db.Column(db.String(10), nullable=False) # SELL, RENT
    Condition = db.Column(db.String(100), nullable=False)
    Status = db.Column(db.String(20), default='AVAILABLE') # AVAILABLE, SOLD
    PostedDate = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    SellerID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    CategoryID = db.Column(db.Integer, db.ForeignKey('Category.CategoryID'), nullable=False)

    orders = db.relationship('Order', backref='product', lazy=True)
    wishlisted_by = db.relationship('Wishlist', backref='product', lazy=True)
    reviews = db.relationship('Review', backref='product', lazy=True)
    messages = db.relationship('Message', backref='product', lazy=True)

class Order(db.Model):
    __tablename__ = 'Order'
    OrderID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OrderDate = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    OrderStatus = db.Column(db.String(20), default='PENDING', nullable=False) # PENDING, CONFIRMED, CANCELLED
    Quantity = db.Column(db.Integer, nullable=False, default=1)
    
    BuyerID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('Product.ProductID'), nullable=False)

    payment = db.relationship('Payment', backref='order', uselist=False, lazy=True)

class Payment(db.Model):
    __tablename__ = 'Payment'
    PaymentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PaymentMethod = db.Column(db.String(20), nullable=False) # UPI, CARD, CASH
    PaymentStatus = db.Column(db.String(20), default='PENDING', nullable=False) # SUCCESS, FAILED, PENDING
    TransactionDate = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    OrderID = db.Column(db.Integer, db.ForeignKey('Order.OrderID'), nullable=False, unique=True)

class Message(db.Model):
    __tablename__ = 'Message'
    MessageID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MessageText = db.Column(db.String(500), nullable=False)
    Timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    SenderID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    ReceiverID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('Product.ProductID'), nullable=False)

class Review(db.Model):
    __tablename__ = 'Review'
    ReviewID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Rating = db.Column(db.Integer, nullable=False) # 1 to 5
    Comment = db.Column(db.String(255))
    ReviewDate = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('Product.ProductID'), nullable=False)

class Wishlist(db.Model):
    __tablename__ = 'Wishlist'
    WishlistID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AddedDate = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('Product.ProductID'), nullable=False)

class Report(db.Model):
    __tablename__ = 'Report'
    ReportID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Reason = db.Column(db.String(255), nullable=False)
    ReportDate = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('Product.ProductID'), nullable=False)
