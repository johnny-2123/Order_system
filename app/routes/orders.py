from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from app.models import Table, Employee, Order, MenuItem, MenuItemType
from app.forms import TableAssignmentForm
from app import db
bp = Blueprint("orders", __name__, url_prefix="")


@bp.route("/")
@login_required
def index():
    taf = TableAssignmentForm()
    openTables = open_tables()
    servers = Employee.query.all()
    taf.tables.choices = [(t.id, f"Table {t.number}") for t in openTables]
    taf.servers.choices = [(s.id, s.name) for s in servers]

    return render_template('orders.html', title='Welcome to order up', taf=taf)


@bp.route("/assign", methods=['POST'])
@login_required
def assign():
    form = TableAssignmentForm()
    open_tables = open_tables()
    servers = Employee.query.all()
    form.tables.choices = [(t.id, f"Table {t.number}") for t in open_tables]
    form.servers.choices = [(s.id, {s.name}) for s in servers]

    if form.validate_on_submit():
        order = Order(
            employee_id=form.servers.data,
            table_id=form.tables.data,
            finished=False
        )
        db.session.add(order)
        db.session.commit()
    return redirect(url_for('.index'))


def open_tables():
    tables = Table.query.order_by(Table.number).all()
    open_orders = Order.query.filter(Order.finished == False)
    busy_table_ids = [order.table_id for order in open_orders]
    open_tables = [table for table in tables if table.id not in busy_table_ids]

    return open_tables
