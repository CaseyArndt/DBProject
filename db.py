#from flask_table import Table, Col
import itertools

"""
class CustomerTable(Table):
    first_name = Col("First Name")
    last_name = Col("Last Name")
    email = Col("Email")
    phone_number = Col("Phone Number")
    street_address = Col("Street Address")
    city = Col("City")
    state = Col("State")
    zip_code = Col("Zip Code")
    actions = Col("Actions")
"""


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


if __name__ == "__main__":
    Bob = Customer("Bob", "James", "bobjames@gmail.com", "16207943788", "1234 Generic Street", "Cityville", "Oregon", "66801")
    Bill = Customer("Bill", "James", "billjames@gmail.com", "16207943789", "1234 Generic Street", "Cityville", "Oregon", "66801")

    shipment_1 = Shipment(101, "1423432423XYZ", "01-01-2021")
    print(Bob.customer_id, Bill.customer_id, shipment_1.shipment_id)
