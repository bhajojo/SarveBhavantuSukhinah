from flask import Flask, render_template, request
from flask_mail import Mail

from flask_sqlalchemy import SQLAlchemy

# from flask_user import login_required, UserMixin, SQLAlchemyAdapter, UserManager
from flask_user import SQLAlchemyAdapter, login_required, UserMixin, UserManager

# import flask_wtf
from sqlalchemy import true, false

app = Flask (__name__)

app.config['SECRET_KEY'] = 'a8b84f7b63d64fb2a6e0161caabc4673'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///samlple.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CSRF_ENABLED'] = True;
app.config['USER_ENABLED_EMAIL'] = False;

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'joshibharat@live.com'
app.config['MAIL_PASSWORD'] = 'Stuti@1987'
app.config['MAIL_USE_TLS'] = False,
app.config['MAIL_USE_SSL'] = True


mail = Mail (app)

db = SQLAlchemy (app)


class User (db.Model, UserMixin):
    id = db.Column (db.Integer, primary_key=True)
    username = db.Column (db.String (80), nullable=False)
    password = db.Column (db.Integer, nullable=False)
    active = db.Column (db.Boolean, nullable=False)
    email = db.Column (db.String, nullable=False)


db_adaptor = SQLAlchemyAdapter (db, User)
user_manager = UserManager (db_adaptor, app)


@app.route ('/')
def home():
    return render_template ("index.html")


@app.route ('/templates/profile')
@login_required
def index_1():
    return '<h1> This is protected profile Page</h1>'



class DeviceData (db.Model):
        id = db.Column (db.Integer, primary_key=True)
        D_Name = db.Column (db.String (80))
        Quantity = db.Column (db.Integer)
        Price = db.Column (db.String (80))
        Deposit = db.Column (db.String (80))
        Location = db.Column (db.String (80))
        Description = db.Column (db.String (80))


@app.route("/EquipmentList", methods=["GET", "POST"])
def AddDeviceDB():
    if request.method == "POST":
        D_Name = request.form.get('DeviceName')
        Quantity=request.form.get ('Quantity')
        Price=request.form.get ('Price')
        Deposit=request.form.get ('Deposit')
        Location=request.form.get ('Location')
        Description=request.form.get ('Description')

        deviceList = DeviceData(DeviceName=D_Name,
                                    quantity=Quantity,
                                    Price=Price,
                                    Deposit=Deposit,
                                    Location=Location,
                                    Description=Description
                                    )
        db.session.add(deviceList)
        db.session.commit()

    #   return redirect (url_for('static', filename='home.html'))
    return render_template ("Add_Device.html")


if __name__ == '__main__':
    app.run (debug=True)
