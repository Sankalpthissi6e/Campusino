-- 3.2 Aggregate Queries
SELECT COUNT(*) AS TotalProducts FROM Product;
SELECT AVG(Price) AS AveragePrice FROM Product;
SELECT MAX(Price) AS HighestPrice FROM Product;

-- 3.3 Set Queries
SELECT ProductID FROM "Order"
INTERSECT
SELECT ProductID FROM Wishlist;

SELECT ProductID FROM "Order"
UNION
SELECT ProductID FROM Wishlist;

SELECT ProductID FROM "Order"
EXCEPT
SELECT ProductID FROM Wishlist;

-- 3.4 Subquery Queries
SELECT Title, Price
FROM Product
WHERE Price > (SELECT AVG(Price) FROM Product);

SELECT Name
FROM User
WHERE UserID IN (SELECT BuyerID FROM "Order");

SELECT Title
FROM Product
WHERE ProductID IN (SELECT ProductID FROM Review);

-- 3.5 Join Queries
SELECT Product.Title, Category.CategoryName
FROM Product
JOIN Category ON Product.CategoryID = Category.CategoryID;

SELECT User.Name, "Order".OrderID
FROM User
JOIN "Order" ON User.UserID = "Order".BuyerID;

SELECT User.Name, Review.Rating, Review.Comment
FROM Review
JOIN User ON Review.UserID = User.UserID;

-- 3.6 Views Queries (Views are created in schema.sql)
SELECT * FROM AvailableProducts;
SELECT * FROM UserReviews;

-- 3.8 Cursors (Note: MySQL specific cursor syntax provided in instructions. For an actual Python/Flask app, we fetch all via SQLAlchemy or DBAPI fetchall(). Included for completeness).
/*
DECLARE product_cursor CURSOR FOR SELECT Title FROM Product;
DECLARE user_cursor CURSOR FOR SELECT Name FROM User;
DECLARE order_cursor CURSOR FOR SELECT OrderID FROM `Order`;
*/
