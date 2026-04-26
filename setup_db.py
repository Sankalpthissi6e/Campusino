import sqlite3
import os

def setup_db():
    db_path = 'instance/campusino.db'
    os.makedirs('instance', exist_ok=True)
    
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign keys in SQLite
    cursor.execute('PRAGMA foreign_keys = ON;')
    
    # 1. Execute DDL, Views, and Triggers from schema.sql
    with open('schema.sql', 'r') as f:
        schema_sql = f.read()
    
    cursor.executescript(schema_sql)
    
    # 2. Insert DML provided by the user
    dml_sql = """
    INSERT INTO User (Name, Email, Password, Phone, Role, CreatedAt)
    VALUES
    ('Rahul Sharma', 'rahul@gmail.com', 'scrypt:32768:8:1$K5Hh...mock_hash', 9876543210, 'USER', CURRENT_TIMESTAMP),
    ('Admin', 'admin@gmail.com', 'scrypt:32768:8:1$v2...mock_hash', 9999999999, 'ADMIN', CURRENT_TIMESTAMP);

    INSERT INTO Category (CategoryName, Description)
    VALUES
    ('Books', 'Academic and reference books'),
    ('Electronics', 'Gadgets and electronic items');

    INSERT INTO Product (Title, Description, Price, Type, Condition, Status, PostedDate, SellerID, CategoryID)
    VALUES
    ('DSA Book', 'Good condition DSA book', 350.00, 'SELL', 'Good', 'AVAILABLE', CURRENT_TIMESTAMP, 1, 1),
    ('Calculator', 'Scientific calculator', 800.00, 'SELL', 'New', 'AVAILABLE', CURRENT_TIMESTAMP, 1, 2);

    INSERT INTO "Order" (OrderDate, OrderStatus, Quantity, BuyerID, ProductID)
    VALUES
    (CURRENT_TIMESTAMP, 'PENDING', 1, 1, 1);

    INSERT INTO Payment (PaymentMethod, PaymentStatus, TransactionDate, OrderID)
    VALUES
    ('UPI', 'SUCCESS', CURRENT_TIMESTAMP, 1);

    INSERT INTO Message (MessageText, Timestamp, SenderID, ReceiverID, ProductID)
    VALUES
    ('Is this book still available?', CURRENT_TIMESTAMP, 1, 2, 1);

    INSERT INTO Review (Rating, Comment, ReviewDate, UserID, ProductID)
    VALUES
    (5, 'Very useful book!', CURRENT_TIMESTAMP, 1, 1);

    INSERT INTO Wishlist (UserID, ProductID, AddedDate)
    VALUES
    (1, 2, CURRENT_TIMESTAMP);

    INSERT INTO Report (Reason, ReportDate, UserID, ProductID)
    VALUES
    ('Duplicate listing', CURRENT_TIMESTAMP, 1, 2);
    """
    
    cursor.executescript(dml_sql)
    
    # Update mock hashes to real hashes so login works with test accounts
    from werkzeug.security import generate_password_hash
    cursor.execute("UPDATE User SET Password = ? WHERE Email = 'rahul@gmail.com'", (generate_password_hash('12345'),))
    cursor.execute("UPDATE User SET Password = ? WHERE Email = 'admin@gmail.com'", (generate_password_hash('admin123'),))
    
    conn.commit()
    conn.close()
    print("Database setup complete with DDL, DML, Views, and Triggers.")

if __name__ == '__main__':
    setup_db()
