from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import timedelta
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kiyo@localhost/Formula One'
db = SQLAlchemy(app)

class Circuit(db.Model):
    __tablename__ = 'circuits'
    circuitid = db.Column(db.Integer, primary_key=True)
    circuitname = db.Column(db.String(40))
    circuitlocation = db.Column(db.String(40))
    circuitcountry = db.Column(db.String(40))
    circuitnationality = db.Column(db.String(40))

    def __init__(self, circuitname, circuitlocation, circuitcountry, circuitnationality):
        self.circuitname = circuitname
        self.circuitlocation = circuitlocation
        self.circuitcountry = circuitcountry
        self.circuitnationality = circuitnationality

@app.route('/')
def index():
    return render_template('index.html')

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, timedelta):
            # Custom handling for timedelta to return total seconds
            return str(obj.total_seconds())
        # Other non-serializable types could be added here
        return super(CustomJSONEncoder, self).default(obj)

app.json_encoder = CustomJSONEncoder

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['circuitname']
    location = request.form['circuitlocation']
    country = request.form['circuitcountry']
    nationality = request.form['circuitnationality']

    circuit = Circuit(name, location, country, nationality)
    db.session.add(circuit)
    db.session.commit()

    return jsonify(message=f"New circuit '{name}' is inserted successfully!!")

@app.route('/table/<table_name>')
def show_table(table_name):
    # Ensure the table name is safe to include in a query
    if table_name not in ['circuits', 'races', 'driver', 'constructors', 'pitstop', 'laptimes', 'results', 'constructorsstandings', 'constructorsresults', 'driverstandings']:
        return jsonify({'error': 'Invalid table name'}), 400
    query = text(f"SELECT * FROM {table_name}")
    data = db.session.execute(query).fetchall()
    # Properly convert data to a list of dictionaries
    result = [row._asdict() for row in data]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
