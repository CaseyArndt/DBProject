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
    def __init__(self, category_name: str, category_description: str = ""):
        self.category_id = next(self.new_id)
        self.category_name = category_name
        self.category_description = category_description



customer_list = [Customer("Sterling", "Archer", "duchess@isis.gov", "212-220-5240", "2 N. Trenton Street", "New York", "New York", "10016"),
                 Customer("Cyril", "Figgis", "chetmanley@isis.gov", "718-380-1669", "8248 S. Cobblestone St.", "Staten Island", "New York", "10312"),
                 Customer("Lana", "Kane", "shehulk@isis.gov", "646-391-2933", "70 North Pumpkin Hill Street", "Bronx", "New York", "10457")]
order_list = [Order(0, 101.20, "10/10/2019"),
              Order(0, 27.34, "02/24/2021"),
              Order(2, 30.92, "04/26/2021")]
order_item_list = [OrderItem(0, 0, 1, 7.59),
                   OrderItem(0, 2, 2, 21.79),
                   OrderItem(0, 1, 1, 27.34)]
shipment_list = [Shipment(0, "1Z12345E0205271688", "10/14/2019"),
                 Shipment(1, "1Z12345E6605272234", "02/26/2021"),
                 Shipment(2, "1Z12345E0305271640", "04/29/2021")]
product_list = [Product("", 50, 7.59),
                Product("", 99, 27.34),
                Product("", 0, 21.79)]
category_list = [Category("Flower Seeds"),
                 Category("Flower Seedlings"),
                 Category("Potting Soil")]