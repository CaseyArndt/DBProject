from logging import exception
import re
from flask import Flask, render_template, request, redirect
from db import *
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

@app.route('/customers', methods=['POST', 'GET'])
def customers():
    db_connection = connect_to_database()
    query = "SELECT * FROM `Customers`;"
    result = execute_query(db_connection, query).fetchall()
    return render_template('customers.html', customers = result)

@app.route('/addcustomer', methods=['POST','GET'])
def add_customer():
    db_connection = connect_to_database()
    
    if request.method == 'POST':
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone_number = request.form['phone_number']
            street_address = request.form['street_address']
            city = request.form['city']
            state = request.form['state']
            zip_code = request.form['zip_code']
            check_null = [first_name, last_name, email, phone_number, street_address, city, state, zip_code]
            for i in check_null:
                if not i:
                    raise Exception

            query = "INSERT INTO `Customers` (`firstName`, `lastName`, `email`, `phoneNumber`, `streetAddress`, `city`, `state`, `zipCode`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            data = (first_name, last_name, email, phone_number, street_address, city, state, zip_code)
            execute_query(db_connection, query, data)

            return redirect('/customers')

        except:
            return "There was an issue adding the Customer. Please make sure text fields are not empty."

@app.route('/searchcustomer', methods=['POST','GET'])
def search_customer():
    db_connection = connect_to_database()
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone_number = request.form['phone_number']
    street_address = request.form['street_address']
    city = request.form['city']
    state = request.form['state']
    zip_code = request.form['zip_code']
    query = f"SELECT * FROM `Customers` WHERE (`firstName` = '{first_name}' OR '{first_name}' = '') AND (`lastName` = '{last_name}' OR '{last_name}' = '') AND (`email` = '{email}' OR '{email}' = '') AND (`phoneNumber` = '{phone_number}' OR '{phone_number}' = '') AND (`streetAddress` = '{street_address}' OR '{street_address}' = '') AND (`city` = '{city}' OR '{city}' = '') AND (`state` = '{state}' OR '{state}' = '') AND (`zipCode` = '{zip_code}' OR '{zip_code}' = '');"
    result = execute_query(db_connection, query).fetchall()
    return render_template('searchcustomer.html', customers = result)


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

@app.route('/orders', methods=['POST', 'GET'])
def orders():
    db_connection = connect_to_database()

    if request.method == 'POST':
        try:
            customer_id = request.form['customer']
            total_price = request.form['total_price']
            order_date = request.form['order_date']
            order_comments = request.form['order_comments']
            if customer_id == "":
                customer_id = None
            check_null = [total_price, order_date]
            for i in check_null:
                if not i:
                    raise Exception
            date_format = "%Y-%m-%d"
            try:
                datetime.datetime.strptime(order_date, date_format)
            except:
                raise Exception
            query = "INSERT INTO `Orders` (`customerID`, `totalPrice`, `orderDate`, `orderComments`) VALUES (%s, %s, %s, %s)"
            data = (customer_id, total_price, order_date, order_comments)
            execute_query(db_connection, query, data)
        
            return redirect('/orders')

        except:
            return "There was an issue adding the Order. Please make sure all fields are filled out properly."

    else:
        query = "SELECT * FROM `Orders`;"
        result = execute_query(db_connection, query).fetchall()

        customers_query = "SELECT `customerID`, `firstName`, `lastName`, `email` FROM `Customers`;"
        customers_result = execute_query(db_connection, customers_query).fetchall()
        return render_template('orders.html', orders = result, customers = customers_result)


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
        order_date = request.form['order_date']
        # date validation from https://www.kite.com/python/answers/how-to-validate-a-date-string-format-in-python
        date_format = "%Y-%m-%d"
        try:
            datetime.datetime.strptime(order_date, date_format)
        except:
            raise Exception
        order_comments = request.form['order_comments']
        query = f"UPDATE `Orders` SET `customerID` = {customer_id}, `totalPrice` = {total_price}, `orderDate` = '{order_date}', `orderComments` = '{order_comments}' WHERE `orderID` = {id};"
        execute_query(db_connection, query)
        return redirect('/orders')
    except:
        return "You have entered an invalid value. Please make sure all fields are filled out properly."


"""
ORDER ITEMS
"""

@app.route('/orderitems', methods=['POST', 'GET'])
def order_items():
    db_connection = connect_to_database()

    if request.method == 'POST':
        try:
            order_id = request.form['order']
            product_id = request.form['product']
            order_item_quantity = request.form['order_item_quantity']
            order_item_price = request.form['order_item_price']

            query = "INSERT INTO `OrderItems` (`orderID`, `productID`, `orderItemQuantity`, `orderItemPrice`) VALUES (%s, %s, %s, %s)"
            data = (order_id, product_id, order_item_quantity, order_item_price)
            execute_query(db_connection, query, data)
        
            return redirect('/orderitems')

        except:
            return "There was an issue adding the Order Item."

    else:
        query = "SELECT * FROM `OrderItems`;"
        result = execute_query(db_connection, query).fetchall()

        # queries for Products, Orders, and Customers when adding new OrderItem
        products_query = "SELECT `productID`, `productName` FROM `Products`;"
        products_result = execute_query(db_connection, products_query).fetchall()

        orders_query = "SELECT `orderID` FROM `Orders`;"
        orders_result = execute_query(db_connection, orders_query).fetchall()

        return render_template('orderitems.html', order_items = result, products = products_result, orders = orders_result)


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

@app.route('/shipments', methods=['POST', 'GET'])
def shipments():
    db_connection = connect_to_database()

    if request.method == 'POST':
        try:
            order_id = request.form['order']
            tracking_number = request.form['tracking_number']
            date_shipped = request.form['date_shipped']
            date_delivered = request.form['date_delivered']
            date_format = "%Y-%m-%d"
            try:
                datetime.datetime.strptime(date_shipped, date_format)
            except:
                raise Exception

            try:
                if date_delivered == "":
                    pass
                else:
                    datetime.datetime.strptime(date_delivered, date_format)
            except:
                raise Exception

            check_null = [order_id, tracking_number, date_shipped]
            for i in check_null:
                if not i:
                    raise Exception

            query = "INSERT INTO `Shipments` (`orderID`, `trackingNumber`, `dateShipped`, `dateDelivered`) VALUES (%s, %s, %s, %s);"
            data = (order_id, tracking_number, date_shipped, date_delivered)
            execute_query(db_connection, query, data)
        
            return redirect('/shipments')

        except:
            return "There was an issue adding the Shipment."

    else:
        query = "SELECT * FROM `Shipments`;"
        result = execute_query(db_connection, query).fetchall()

        orders_query = "SELECT `orderID` FROM `Orders`;"
        orders_result = execute_query(db_connection, orders_query).fetchall()
        return render_template('shipments.html', shipments = result, orders = orders_result)


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
        order_id = request.form['order']
        tracking_number = request.form['tracking_number']
        date_shipped = request.form['date_shipped']
        date_delivered = request.form['date_delivered']
        # date validation from https://www.kite.com/python/answers/how-to-validate-a-date-string-format-in-python
        date_format = "%Y-%m-%d"
        try:
            datetime.datetime.strptime(date_shipped, date_format)
        except:
            raise Exception

        try:
            if date_delivered == "None":
                pass
            else:
                datetime.datetime.strptime(date_delivered, date_format)
        except:
            raise Exception

        check_null = [order_id, tracking_number, date_shipped]
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

@app.route('/products', methods=['POST', 'GET'])
def products():
    db_connection = connect_to_database()

    if request.method == 'POST':
        try:
            product_name = request.form['product_name']
            product_inventory = request.form['product_inventory']
            product_price = request.form['product_price']
            product_description = request.form['product_description']
            category_id = request.form['categories']

            check_null = [product_name, product_inventory, product_price]
            for i in check_null:
                if not i:
                    raise Exception

            query = "INSERT INTO `Products` (`productName`, `productInventory`, `productPrice`, `productDescription`) VALUES (%s, %s, %s, %s)"
            data = (product_name, product_inventory, product_price, product_description)
            cursor = execute_query(db_connection, query, data)

            # Add Product to ProductsCategories if Category is specified
            if category_id and category_id != "NULL":
                product_id = cursor.lastrowid
                query = "INSERT INTO `ProductsCategories` (`productID`, `categoryID`) VALUES (%s, %s)"
                data = (product_id, category_id)
                execute_query(db_connection, query, data)
        
            return redirect('/products')

        except:
            return "There was an issue adding the Product."

    else:
        query = "SELECT * FROM `Products`;"
        result = execute_query(db_connection, query).fetchall()

        categories_query = "SELECT `categoryID`, `categoryName` FROM `Categories`;"
        categories_result = execute_query(db_connection, categories_query).fetchall()
        return render_template('products.html', products = result, categories = categories_result)
        


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

@app.route('/categories', methods=['POST', 'GET'])
def categories():
    db_connection = connect_to_database()

    if request.method == 'POST':
        try:
            category_name = request.form['category_name']
            category_description = request.form['category_description']

            if not category_name:
                raise Exception

            query = "INSERT INTO `Categories` (`categoryName`, `categoryDescription`) VALUES (%s, %s)"
            data = (category_name, category_description)
            execute_query(db_connection, query, data)
            
        
            return redirect('/categories')

        except:
            return "There was an issue adding the Category."

    else:
        query = "SELECT * FROM `Categories`;"
        result = execute_query(db_connection, query).fetchall()
        return render_template('categories.html', categories = result)


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

@app.route('/productscategories', methods=['POST', 'GET'])
def products_categories():
    db_connection = connect_to_database()

    if request.method == 'POST':
        try:
            product_id = request.form['product']
            category_id = request.form['category']
            
            query = "INSERT INTO `ProductsCategories` (`productID`, `categoryID`) VALUES (%s, %s)"
            data = (product_id, category_id)
            execute_query(db_connection, query, data)
        
            return redirect('/productscategories')

        except:
            return "There was an issue adding the ProductCategory."

    else:
        query = "SELECT * FROM `ProductsCategories`;"
        result = execute_query(db_connection, query).fetchall()

        # queries and results for adding new productcategory by name in drop down list
        products_query = "SELECT * FROM `Products`;"
        products_result = execute_query(db_connection, products_query)
        categories_query = "SELECT * FROM `Categories`;"
        categories_result = execute_query(db_connection, categories_query)

        return render_template('productscategories.html', products_categories = result, products = products_result, categories = categories_result)

@app.route('/deleteproductcategory/<string:id_string>', methods=['GET'])
def delete_product_category(id_string):
    db_connection = connect_to_database()
    try:
        id_string_split = id_string.split('-', 1)
        product_id = int(id_string_split[0])
        category_id = int(id_string_split[1])
        query = f"DELETE FROM `ProductsCategories` WHERE `categoryID` = {category_id} AND `productID` = {product_id};"
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