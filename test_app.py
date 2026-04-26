import pytest
from app import app
from models import db, User, Category, Product, Order, Payment, Review, Wishlist, Message, Report

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    # Avoid CSRF checking during testing if any forms are used, though not heavily relying on it here
    app.config['WTF_CSRF_ENABLED'] = False 
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            # Initial Data
            cat = Category(CategoryName='Test Category')
            db.session.add(cat)
            db.session.commit()
            
            yield client
            
        # Clean up
        with app.app_context():
            db.drop_all()

def test_user_creation(client):
    with app.app_context():
        user = User(Name='testuser', Email='test@test.com', Password='hash', Phone=1234567890)
        db.session.add(user)
        db.session.commit()
        
        saved_user = User.query.filter_by(Email='test@test.com').first()
        assert saved_user is not None
        assert saved_user.Name == 'testuser'

def test_product_relationship(client):
    with app.app_context():
        user = User(Name='seller', Email='seller@test.com', Password='hash', Phone=1234567890)
        cat = Category(CategoryName='Electronics')
        db.session.add_all([user, cat])
        db.session.commit()
        
        product = Product(Title='Laptop', Description='Good condition', Price=500.0, Type='SELL', Condition='Used', SellerID=user.UserID, CategoryID=cat.CategoryID)
        db.session.add(product)
        db.session.commit()
        
        assert len(user.products) == 1
        assert user.products[0].Title == 'Laptop'
        assert product.seller.Name == 'seller'
        assert product.category.CategoryName == 'Electronics'

def test_order_and_payment(client):
    with app.app_context():
        seller = User(Name='seller', Email='seller@test.com', Password='hash', Phone=1234567890)
        buyer = User(Name='buyer', Email='buyer@test.com', Password='hash', Phone=1234567890)
        cat = Category(CategoryName='Books')
        db.session.add_all([seller, buyer, cat])
        db.session.commit()
        
        product = Product(Title='Book', Description='Math', Price=20.0, Type='SELL', Condition='New', SellerID=seller.UserID, CategoryID=cat.CategoryID)
        db.session.add(product)
        db.session.commit()
        
        order = Order(BuyerID=buyer.UserID, ProductID=product.ProductID)
        db.session.add(order)
        db.session.flush()
        
        payment = Payment(PaymentMethod='CARD', OrderID=order.OrderID)
        db.session.add(payment)
        db.session.commit()
        
        saved_order = Order.query.first()
        assert saved_order.buyer.Name == 'buyer'
        assert saved_order.product.Title == 'Book'
        assert saved_order.payment.PaymentMethod == 'CARD'
