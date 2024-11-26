from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///D:/projects/Python flask form/instance/Data.db" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Data(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(200), nullable=False)  
    name = db.Column(db.String(200), nullable=False)  
    email = db.Column(db.String(500), nullable=False) 
    data_created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return f"{self.data_created} - {self.name} - {self.email}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Insert new record into the database
        new_data = Data(name=name, email=email, password=password)
        db.session.add(new_data)
        db.session.commit()
        return redirect('/')

    all_data = Data.query.all()
    return render_template('index.html', all_data=all_data)

@app.route('/Delete/<int:sno>', methods=['GET', 'POST'])
def delete(sno):
    data = Data.query.filter_by(sno=sno).first()
    db.session.delete(data)
    db.session.commit()
    
    return redirect('/table')

@app.route('/table')
def table():
    all_data = Data.query.all()  
    return render_template('table.html', all_data=all_data)  

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
