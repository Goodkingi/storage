import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, validators, SubmitField,PasswordField
from wtforms.validators import DataRequired


class DepartmentForm(FlaskForm):
    department_name = StringField("department name", validators=[DataRequired()])
    department_address = StringField("address", validators=[DataRequired()])
    submit = SubmitField('add department')


class StaffForm(FlaskForm):
    staff_department = StringField("department:", validators=[DataRequired()])
    staff_first_name = StringField("first name:", validators=[DataRequired()])
    staff_last_name = StringField("last name:", validators=[DataRequired()])
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password:", validators=[DataRequired()])
    submit = SubmitField("add user")


class ProductInventoryForm(FlaskForm):
    product_categorie=StringField("categorie: ",validators=[DataRequired()])
    product_name = StringField("name of product: ", validators=[DataRequired()])
    product_serial_number = StringField("serial number: ", validators=[DataRequired()])
    product_barcode = StringField("Barcode ", validators=[DataRequired()])
    product_quantity = StringField("Quantity: ", validators=[DataRequired()])
    received_date = StringField("received date: ", validators=[DataRequired()])
    product_details = StringField("product details: ", validators=[DataRequired()])
    product_status = StringField("Status: ", validators=[DataRequired()])
    product_brand = StringField("Brand: ", validators=[DataRequired()])
    product_condition = StringField("condition ", validators=[DataRequired()])
    product_department = StringField("Department ",validators=[DataRequired()])
    product_address= StringField("location/address ", validators=[DataRequired()])
    submit = SubmitField("save item")


class product_categoryForm(FlaskForm):
    product_id = StringField("id")
    category_id = StringField('id')


class StoreForm(FlaskForm):
    store_id = StringField("store id", validators=[DataRequired()])
    store_name = StringField('main store', validators=[DataRequired()])
    store_address = StringField('main store address', validators=[DataRequired()])

