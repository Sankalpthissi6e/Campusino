from app import app
from models import db, Category

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Add some initial categories if they don't exist
        if not Category.query.first():
            categories = [
                Category(name='Electronics', description='Gadgets, phones, laptops, etc.'),
                Category(name='Textbooks', description='Course materials and books.'),
                Category(name='Furniture', description='Chairs, desks, beds, etc.'),
                Category(name='Clothing', description='Apparel and accessories.'),
                Category(name='Miscellaneous', description='Other items.')
            ]
            db.session.add_all(categories)
            db.session.commit()
            print("Database initialized and categories populated.")
        else:
            print("Database already initialized.")

if __name__ == '__main__':
    init_db()
