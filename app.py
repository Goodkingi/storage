from flask import Flask, request, redirect, render_template, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from forms import *
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, PasswordField
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField

# from flask_mysqldb import MySQL
# import yaml

app = Flask(__name__)
app.config['SECRET_KEY'] = "ta-saf"

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///storage.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##tables in storage
# 1 Department
class DepartmentTable(db.Model):
    _tablename_="table_name"
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), nullable=False)
    department_address = db.Column(db.String(100), unique=True, nullable=False)

   #relation between store and department
    store_id = db.Column(db.Integer,db.ForeignKey("store_table.id"))
    store = relationship("StoreTable",back_populates='department')



# 2 staff
class StaffTable(UserMixin, db.Model):
    _tablename_="staff_table"
    id = db.Column(db.Integer, primary_key=True)
    staff_department = db.Column(db.String(100), nullable=False)
    staff_first_name = db.Column(db.String(100), nullable=False)
    staff_last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    # relationship between users and store
    store_id = db.Column(db.Integer, db.ForeignKey("store_table.id"))
    store = relationship("StoreTable", back_populates="staff")


# 3 productInventoryTable
class InventoryTable(db.Model):
    _tablename_="inventory_table"
    id = db.Column(db.Integer, primary_key=True)
    product_categorie = db.Column(db.String(100), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    product_barcode = db.Column(db.String(100), unique=True, nullable=False)
    product_serial_number = db.Column(db.Integer, unique=True, nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    received_date = db.Column(db.String(100), nullable=False)
    product_brand = db.Column(db.String(100), nullable=False)
    product_details = db.Column(db.String(100), nullable=True)
    product_condition = db.Column(db.String(100), nullable=False)
    product_status = db.Column(db.String(100), nullable=False)
    product_department = db.Column(db.String(100), nullable=False)
    product_address = db.Column(db.String(100), nullable=False)

    #relationship between store and product_inventory
    store_id =db.Column(db.Integer,db.ForeignKey("store_table.id"))
    store = relationship("StoreTable",back_populates="inventory")

# class product_categoryTable(db.Model):
#     product_id = db.Column(db.Integer,nullable=False)
#     category_id = db.Column(db.Integer,nullable=False)



class StoreTable(db.Model):
    _tablename_="store_table"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    store_name = db.Column(db.String(100), nullable=False)
    store_address = db.Column(db.String(100), unique=True, nullable=False)

    # relationship between user(staff) and store
    staff= relationship("StaffTable",back_populates="store")

    #relationship between store and inventory_table
    inventory= relationship("InventoryTable",back_populates="store")

    # relationship between store and department
    department = relationship("DepartmentTable",back_populates="store")



# with app.app_content():
db.create_all()


####################################################################authenticaton user
@app.route('/register', methods=["GET", "POST"])
def register():
    staffs = StaffForm()
    staffs_all_records = StaffTable.query.all()
    form = StaffForm()
    forms = StaffTable.query.all()
    if form.validate_on_submit():

        # If user's username already exists
        if StaffTable.query.filter_by(username=form.username.data).first():
            # Send flash messsage
            flash("You've already signed up with that username, log in instead!")
            # Redirect to /login route.
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = StaffTable(
            username=form.username.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        # This line will authenticate the user with Flask-Login
        login_user(new_user)
        return redirect(url_for("login"))

    return render_template("register.html", form=form, staff_data=staffs_all_records,
                           logged_in=current_user.is_authenticated)


################################### staff registration ##########################################
##########registration
@app.route('/staff', methods=['POST', 'GET'])
def staff():
    staffs = StaffForm()
    staffs_all_records = StaffTable.query.all()  # reading all data in table

    if request.method == "POST":
        if StaffTable.query.filter_by(username=request.form.get('username')).first():
            # if user is registered
            flash("this username is already registered, please login")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        add_staff = StaffTable(
            staff_department=request.form.get('staff_department'),
            staff_first_name=request.form.get('staff_first_name'),
            staff_last_name=request.form.get('staff_last_name'),
            username=request.form.get('username'),
            password=hash_and_salted_password
        )
        db.session.add(add_staff)
        db.session.commit()
        return redirect(url_for('staff'))
    return render_template('staff.html', form=staffs, staff_data=staffs_all_records,
                           logged_in=current_user.is_authenticated)


#################   login and authentication admin #############################

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(staff_id):
    return StaffTable.query.get(int(staff_id))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = StaffTable.query.filter_by(username=username).first()
        # Email doesn't exist
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        # Email exists and password correct
        else:
            login_user(user)
            return redirect(url_for('home'))

    return render_template("login.html")


##########USER LOGIN
#
# login_manager = LoginManager()
# login_manager.init_app(app)
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     return StaffTable.query.get(int(user_id))
#
#
# @app.route('/user_login', methods=["GET", "POST"])
# def user_login():
#     form = StaffForm()
#     if form.validate_on_submit():
#         username = form.username.data
#         password = form.password.data
#
#         user = StaffTable.query.filter_by(username=username).first()
#         # username doesn't exist
#         if not user:
#             flash("That username does not exist, please try again.")
#             return redirect(url_for('login'))
#         # Password incorrect
#
#         elif user and check_password_hash(user.password, password):
#             flash('Password incorrect, please try again.')
#             return redirect(url_for('login'))
#         else:
#
#             login_user(user)
#             return redirect(url_for('get_all_posts'))
#
#     return render_template("login.html", form=form)
# Everytime you call render_template(), you pass the current_user over to the template.
# current_user.is_authenticated will be True if they are logged in/authenticated after registering.
# You can check for this is header.html
@app.route('/')
def initial():
    return render_template('login.html')


@app.route('/home')
def home():
    ## when successful print loggedin user

    # reading all record from database
    all_records = InventoryTable.query.all()  # reading all data in table
    all_data = db.session.query(DepartmentTable).all()  # reading all data using sessions
    return render_template('index.html', department=all_data, inventory=all_records,
                           logged_in=current_user.is_authenticated, current_user=current_user)


@app.route('/base')
def base():
    return render_template('base.html')


@app.route('/department', methods=['POST', 'GET'])
def department():
    department_form = DepartmentForm()
    all_data = db.session.query(DepartmentTable).all()  # reading all data using sessions
    # adding departmnts
    if request.method == "POST":
        # CREATE RECORD in
        add_department = DepartmentTable(
            department_name=request.form["department_name"],
            department_address=request.form["department_address"]
        )
        db.session.add(add_department)
        db.session.commit()
        return redirect(url_for('department'))
    return render_template('department.html', form=department_form, department=all_data,
                           logged_in=current_user.is_authenticated, current_user=current_user)


@app.route('/inventory', methods=['POST', 'GET'])
def inventory():
    inventory_form = ProductInventoryForm()
    all_records = InventoryTable.query.all()  # reading all data in table

    if request.method == "POST":
        add_item = InventoryTable(
            product_categorie=request.form['product_categorie'],
            product_name=request.form['product_name'],
            product_barcode=request.form['product_barcode'],
            product_serial_number=request.form['product_serial_number'],
            product_quantity=request.form['product_quantity'],
            received_date=request.form['received_date'],
            product_brand=request.form['product_brand'],
            product_details=request.form['product_details'],
            product_condition=request.form['product_condition'],
            product_status=request.form['product_status'],
            product_department=request.form['product_department'],
            product_address=request.form['product_address']
        )
        db.session.add(add_item)
        db.session.commit()
        return redirect(url_for('inventory'))
    return render_template('inventory.html', form=inventory_form, inventory=all_records,
                           logged_in=current_user.is_authenticated, current_user=current_user)


@app.route('/store')
def store():
    inventory_form = ProductInventoryForm()
    all_records = InventoryTable.query.all()  # reading all data in table
    form = InventoryTable.query.all()
    return render_template('store.html', form=inventory_form, inventory=all_records,
                           logged_in=current_user.is_authenticated, current_user=current_user)


@app.route('/status')
def status():
    return render_template('status.html', logged_in=current_user.is_authenticated, current_user=current_user)


@app.route('/about')
def about():
    return render_template('about.html', logged_in=current_user.is_authenticated, current_user=current_user)


##################################################################################
###CRUD Operations on tables
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # CREATE RECORD in
        add_deparment = DepartmentTable(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(add_deparment)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html", current_user=current_user)


##edit
@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = ProductInventoryForm()
    item_id = request.args.get('id')
    item = InventoryTable.query.get(item_id)
    if form.validate_on_submit():
        item.categorie = form.product_categorie.data
        item.product_name = form.product_name.data
        item.serial_number =form.product_serial_number.data
        item.barcode = form.product_barcode.data
        item.quantity = form.product_quantity.data
        item.received_date = form.received_date.data
        item.product_details = form.product_details.data
        item.product_status = form.product_status.data
        item.product_brand = form.product_brand.data
        item.product_condition = form.product_condition.data
        item.product_department = form.product_department.data
        item.product_address = form.product_address.data
        return  redirect(url_for('inventory'))
    return render_template("edit.html", item=item,form=form, current_user=current_user)


@app.route('/main_store', methods=['GET', 'POST'])
def main_store():
    store_table = StoreTable()
    all_data = db.session.query(StoreTable).all()  # reading all data using sessions
    # adding main store
    if request.method == "POST":
        # CREATE RECORD in
        add_store = StoreTable(
            store_name=request.form["store_name"],
            store_address=request.form["store_address"]
        )
        db.session.add(add_store)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('index.html', form=all_data, logged_in=current_user.is_authenticated,
                           current_user=current_user)


### delete
@app.route('/delete')
def delete():
    item_id = request.args.get('id')

    # DELETE A RECORD BY ID
    item = InventoryTable.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('inventory'))


#main function for all crud opereations
@app.route('/crud')
def crud():
   pass

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('initial'))


@app.route('/home')
@login_required
def secrets():
    print(current_user.username)
    return render_template("index.html", name=current_user.username, logged_in=True, current_user=current_user)


if __name__ == "__main__":
    app.run(debug=True)
