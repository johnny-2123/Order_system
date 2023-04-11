from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Employee(db.Model, UserMixin):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employee_number = db.Column(db.Integer, nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)

    orders = db.relationship('Order', back_populates='employee')

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Menu(db.Model, UserMixin):
    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    items = db.relationship('MenuItem', back_populates='menu')


class MenuItem(db.Model, UserMixin):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)

    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=False)
    menu = db.relationship('Menu', back_populates='items')

    menu_type_id = db.Column(db.Integer, db.ForeignKey(
        'menu_item_types.id'), nullable=False)
    menu_type = db.relationship('MenuItemType', back_populates='items')

    # details = db.relationship(
    #     'OrderDetail', back_populates='menu_item', cascade='all, delete-orphan')

    order_details = db.relationship(
        'Order',
        secondary='order_details',
        back_populates='menu_items',
        cascade='all, delete'
    )


class MenuItemType(db.Model, UserMixin):
    __tablename__ = 'menu_item_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    items = db.relationship('MenuItem', back_populates='menu_type')


class Table(db.Model, UserMixin):
    __tablename__ = 'tables'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    capacity = db.Column(db.Integer, nullable=False)

    orders = db.relationship('Order', back_populates='table')


class Order(db.Model, UserMixin):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    finished = db.Column(db.Boolean, nullable=False)

    employee_id = db.Column(db.Integer, db.ForeignKey(
        'employees.id'), nullable=False)
    employee = db.relationship('Employee', back_populates='orders')

    table_id = db.Column(db.Integer, db.ForeignKey(
        'tables.id'), nullable=False)
    table = db.relationship('Table', back_populates='orders')

    # details = db.relationship(
    #     'OrderDetail', back_populates='order', cascade='all, delete-orphan')

    menu_items = db.relationship(
        'MenuItem',
        secondary='order_details',
        back_populates='order_details',
        cascade='all, delete'
    )

    @property
    def total(self):
        return sum([item.price for item in self.menu_items])


OrderDetails = db.Table(
    'order_details',
    db.Model.metadata,
    db.Column('orders', db.Integer, db.ForeignKey(
        'orders.id'), primary_key=True),
    db.Column('menu_items', db.Integer, db.ForeignKey(
        'menu_items.id'), primary_key=True)
)


# class OrderDetail(db.Model, UserMixin):
#     __tablename__ = "order_details"
#     id = db.Column(db.Integer, primary_key=True)

#     order_id = db.Column(db.Integer, db.ForeignKey(
#         'orders.id', ondelete='CASCADE'), nullable=False)
#     order = db.relationship('Order', back_populates='details')

#     menu_item_id = db.Column(db.Integer, db.ForeignKey(
#         'menu_items.id', ondelete='CASCADE'), nullable=False)
#     menu_item = db.relationship(
#         'MenuItem', back_populates='details', cascade='all, delete-orphan')
