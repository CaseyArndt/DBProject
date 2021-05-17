from flask import Flask, render_template, request, redirect
from db import *
from .. db_credentials import host, user, passwd, db
from db_connector import connect_to_database, execute_query

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

            customer = Customer(first_name, last_name, email, phone_number, street_address, city, state, zip_code) 

            customer_list.append(customer)
        
            return redirect('/customers')

        except:
            return "There was an issue adding the Customer."

    else:
        return render_template('customers.html', customer_list = customer_list)


@app.route('/deletecustomer/<int:id>')
def delete_customer(id):
    try:
        for customer in customer_list:
            if customer.customer_id == id:
                customer_list.remove(customer)
                return redirect('/customers')
    except:
        return "There was an error deleting this Customer."


@app.route('/updatecustomer/<int:id>', methods=['POST', 'GET'])
def update_customer(id):
    for customer in customer_list:
        if customer.customer_id == id:
            break

    if request.method == 'POST':
        try:
            customer.first_name = request.form['first_name']
            customer.last_name = request.form['last_name']
            customer.email = request.form['email']
            customer.phone_number = request.form['phone_number']
            customer.street_address = request.form['street_address']
            customer.city = request.form['city']
            customer.state = request.form['state']
            customer.zip_code = request.form['zip_code']
            return redirect('/customers')

        except:
            return "There was an error updating this Customer."

    else:
        return render_template('updatecustomer.html', customer = customer)


"""
ORDERS
"""

@app.route('/orders', methods=['POST', 'GET'])
def orders():
    if request.method == 'POST':
        try:
            customer_id = request.form['customer_id']
            total_price = request.form['total_price']
            order_date = request.form['order_date']
            order_comments = request.form['order_comments']

            order = Order(customer_id, total_price, order_date, order_comments) 

            order_list.append(order)
        
            return redirect('/orders')

        except:
            return "There was an issue adding the Order."

    else:
        return render_template('orders.html', order_list = order_list)


@app.route('/deleteorder/<int:id>')
def delete_order(id):
    try:
        for order in order_list:
            if order.order_id == id:
                order_list.remove(order)
                return redirect('/orders')
    except:
        return "There was an error deleting this Order."


@app.route('/updateorder/<int:id>', methods=['POST', 'GET'])
def update_order(id):
    for order in order_list:
        if order.order_id == id:
            break

    if request.method == 'POST':
        try:
            order.customer_id = request.form['customer_id']
            order.total_price = request.form['total_price']
            order.order_date = request.form['order_date']
            order.order_comments = request.form['order_comments']

            return redirect('/orders')

        except:
            return "There was an error updating this Order."

    else:
        return render_template('updateorder.html', order = order)


"""
ORDER ITEMS
"""

@app.route('/orderitems', methods=['POST', 'GET'])
def order_items():
    if request.method == 'POST':
        try:
            order_id = request.form['order_id']
            product_id = request.form['product_id']
            item_quantity= request.form['item_quantity']
            item_price = request.form['item_price']

            order_item = OrderItem(order_id, product_id, item_quantity, item_price) 

            order_item_list.append(order_item)
        
            return redirect('/orderitems')

        except:
            return "There was an issue adding the Order Item."

    else:
        return render_template('orderitems.html', order_item_list = order_item_list)


@app.route('/deleteorderitem/<int:id>')
def delete_order_item(id):
    try:
        for order_item in order_item_list:
            if order_item.item_id == id:
                order_item_list.remove(order_item)
                return redirect('/orderitems')
    except:
        return "There was an error deleting this Order Item."


@app.route('/updateorderitem/<int:id>', methods=['POST', 'GET'])
def update_order_item(id):
    for order_item in order_item_list:
        if order_item.item_id == id:
            break

    if request.method == 'POST':
        try:
            order_item.order_id = request.form['order_id']
            order_item.product_id = request.form['product_id']
            order_item.item_quantity = request.form['item_quantity']
            order_item.item_price = request.form['item_price']

            return redirect('/orderitems')

        except:
            return "There was an error updating this Order Item."

    else:
        return render_template('updateorderitem.html', order_item = order_item)

"""
SHIPMENTS
"""

@app.route('/shipments', methods=['POST', 'GET'])
def shipments():
    if request.method == 'POST':
        try:
            order_id = request.form['order_id']
            tracking_number = request.form['tracking_number']
            date_shipped = request.form['date_shipped']

            shipment = Shipment(order_id, tracking_number, date_shipped) 

            shipment_list.append(shipment)
        
            return redirect('/shipments')

        except:
            return "There was an issue adding the Shipment."

    else:
        return render_template('shipments.html', shipment_list = shipment_list)


@app.route('/deleteshipment/<int:id>')
def delete_shipment(id):
    try:
        for shipment in shipment_list:
            if shipment.shipment_id == id:
                shipment_list.remove(shipment)
                return redirect('/shipments')
    except:
        return "There was an error deleting this Shipment."


@app.route('/updateshipment/<int:id>', methods=['POST', 'GET'])
def update_shipment(id):
    for shipment in shipment_list:
        if shipment.shipment_id == id:
            break

    if request.method == 'POST':
        try:
            shipment.order_id = request.form['order_id']
            shipment.tracking_number = request.form['tracking_number']
            shipment.date_shipped = request.form['date_shipped']

            return redirect('/shipments')

        except:
            return "There was an error updating this Shipment."

    else:
        return render_template('updateshipment.html', shipment = shipment)


"""
PRODUCTS
"""

@app.route('/products', methods=['POST', 'GET'])
def products():
    if request.method == 'POST':
        try:
            product_name = request.form['product_name']
            product_inventory = request.form['product_inventory']
            product_price = request.form['product_price']
            product_description = request.form['product_description']
            category_id = request.form['category_id']

            product = Product(product_name, product_inventory, product_price, product_description)
            product_list.append(product)

            product_category = ProductCategory(product.product_id, category_id)
            product_category_list.append(product_category)
        
            return redirect('/products')

        except:
            return "There was an issue adding the Product."

    else:
        return render_template('products.html', product_list = product_list)


@app.route('/deleteproduct/<int:id>')
def delete_product(id):
    try:
        for product in product_list:
            if product.product_id == id:
                product_list.remove(product)
                return redirect('/products')
    except:
        return "There was an error deleting this Product."


@app.route('/updateproduct/<int:id>', methods=['POST', 'GET'])
def update_product(id):
    for product in product_list:
        if product.product_id == id:
            break

    if request.method == 'POST':
        try:
            product.product_name = request.form['product_name']
            product.product_inventory = request.form['product_inventory']
            product.product_price = request.form['product_price']
            product.product_description = request.form['product_description']
            return redirect('/products')

        except:
            return "There was an error updating this Product."

    else:
        return render_template('updateproduct.html', product = product)


"""
CATEGORIES
"""

@app.route('/categories', methods=['POST', 'GET'])
def categories():
    if request.method == 'POST':
        try:
            category_name = request.form['category_name']
            category_description = request.form['category_description']

            category = Category(category_name, category_description)

            category_list.append(category)
        
            return redirect('/categories')

        except:
            return "There was an issue adding the Category."

    else:
        return render_template('categories.html', category_list = category_list)


@app.route('/deletecategory/<int:id>')
def delete_category(id):
    try:
        for category in category_list:
            if category.category_id == id:
                category_list.remove(category)
                return redirect('/categories')
    except:
        return "There was an error deleting this Category."


@app.route('/updatecategory/<int:id>', methods=['POST', 'GET'])
def update_category(id):
    for category in category_list:
        if category.category_id == id:
            break

    if request.method == 'POST':
        try:
            category.category_name = request.form['category_name']
            category.category_description = request.form['category_description']
            return redirect('/categories')

        except:
            return "There was an error updating this Category."

    else:
        return render_template('updatecategory.html', category = category)


"""
PRODUCTSCATEGORIES
"""

@app.route('/productscategories', methods=['POST', 'GET'])
def products_categories():
    if request.method == 'POST':
        try:
            product_id = request.form['product_id']
            category_id = request.form['category_id']
            print(product_id, category_id)
            product_category = ProductCategory(product_id, category_id)

            product_category_list.append(product_category)
        
            return redirect('/productscategories')

        except:
            return "There was an issue adding the ProductCategory."

    else:
        return render_template('productscategories.html', product_category_list = product_category_list)



@app.route('/deleteproductcategory/<int:id>')
def delete_product_category(id):
    try:
        for product_category in product_category_list:
            if product_category.id == id:
                product_category_list.remove(product_category)
                return redirect('/productscategories')
    except:
        return "There was an error deleting this ProductCategory."


@app.route('/updateproductcategory/<int:id>', methods=['POST', 'GET'])
def update_product_category(id):
    for product_category in product_category_list:
        if product_category.id == id:
            break

    if request.method == 'POST':
        try:
            product_category.product_id = request.form['product_id']
            product_category.category_id = request.form['category_id']
            return redirect('/productscategories')

        except:
            return "There was an error updating this ProductCategory."

    else:
        return render_template('updateproductcategory.html', product_category = product_category)


if __name__ == "__main__":
    app.run(debug=True)