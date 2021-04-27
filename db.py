#from flask_table import Table, Col
import itertools

class Customer(object):
    new_id = itertools.count()
    def __init__(self, first_name: str, last_name: str, email: str, phone_number: str, \
        street_address: str, city: str, state: str, zip_code: str):
        
        self.customer_id = next(self.new_id)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code


class Order(object):
    new_id = itertools.count()
    def __init__(self, customer_id: int, total_price: float, order_date: str, order_comments: str = ""):
        self.order_id = next(self.new_id)
        self.customer_id = customer_id
        self.total_price = total_price
        self.order_date = order_date
        self.order_comments = order_comments


class OrderItem(object):
    new_id = itertools.count()
    def __init__(self, order_id: int, product_id: int, item_quantity: int, item_price: float):
        self.item_id = next(self.new_id)
        self.order_id = order_id
        self.product_id = product_id
        self.item_quantity = item_quantity
        self.item_price = item_price


class Shipment(object):
    new_id = itertools.count()
    def __init__(self, order_id: int, tracking_number: str, date_shipped: str):
        self.shipment_id = next(self.new_id)
        self.order_id = order_id
        self.tracking_number = tracking_number
        self.date_shipped = date_shipped


class Product(object):
    new_id = itertools.count()
    def __init__(self, product_name: str, product_inventory: int, product_price: float, product_description: str = "",):
        self.product_id = next(self.new_id)
        self.product_name = product_name
        self.product_inventory = product_inventory
        self.product_price = product_price
        self.product_description = product_description


class Category(object):
    new_id = itertools.count()
    def __init__(self, category_name: str, category_description: str):
        self.category_id = next(self.new_id)
        self.category_name = category_name
        self.category_description = category_description

