from logging import exception
import re
from flask import Flask, render_template, request, redirect
from db_credentials import host, user, passwd, db
from db_connector import connect_to_database, execute_query
import datetime

DEBUG = False

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")



"""
CUSTOMERS
"""

@app.route('/customers')
def customers():
    db_connection = connect_to_database()

    query = "SELECT * FROM `Customers`;"
    result = execute_query(db_connection, query).fetchall()
    return render_template('customers.html', customers = result)


@app.route('/addcustomer', methods=['POST'])
def add_customer():
    db_connection = connect_to_database()

    first_name = request.form['first_name'] or None
    last_name = request.form['last_name'] or None
    email = request.form['email'] or None
    phone_number = request.form['phone_number'] or None
    street_address = request.form['street_address'] or None
    city = request.form['city'] or None
    state = request.form['state'] or None
    zip_code = request.form['zip_code'] or None

    try:

        query = "INSERT INTO `Customers` (`firstName`, `lastName`, `email`, `phoneNumber`, `streetAddress`, `city`, `state`, `zipCode`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data = (first_name, last_name, email, phone_number, street_address, city, state, zip_code)
        execute_query(db_connection, query, data)

        return redirect('/customers')
    
    except:
        return "There was an issue adding the Customer. Please make sure text fields are not empty."


@app.route('/searchcustomers', methods=['POST'])
def search_customers():
    db_connection = connect_to_database()

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone_number = request.form['phone_number']
    street_address = request.form['street_address']
    city = request.form['city']
    state = request.form['state']
    zip_code = request.form['zip_code']

    try:
        query = f"""SELECT * FROM `Customers` 
        WHERE (`firstName` = '{first_name}' OR '{first_name}' = '') 
        AND (`lastName` = '{last_name}' OR '{last_name}' = '') 
        AND (`email` = '{email}' OR '{email}' = '') 
        AND (`phoneNumber` = '{phone_number}' OR '{phone_number}' = '') 
        AND (`streetAddress` = '{street_address}' OR '{street_address}' = '') 
        AND (`city` = '{city}' OR '{city}' = '') 
        AND (`state` = '{state}' OR '{state}' = '') 
        AND (`zipCode` = '{zip_code}' OR '{zip_code}' = '');"""

        result = execute_query(db_connection, query).fetchall()
        return render_template('customers.html', customers = result)
    
    except:
        return "There was an issue searching Customers."


@app.route('/deletecustomer/<int:id>')
def delete_customer(id):
    db_connection = connect_to_database()

    try:
        query = f"DELETE FROM `Customers` WHERE `customerID` = {id};"
        execute_query(db_connection, query)
        return redirect('/customers')
    except:
        return "There was an error deleting this Customer."


@app.route('/updatecustomer/<int:id>', methods=['POST', 'GET'])
def update_customer(id):
    db_connection = connect_to_database()
    try:
        query = f"SELECT * FROM `Customers` WHERE `customerID` = {id};"
        result = execute_query(db_connection, query).fetchall()
        return render_template('updatecustomer.html', customer = result)
    except:
        return "There was an error updating this Customer."

@app.route('/updatedcustomer/<int:id>', methods=['POST', 'GET'])
def update_customer_process(id):
    db_connection = connect_to_database()
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone_number = request.form['phone_number']
    street_address = request.form['street_address']
    city = request.form['city']
    state = request.form['state']
    zip_code = request.form['zip_code']
    query = f"UPDATE `Customers` SET `firstName` = '{first_name}', `lastName` = '{last_name}', `email` = '{email}', `phoneNumber` = '{phone_number}', `streetAddress` = '{street_address}', `city` = '{city}', `state` = '{state}', `zipCode` = '{zip_code}' WHERE `customerID` = {id};"
    execute_query(db_connection, query)
    return redirect('/customers')

    
"""
ORDERS
"""

@app.route('/orders')
def orders():
    db_connection = connect_to_database()
 
    query = "SELECT * FROM `Orders`;"
    result = execute_query(db_connection, query).fetchall()

    customers_query = "SELECT `customerID`, `firstName`, `lastName`, `email` FROM `Customers`;"
    customers_result = execute_query(db_connection, customers_query).fetchall()

    return render_template('orders.html', orders = result, customers = customers_result)


@app.route('/addorder', methods=['POST'])
def add_order():
    db_connection = connect_to_database()
        
    customer_id = request.form['customer'] or None
    total_price = request.form['total_price'] or None
    x = request.form['order_date'] or None
    order_comments = request.form['order_comments'] or None

    try:
        order_date = datetime.datetime.strptime(x, "%Y-%m-%d")
        query = "INSERT INTO `Orders` (`customerID`, `totalPrice`, `orderDate`, `orderComments`) VALUES (%s, %s, %s, %s)"
        data = (customer_id, total_price, order_date, order_comments)
        execute_query(db_connection, query, data)
    
        return redirect('/orders')

    except:
        return "There was an issue adding the Order. Please make sure text fields are filled out properly."


@app.route('/searchorders', methods=['POST'])
def search_orders():
    db_connection = connect_to_database()
    
    customer_id = request.form['customer']
    total_price = request.form['total_price']
    order_date = request.form['order_date']
    order_comments = request.form['order_comments']
    try:
        query = f"""SELECT * FROM `Orders` 
        WHERE (`customerID` = '{customer_id}' OR '{customer_id}' = '') 
        AND (`totalPrice` = '{total_price}' OR '{total_price}' = '') 
        AND (`orderDate` = '{order_date}' OR '{order_date}' = '') 
        AND (`orderComments` = '{order_comments}' OR '{order_comments}' = '');"""

        result = execute_query(db_connection, query).fetchall()

        customers_query = "SELECT `customerID`, `firstName`, `lastName`, `email` FROM `Customers`;"
        customers_result = execute_query(db_connection, customers_query).fetchall()

        return render_template('orders.html', orders = result, customers = customers_result)

    except:
        return "There was an issue searching Orders."

@app.route('/deleteorder/<int:id>')
def delete_order(id):
    db_connection = connect_to_database()

    try:
        query = f"DELETE FROM `Orders` WHERE `orderID` = {id};"
        execute_query(db_connection, query)
        return redirect('/orders')
    except:
        return "There was an error deleting this Order."


@app.route('/updateorder/<int:id>', methods=['POST', 'GET'])
def update_order(id):
    db_connection = connect_to_database()
    query = f"SELECT * FROM `Orders` WHERE `orderID` = {id};"
    result = execute_query(db_connection, query).fetchall()

    find_customer_id = f"SELECT `customerID` FROM `Orders` WHERE `orderID` = {id};"
    find_customer_result = execute_query(db_connection, find_customer_id).fetchone()
    customer_query = f"SELECT `customerID`, `firstName`, `lastName`, `email` FROM `Customers` WHERE `customerID` = '{find_customer_result[0]}';"
    customer_result = execute_query(db_connection, customer_query).fetchall()

    customers_query = "SELECT `customerID`, `firstName`, `lastName`, `email` FROM `Customers`;"
    customers_result = execute_query(db_connection, customers_query).fetchall()
    return render_template('updateorder.html', order = result, customers = customers_result, order_customer = customer_result)


@app.route('/updatedorder/<int:id>', methods=['POST', 'GET'])
def update_order_process(id):
    try:
        db_connection = connect_to_database()
        customer_id = request.form['customer']
        if customer_id == "":
                customer_id = None
        total_price = request.form['total_price']
        x = request.form['order_date']
        order_date = datetime.datetime.strptime(x, "%Y-%m-%d")
        order_comments = request.form['order_comments']
        query = f"UPDATE `Orders` SET `customerID` = {customer_id}, `totalPrice` = {total_price}, `orderDate` = '{order_date}', `orderComments` = '{order_comments}' WHERE `orderID` = {id};"
        execute_query(db_connection, query)
        return redirect('/orders')
    except:
        return "You have entered an invalid value. Please make sure all fields are filled out properly."


"""
ORDER ITEMS
"""

@app.route('/orderitems')
def order_items():
    db_connection = connect_to_database()

    query = "SELECT * FROM `OrderItems`;"
    result = execute_query(db_connection, query).fetchall()

    # queries for Products and Orders when adding new OrderItem
    products_query = "SELECT `productID`, `productName` FROM `Products`;"
    products_result = execute_query(db_connection, products_query).fetchall()

    orders_query = "SELECT `orderID`, `customerID` FROM `Orders`;"
    orders_result = execute_query(db_connection, orders_query).fetchall()

    return render_template('orderitems.html', order_items = result, products = products_result, orders = orders_result)


@app.route('/addorderitem', methods=['POST'])
def add_order_item():
    db_connection = connect_to_database()

    order_id = request.form['order'] or None
    product_id = request.form['product'] or None
    order_item_quantity = request.form['order_item_quantity'] or None
    order_item_price = request.form['order_item_price'] or None

    try:
        query = "INSERT INTO `OrderItems` (`orderID`, `productID`, `orderItemQuantity`, `orderItemPrice`) VALUES (%s, %s, %s, %s)"
        data = (order_id, product_id, order_item_quantity, order_item_price)
        execute_query(db_connection, query, data)
    
        return redirect('/orderitems')

    except:
        return "There was an issue adding the Order Item. Please make sure text fields aren't empty"


@app.route('/searchorderitems', methods=['POST'])
def search_order_items():
    db_connection = connect_to_database()

    order_id = request.form['order']
    product_id = request.form['product']
    order_item_quantity = request.form['order_item_quantity']
    order_item_price = request.form['order_item_price']

    try:
        query = f"""SELECT * FROM `OrderItems` 
        WHERE (`orderID` = '{order_id}' OR '{order_id}' = '') 
        AND (`productID` = '{product_id}' OR '{product_id}' = '') 
        AND (`orderItemQuantity` = '{order_item_quantity}' OR '{order_item_quantity}' = '') 
        AND (`orderItemPrice` = '{order_item_price}' OR '{order_item_price}' = '');"""
        
        result = execute_query(db_connection, query).fetchall()

        # queries for Products and Orders
        products_query = "SELECT `productID`, `productName` FROM `Products`;"
        products_result = execute_query(db_connection, products_query).fetchall()

        orders_query = "SELECT `orderID` FROM `Orders`;"
        orders_result = execute_query(db_connection, orders_query).fetchall()

        return render_template('orderitems.html', order_items = result, products = products_result, orders = orders_result)

    except:
        return "There was an issue searching Order Items."


@app.route('/deleteorderitem/<int:id>')
def delete_order_item(id):
    db_connection = connect_to_database()

    try:
        query = f"DELETE FROM `OrderItems` WHERE `orderItemID` = {id};"
        execute_query(db_connection, query)

        return redirect('/orderitems')

    except:
        return "There was an error deleting this Order Item."


@app.route('/updateorderitem/<int:id>', methods=['POST', 'GET'])
def update_orderItems(id):
    db_connection = connect_to_database()
    query = f"SELECT * FROM `OrderItems` WHERE `orderItemID` = {id};"
    result = execute_query(db_connection, query).fetchall()

    find_order_id = f"SELECT `orderID` FROM `OrderItems` WHERE `orderItemID` = {id};"
    find_order_result = execute_query(db_connection, find_order_id).fetchone()

    find_product_id = f"SELECT `productID` FROM `OrderItems` WHERE `orderItemID` = {id};"
    find_product_result = execute_query(db_connection, find_product_id).fetchone()
    product_query = f"SELECT `productID`, `productName` FROM `Products` WHERE `productID` = '{find_product_result[0]}';"
    product_result = execute_query(db_connection, product_query).fetchall()

    products_query = "SELECT `productID`, `productName` FROM `Products`;"
    products_result = execute_query(db_connection, products_query).fetchall()

    orders_query = "SELECT `orderID`, `customerID` FROM `Orders`;"
    orders_result = execute_query(db_connection, orders_query).fetchall()
    return render_template('updateorderitem.html', order_items = result, products = products_result, orders = orders_result, product = product_result, order = find_order_result)


@app.route('/updatedorderitem/<int:id>', methods=['POST', 'GET'])
def update_orderItems_process(id):
    db_connection = connect_to_database()

    order_id = request.form['order']
    product_id = request.form['product']
    item_quantity = request.form['item_quantity']
    item_price = request.form['item_price']
    
    query = f"UPDATE `OrderItems` SET `orderID` = {order_id}, `productID` = {product_id}, `orderItemQuantity` = {item_quantity}, `orderItemPrice` = {item_price} WHERE `orderItemID` = {id};"
    execute_query(db_connection, query)
    return redirect('/orderitems')



"""
SHIPMENTS
"""

@app.route('/shipments')
def shipments():
    db_connection = connect_to_database()

    query = "SELECT * FROM `Shipments`;"
    result = execute_query(db_connection, query).fetchall()

    # query for Orders when adding new Shipment
    orders_query = "SELECT `orderID`, `customerID` FROM `Orders`;"
    orders_result = execute_query(db_connection, orders_query).fetchall()

    return render_template('shipments.html', shipments = result, orders = orders_result)


@app.route('/addshipment', methods=['POST'])
def add_shipment():
    db_connection = connect_to_database()
    
    order_id = request.form['order_id'] or None
    tracking_number = request.form['tracking_number'] or None
    x = request.form['date_shipped'] or None
    y = request.form['date_delivered'] or None

    

    try:
        if y is None:
            date_delivered = None
        else:
            date_delivered = datetime.datetime.strptime(y, "%Y-%m-%d")
        date_shipped = datetime.datetime.strptime(x, "%Y-%m-%d")
        query = "INSERT INTO `Shipments` (`orderID`, `trackingNumber`, `dateShipped`, `dateDelivered`) VALUES (%s, %s, %s, %s)"
        data = (order_id, tracking_number, date_shipped, date_delivered)
        execute_query(db_connection, query, data)
    
        return redirect('/shipments')

    except:
        return "There was an issue adding the Shipment. Please make sure the fields are filled out properly."


@app.route('/searchshipments', methods=['POST'])
def search_shipments():
    db_connection = connect_to_database()
    
    order_id = request.form['order_id']
    tracking_number = request.form['tracking_number']
    date_shipped = request.form['date_shipped']
    date_delivered = request.form['date_delivered']

    try:
        query = f"""SELECT * FROM `Shipments` 
        WHERE (`orderID` = '{order_id}' OR '{order_id}' = '') 
        AND (`trackingNumber` = '{tracking_number}' OR '{tracking_number}' = '') 
        AND (`dateShipped` = '{date_shipped}' OR '{date_shipped}' = '') 
        AND (`dateDelivered` = '{date_delivered}' OR '{date_delivered}' = '');"""
        
        result = execute_query(db_connection, query).fetchall()

        orders_query = "SELECT `orderID`, `customerID` FROM `Orders`;"
        orders_result = execute_query(db_connection, orders_query).fetchall()
        
        return render_template('shipments.html', shipments = result, orders = orders_result)

    except:
        return "There was an issue searching Shipments."


@app.route('/deleteshipment/<int:id>')
def delete_shipment(id):
    db_connection = connect_to_database()

    try:
        query = f"DELETE FROM `Shipments` WHERE `shipmentID` = {id};"
        execute_query(db_connection, query)
        return redirect('/shipments')

    except:
        return "There was an error deleting this Shipment."


@app.route('/updateshipment/<int:id>', methods=['POST', 'GET'])
def update_shipment(id):
    db_connection = connect_to_database()
    query = f"SELECT * FROM `Shipments` WHERE `shipmentID` = {id};"
    result = execute_query(db_connection, query).fetchall()

    find_order_id = f"SELECT `orderID` FROM `Shipments` WHERE `shipmentID` = {id};"
    find_order_result = execute_query(db_connection, find_order_id).fetchone()

    orders_query = "SELECT `orderID` FROM `Orders`;"
    orders_result = execute_query(db_connection, orders_query).fetchall()
    return render_template('updateshipment.html', shipment = result, orders = orders_result)


@app.route('/updatedshipment/<int:id>', methods=['POST', 'GET'])
def update_shipment_process(id):
    try:
        db_connection = connect_to_database()
        order_id = request.form['order'] or None
        tracking_number = request.form['tracking_number'] or None
        x = request.form['date_shipped'] or None
        y = request.form['date_delivered'] or None

        if y is None:
            date_delivered = None
        else:
            date_delivered = datetime.datetime.strptime(y, "%Y-%m-%d")
        date_shipped = datetime.datetime.strptime(x, "%Y-%m-%d")

        check_null = [order_id, date_shipped]
        for i in check_null:
            if not i:
                raise Exception
                
        query = f"UPDATE Shipments SET orderID = {order_id}, trackingNumber = '{tracking_number}', dateShipped = '{date_shipped}', dateDelivered = '{date_delivered}' WHERE shipmentID = {id};"
        execute_query(db_connection, query)
        return redirect('/shipments')
    except:
        return "You have entered an invalid value. Please make sure all fields are filled out properly."


"""
PRODUCTS
"""

@app.route('/products')
def products():
    db_connection = connect_to_database()

    query = "SELECT * FROM `Products`;"
    result = execute_query(db_connection, query).fetchall()

    category_query = "SELECT `categoryID`, `categoryName` FROM `Categories`;"
    category_result = execute_query(db_connection, category_query)

    return render_template('products.html', products = result, categories = category_result)
    

@app.route('/addproduct', methods=['POST'])
def add_product():
    db_connection = connect_to_database()
    
    product_name = request.form['product_name'] or None
    product_inventory = request.form['product_inventory'] or None
    product_price = request.form['product_price'] or None
    product_description = request.form['product_description'] or None
    category_id = request.form['category_id'] or None

    try:
        query = "INSERT INTO `Products` (`productName`, `productInventory`, `productPrice`, `productDescription`) VALUES (%s, %s, %s, %s)"
        data = (product_name, product_inventory, product_price, product_description)
        cursor = execute_query(db_connection, query, data)

        # Add Product to ProductsCategories if Category is specified
        if category_id:
            product_id = cursor.lastrowid
            query = "INSERT INTO `ProductsCategories` (`productID`, `categoryID`) VALUES (%s, %s)"
            data = (product_id, category_id)
            execute_query(db_connection, query, data)
    
        return redirect('/products')

    except:
        return "There was an issue adding the Product. Please make sure text fields aren't empty."


@app.route('/searchproducts', methods=['POST'])
def search_products():
    db_connection = connect_to_database()
    
    product_name = request.form['product_name']
    product_inventory = request.form['product_inventory']
    product_price = request.form['product_price']
    product_description = request.form['product_description']

    try:
        query = f"""SELECT * FROM `Products` 
        WHERE (`productName` = '{product_name}' OR '{product_name}' = '') 
        AND (`productInventory` = '{product_inventory}' OR '{product_inventory}' = '') 
        AND (`productPrice` = '{product_price}' OR '{product_price}' = '') 
        AND (`productDescription` = '{product_description}' OR '{product_description}' = '');"""
        
        result = execute_query(db_connection, query).fetchall()
        return render_template('products.html', products = result)

    except:
        return "There was an issue searching Products."


@app.route('/deleteproduct/<int:id>')
def delete_product(id):
    db_connection = connect_to_database()

    try:
        query = f"DELETE FROM `Products` WHERE `productID` = {id};"
        execute_query(db_connection, query)
        return redirect('/products')
    except:
        return "There was an error deleting this Product."


@app.route('/updateproduct/<int:id>', methods=['POST', 'GET'])
def update_product(id):
    db_connection = connect_to_database()
    query = f"SELECT * FROM `Products` WHERE `productID` = {id};"
    result = execute_query(db_connection, query).fetchall()
    return render_template('updateproduct.html', product = result)


@app.route('/updatedproduct/<int:id>', methods=['POST', 'GET'])
def update_product_process(id):
    try:
        db_connection = connect_to_database()
        product_name = request.form['product_name']
        product_inventory = request.form['product_inventory']
        product_price = request.form['product_price']
        product_description = request.form['product_description']
        # category_id = request.form['category_id']

        check_null = [product_name, product_inventory, product_price]
        for i in check_null:
            if not i:
                raise Exception

        query = f"UPDATE `Products` SET `productName` = '{product_name}', `productInventory` = {product_inventory}, `productPrice` = {product_price}, `productDescription` = '{product_description}' WHERE productID = {id};"
        execute_query(db_connection, query)

        """if category_id

        # Update Product Category if applicable
        if category_id:
            query = "UPDATE `ProductsCategories` SET `productID` = {id}, `categoryID` = {category_id} WHERE `productID` = {id}"
            execute_query(db_connection, query)"""

        return redirect('/products')
    except:
        return "You have entered an invalid value. Please make sure all fields are filled out properly."



"""
CATEGORIES
"""

@app.route('/categories')
def categories():
    db_connection = connect_to_database()

    query = "SELECT * FROM `Categories`;"
    result = execute_query(db_connection, query).fetchall()
    return render_template('categories.html', categories = result)


@app.route('/addcategory', methods=['POST'])
def add_category():
    db_connection = connect_to_database()

    category_name = request.form['category_name'] or None
    category_description = request.form['category_description'] or None
    
    try:
        query = "INSERT INTO `Categories` (`categoryName`, `categoryDescription`) VALUES (%s, %s)"
        data = (category_name, category_description)
        execute_query(db_connection, query, data)
    
        return redirect('/categories')
    
    except:
        return "There was an issue adding the Category. Please make sure text fields are not empty."


@app.route('/searchcategories', methods=['POST'])
def search_categories():
    db_connection = connect_to_database()

    category_name = request.form['category_name']
    category_description = request.form['category_description']
    try:
        query = f"""SELECT * FROM `Categories` 
        WHERE (`categoryName` = '{category_name}' OR '{category_name}' = '') 
        AND (`categoryDescription` = '{category_description}' OR '{category_description}' = '');"""

        result = execute_query(db_connection, query).fetchall()
        return render_template('categories.html', categories = result)
    
    except:
        return "There was an issue searching Categories."


@app.route('/deletecategory/<int:id>')
def delete_category(id):
    db_connection = connect_to_database()

    try:
        query = f"DELETE FROM `Categories` WHERE `categoryID` = {id};"
        execute_query(db_connection, query)
        return redirect('/categories')
    except:
        return "There was an error deleting this Category."


@app.route('/updatecategory/<int:id>', methods=['POST', 'GET'])
def update_category(id):
    db_connection = connect_to_database()
    query = f"SELECT * FROM `Categories` WHERE `categoryID` = {id};"
    result = execute_query(db_connection, query).fetchall()

    return render_template('updatecategory.html', category = result)


@app.route('/updatedcategory/<int:id>', methods=['POST', 'GET'])
def update_category_process(id):
    try:
        db_connection = connect_to_database()
        category_name = request.form['category_name']
        category_description = request.form['category_description']

        if not category_name:
            raise Exception
        
        query = f"UPDATE Categories SET categoryName = '{category_name}', categoryDescription = '{category_description}' WHERE categoryID = {id};"
        execute_query(db_connection, query)
        return redirect('/categories')
    except:
        return "You have entered an invalid value. Please make sure all fields are filled out properly."



"""
PRODUCTSCATEGORIES
"""

@app.route('/productscategories')
def products_categories():
    db_connection = connect_to_database()

    query = "SELECT * FROM `ProductsCategories`;"
    result = execute_query(db_connection, query).fetchall()

    # queries and results for adding new productcategory by name in drop down list
    products_query = "SELECT * FROM `Products`;"
    products_result = execute_query(db_connection, products_query)
    categories_query = "SELECT * FROM `Categories`;"
    categories_result = execute_query(db_connection, categories_query)

    return render_template('productscategories.html', products_categories = result, products = products_result, categories = categories_result)


@app.route('/addproductcategory', methods=['POST'])
def add_product_category():
    db_connection = connect_to_database()

    product_id = request.form['product'] or None
    category_id = request.form['category'] or None

    try:
        query = "INSERT INTO `ProductsCategories` (`productID`, `categoryID`) VALUES (%s, %s)"
        data = (product_id, category_id)
        execute_query(db_connection, query, data)

        return redirect('/productscategories')
    
    except:
        return "There was an issue adding the ProductCategory. Please make sure fields are not empty."


@app.route('/searchproductscategories', methods=['POST'])
def search_products_categories():
    db_connection = connect_to_database()

    product_id = request.form['product']
    category_id = request.form['category']

    try:
        query = f"""SELECT * FROM `ProductsCategories` 
        WHERE (`productID` = '{product_id}' OR '{product_id}' = '') 
        AND (`categoryID` = '{category_id}' OR '{category_id}' = '');"""

        result = execute_query(db_connection, query).fetchall()
        
        # queries and results for adding new productcategory by name in drop down list
        products_query = "SELECT * FROM `Products`;"
        products_result = execute_query(db_connection, products_query)
        categories_query = "SELECT * FROM `Categories`;"
        categories_result = execute_query(db_connection, categories_query)

        return render_template('productscategories.html', products_categories = result, products = products_result, categories = categories_result)
    
    except:
        return "There was an issue searching ProductsCategories."


@app.route('/deleteproductcategory')
def delete_product_category():
    db_connection = connect_to_database()

    try:
        product_id = request.args.get('productID', None)
        category_id = request.args.get('categoryID', None)

        query = f"DELETE FROM `ProductsCategories` WHERE `productID` = {product_id} AND `categoryID` = {category_id};"
        execute_query(db_connection, query)
        
        return redirect('/productscategories')
    except:
        return "There was an error deleting this Category."


@app.route('/updateproductcategory/<string:id_string>', methods=['POST', 'GET'])
def update_product_category(id_string):
    db_connection = connect_to_database()
    id_string_split = id_string.split('-', 1)
    product_id = int(id_string_split[0])
    category_id = int(id_string_split[1])
    query = f"SELECT * FROM `ProductsCategories` WHERE `productID` = {product_id} AND `categoryID` = {category_id};"
    result = execute_query(db_connection, query).fetchall()

    products_query = "SELECT * FROM `Products`;"
    products_result = execute_query(db_connection, products_query)
    categories_query = "SELECT * FROM `Categories`;"
    categories_result = execute_query(db_connection, categories_query)

    return render_template('updateproductcategory.html', product_category = result, products = products_result, categories = categories_result)


@app.route('/updatedproductcategory/<string:id_string>', methods=['POST', 'GET'])
def update_productCategory_process(id_string):
    try:
        db_connection = connect_to_database()
        id_string_split = id_string.split('-', 1)
        product_id = int(id_string_split[0])
        category_id = int(id_string_split[1])
        product_id_new = request.form['product']
        category_id_new = request.form['category']

        query = f"UPDATE ProductsCategories SET productID = {product_id_new}, categoryID = {category_id_new} WHERE productID = {product_id} AND categoryID = {category_id};"
        execute_query(db_connection, query)
        return redirect('/productscategories')
    except:
        return "You have entered an invalid value. Please make sure all fields are filled out properly."


if __name__ == "__main__":
    app.run(debug=True)