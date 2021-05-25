-- Home Page - Search Tables
-- Get all database tables to populate a dropdown for selecting a table
SHOW TABLES;

-- Get all attributes from a specific database table to populate a dropdown for selecting an attribute to search
SELECT COLUMN_NAME FROM information_schema.columns WHERE TABLE_NAME = :table_choice_from_dropdown_input_Select_Table;

-- Search for entities in the selected dropdown table and the selected dropdown attribute that matches the attribute typed into the search bar
SELECT * FROM :table_choice_from_dropdown_input_Select_Table WHERE :attribute_choice_from_dropdown_Select_Attribute = :attribute_text_input_on_homepage;

--

-- Customers
-- Show all Customers in Database under "Manage Customers"
SELECT * FROM Customers;

-- Add New Customer
INSERT INTO Customers(firstName, lastName, email, phoneNumber, streetAddress, city, state, zipCode)
VALUES (:firstNameInput, :lastNameInput, :emailInput, :phoneNumberInput, :streetAddressInput, :cityInput, :stateInput, :zipCodeInput);

-- Update Customer
-- Get a Customer's data for the Update Customer form
SELECT * FROM Customers WHERE customerID = :customerID_selected_from_customers_page;

-- Update a Customer's data based on submission of the Update Customer form
UPDATE Customers SET firstName = :firstNameInput, lastName = :lastNameInput, email = :emailInput, phoneNumber = :phoneNumberInput, streetAddress = :streetAddressInput, city = :cityInput, state = :stateInput, zipCode = :zipCodeInput
WHERE customerID = :customerID_selected_from_customers_page;

-- Delete Customer
DELETE FROM Customers WHERE customerID = :customerID_selected_from_customers_page;
--


-- Orders
-- Show all Orders in Database under "Manage Orders"
SELECT * FROM Orders;

-- Add New Order
INSERT INTO Orders(customerID, totalPrice, orderDate, orderComments)
VALUES (:customerID_selcted_from_dropdown_box, :totalPriceInput, :orderDateInput, :orderCommentsInput);

-- Update Order
-- Get an Order's data for the Update Order form
SELECT * FROM Orders WHERE orderID = :orderID_selected_from_orders_page;

-- Update an Order's data based on submission of the Update Order form
UPDATE Orders SET customerID = :customerID_selected_from_dropdown_box, totalPrice = :totalPriceInput, orderDate = :orderDateInput, orderComments = :orderCommentsInput
WHERE orderID = :orderID_selected_from_orders_page;

-- Delete Order
DELETE FROM Orders WHERE orderID = :orderID_selected_from_orders_page;
--


--OrderItems
-- Show all OrderItems in Database under "Manage Order Items"
SELECT * FROM OrderItems;

-- Add New OrderItem
INSERT INTO OrderItems(orderID, productID, orderItemQuantity, orderItemPrice)
VALUES (:orderID_selected_from_dropdown_box, :productID_selected_from_dropdown_box, :orderItemQuantityInput, :orderItemPriceInput);

-- Update OrderItem
-- Get an OrderItem's data for the Update Order Items form
SELECT * FROM OrderItems WHERE orderItemID = :orderItemID_selected_from_orderItems_page;

-- Update an OrderItem's data based on submission of the Update OrderItem form
UPDATE OrderItems SET orderID = :orderID_selected_from_dropdown_box, productID = :productID_selected_from_dropdown_box, orderItemQuantity = :orderItemQuantityInput, orderItemPrice = :orderItemPriceInput
WHERE orderItemID = :orderItemID_selected_from_orderItems_page;

-- Delete OrderItem
DELETE FROM OrderItems WHERE orderItemID = :orderItemID_selected_from_orderItems_page;
--


-- Shipments
-- Show all Shipments in Database under "Manage Shipments"
SELECT * FROM Shipments;

-- Add New Shipment
INSERT INTO Shipments(orderID, trackingNumber, dateShipped)
VALUES(:orderID_selected_from_dropdown_box, :trackingNumberInput, :dateShippedInput);

-- Update Shipment
-- Get a Shipment's data for the Update Shipment form
SELECT * FROM Shipments WHERE shipmentID = :shipmentID_selected_from_shipments_page;

-- Update a Shipment's data based on submission of the Update Shipment form
UPDATE Shipments SET orderID = :orderID_selected_from_dropdown_box, trackingNumber = :trackingNumberInput, dateShipped = :dateShippedInput, dateDelivered = :dateDeliveredInput
WHERE shipmentID = :shipmentID_selected_from_shipments_page;

-- Delete Shipment
DELETE FROM Shipments WHERE shipmentID = :shipmentID_selected_from_shipments_page;
--


-- Products
-- Show all Products in Database under "Manage Products"
SELECT * FROM Products;

-- Add New Product
INSERT INTO Products(productInventory, productName, productDescription, productPrice)
VALUES (:productInventoryInput, :productNameInput, :productDescriptionInput, :productPriceInput);

-- Update Product
-- Get a Product's data for the Update Product form
SELECT * FROM Products WHERE productID = :productID_selected_from_products_page;

-- Update a Product's data based on submission of the Update Product form
UPDATE Products SET productName = :productNameInput, productInventory = :productInventoryInput, productPrice = :productPriceInput, productDescription = :productDescriptionInput
WHERE productID = :productID_selected_from_products_page;

-- Delete Product
DELETE FROM Products WHERE productID = :productID_selected_from_products_page;
--


-- Categories
-- Show all Categories in Database under "Manage Categories"
SELECT * FROM Categories;

-- Add New Category
INSERT INTO Categories(categoryName, categoryDescription)
VALUES(:categoryNameInput, :categoryDescriptionInput);

-- Update Category
-- Get a Category's data for the Update Category form
SELECT * FROM Categories WHERE categoryID = :categoryID_selected_from_categories_page;

-- Update a Category's data based on submission of the Update Category form
UPDATE Categories SET categoryName = :categoryNameInput, categoryDescription = :categoryDescriptionInput
WHERE categoryID = :categoryID_selected_from_categories_page;

-- Delete Category
DELETE FROM Categories WHERE categoryID = :categoryID_selected_from_categories_page;
--


-- ProductsCategories
-- Show all ProductsCategories in Database under "Manage ProductsCategories"
SELECT * FROM ProductsCategories;

-- Add New ProductCategory
INSERT INTO ProductsCategories(productID, categoryID)
VALUES (:productIDInput, :categoryIDInput);

-- Update ProductCategory
-- Get a Product Category's data for the Update Category form
SELECT * FROM ProductsCategories WHERE productID = :productID_selected_from_productcategory_page AND categoryID = :categoryID_selected_from_productcategory_page;

-- Update a Product Category's data based on submission of the Update Category form
UPDATE ProductsCategories SET productID = :productIDInput, categoryID = :categoryIDInput
WHERE productID = :productID_selected_from_productcategory_page AND categoryID = :categoryID_selected_from_productcategory_page;

-- Delete ProductCategory (M-to-M relationship deletion)
DELETE FROM ProductsCategories WHERE productID = :productID_selected_from_ProductCategory_page AND categoryID = :categoryID_selected_from_ProductCategory_page;
--