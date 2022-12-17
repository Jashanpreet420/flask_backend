from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///final2.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
global login_ornot
login_ornot=False
current_date=date.today()
hour_and_minute = datetime.now().strftime("%H:%M")

class final2(db.Model):
     Sno= db.Column(db.Integer, primary_key=True)
     VehicleNumber=db.Column(db.String(20))
     DateofTable=db.Column(db.Date, nullable=True)
     Entry=db.Column(db.String(10), nullable=True)
     Exit=db.Column(db.String(10), nullable=True)
     Authorised=db.Column(db.String(5), default="Yes")

     def __repr__(self) -> str:
         return f"{self.Sno} - {self.VehicleNumber} - {self.Entry} - {self.Exit} - {self.Authorised}"

class master1(db.Model):
     userid= db.Column(db.Integer, primary_key=True)
     UserName=db.Column(db.String(30), unique=False)
     IdNumber=db.Column(db.Integer)
     VehicleNumber=db.Column(db.String(25), unique=True)
     PhoneNumber=db.Column(db.Integer)
     Email=db.Column(db.String(30))
     

     def __repr__(self) -> str:
         return f"{self.userid} - {self.UserName} - {self.IdNumber} - {self.VehicleNumber} - {self.PhoneNumber} - {self.Email}"


@app.route('/home')
def showit():
    if login_ornot is False:
        return render_template('login.html')
    return render_template('admin.html')

@app.route('/view')
def view_default():
    if login_ornot is False:
        return render_template('login.html')
    return render_template('view.html')


@app.route('/insert')
def showinsert():
    if login_ornot is False:
        return render_template('login.html')
    return render_template('insert.html')

@app.route('/home', methods=['GET', 'POST'])
def showdetails():
    if login_ornot is False:
        return render_template('login.html')
    if request.method == 'POST':
        idsearch= request.form.get('show_results')
        search = final2.query.all()
    return render_template('admin.html', showSearch=search)


@app.route('/insert', methods=['GET', 'POST'])    
def MasterEntry():
    if login_ornot is False:
        return render_template('login.html')
    if request.method=='POST':
        Name= request.form['UserName']
        Id= request.form['IdNum']
        Number= request.form['vehicle']
        phone= request.form['phone']
        email= request.form['Email']
        new_record=master1(UserName=Name, IdNumber=Id, VehicleNumber=Number,PhoneNumber=phone, Email=email)       #entry detail to db
        db.session.add(new_record)
        db.session.commit()
    allRecords= master1.query.all()
    return render_template('insert.html', masterrec=allRecords)

def automated_Entry():
    if request.method=='POST':
        Number= request.form['vehicle']
        datenow=current_date
        entry= hour_and_minute
        SnoOfexit = exit_or_not(Number)
        auth= findIt(Number)                                                                                #authorised or not
        if SnoOfexit is not None:
            changeit= final2.query.filter_by(Sno= SnoOfexit).first()
            changeit.Exit=hour_and_minute
            db.session.commit()
        else:  
            new_record=final2(VehicleNumber=Number, DateofTable=datenow, Entry=entry, Authorised= auth)       #entry detail to db
            db.session.add(new_record)
            db.session.commit()
        
    temprecords= final2.query.all()
    return render_template('admin.html', allRecords=temprecords)

def exit_or_not(num):
    first_row= final2.query.filter_by(VehicleNumber=num, Exit=None).first()
    if first_row is None:
        return None
    elif first_row.Exit is None and first_row.Entry is not None:
        return first_row.Sno
    return None

def findIt(num):
    exist = master1.query.filter_by(VehicleNumber=num).all()
    if  len(exist):
        return "Yes"   
    return "No"

@app.route('/view', methods=['GET', 'POST'])
def view_all():
    if login_ornot is False:
        return render_template('login.html')
    if request.method == 'POST':
        idsearch= request.form['IdNum']
        idsearch=idsearch.upper()
        search = master1.query.filter_by(VehicleNumber=idsearch).all()
    return render_template('view.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'Jashandeep01' or request.form['password'] != 'openocula':
            error = 'Invalid Credentials. Please try again.'
        else:
            global login_ornot
            login_ornot= True
            return render_template('admin.html')
    return render_template('login.html', error=error)

if __name__ == "__main__":
    app.run(debug=True)

