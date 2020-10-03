
import sqlite3 as sql

from flask import Flask, render_template
from flask import redirect, url_for, session, request, g
from flask_sqlalchemy import SQLAlchemy
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf import FlaskForm

import wtforms
from flask_wtf import Form

# from flask_user import roles_required
from wtforms import validators, StringField, TextAreaField, SelectField, SelectMultipleField

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a8b84f7b63d64fb2a6e0161caabc4673'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///samlple.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =True

db = SQLAlchemy(app)


class RegistrationData(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    Patient_Name = db.Column(db.String(80))
    Patient_Age = db.Column(db.Integer)
    email = db.Column(db.String(80))
    Doctor_Name= db.Column(db.String(80))
    PhoneNumber=db.Column(db.String(80))
    Equipment=db.Column(db.String(80))
    Deposit= db.Column(db.Integer)
    Disease= db.Column(db.String(80))
    Issue_Date= db.Column(db.String(80))
    Return_Date= db.Column(db.String(80))
    Address = db.Column (db.String (80))

    def __init__(self,
                 Patient_Name,
                 Patient_Age,
                 email,
                 Doctor_Name,
                 PhoneNumber,
                 Address,
                 Equipment,
                 Deposit,
                 Disease,
                 Issue_Date,
                 Return_Date,
                 ):
        self.Patient_Name = Patient_Name
        self.Patient_Age = Patient_Age
        self.email = email
        self.Doctor_Name = Doctor_Name
        self.PhoneNumber = PhoneNumber
        self.Equipment = Equipment
        self.Deposit = Deposit
        self.Disease = Disease
        self.Issue_Date = Issue_Date
        self.Return_Date = Return_Date
        self.Address = Address


class DeviceData (db.Model):
        id = db.Column (db.Integer, primary_key=True)
        DeviceName = db.Column (db.String (80))
        quantity = db.Column (db.Integer)
        Price = db.Column (db.String (80))
        Deposit = db.Column (db.String (80))
        Location = db.Column (db.String (80))
        description = db.Column (db.String (80))

        def __repr__(self):
             return self.DeviceName

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/template/device')
def devices():
    return render_template("device.html")

@app.route('/templates/list')
def devices1():
    return render_template("list.html")

@app.route('/templates/home')
def about():
    name= "Rugna Sahayata Kendra"
    return render_template("about.html", name=name)

@app.route('/templates/Registration', methods=['GET', 'POST'])
def Registration():

    form = ChoiceForm ()
    form.opts.query = DeviceData.query.filter (DeviceData.id >= "1")

    # if form.validate_on_submit ():
    #     return '<html><h1>{}</h1></html>'.format (form.opts.gettext (""))

    return render_template('RegistrationForm.html', form=form)

@app.route('/templates/Add_Device')
def AddDevice():
    name= "Rugna Sahayata Kendra"
    return render_template("Add_Device.html", name=name)

@app.route ('/templates/table')
def AllocationList():
    con = sql.connect ("samlple.db")
    con.row_factory = sql.Row

    cur = con.cursor ()
    cur.execute ("select * from registration_data")

    rows = cur.fetchall ();
    return render_template ("table.html", rows=rows)


@app.route ('/templates/EquipmentList')
def EquipmentList():
    con = sql.connect ("samlple.db")
    con.row_factory = sql.Row

    cur = con.cursor ()
    cur.execute ("select * from device_data")

    rows = cur.fetchall ();
    return render_template ("EquipmentList.html", rows=rows)

@app.route ('/templates/contact')
def ContactsPage():
    return render_template ("contact.html")


@app.route("/home", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        P_Name = request.form.get('PatientName')
        P_AGE=request.form.get ('Age')
        P_Email=request.form.get ('email')
        D_Name=request.form.get ('DoctorName')
        Phone_No=request.form.get ('phoneNumber')
        equipment = str (request.form.getlist ('mymultiselect'))
        deposit=request.form.get ('Deposit')
        disease=request.form.get('Disease')
        I_Date=request.form.get ('IssueDate')
        R_Date=request.form.get ('ReturnDate')
        address = request.form.get('Address')

        register = RegistrationData(Patient_Name=P_Name,
                                    Patient_Age=P_AGE,
                                    email=P_Email,
                                    Doctor_Name=D_Name,
                                    PhoneNumber=Phone_No,
                                    Equipment=equipment,
                                    Deposit=deposit,
                                    Disease=disease,
                                    Issue_Date=I_Date,
                                    Return_Date=R_Date,
                                    Address=address
                                    )
        db.session.add (register)
        db.session.commit()

    return render_template ("home.html")


@app.route("/index", methods=["GET", "POST"])
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
                                    description=Description
                                    )
        db.session.add(deviceList)
        db.session.commit()

    return render_template ("index.html")



def choice_query():
    return DeviceData.query

class ChoiceForm(FlaskForm):
    opts = QuerySelectField(query_factory=choice_query, allow_blank=True, get_label='DeviceName')

if __name__=='__main__':

    app.run(debug=True)