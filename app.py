from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__, static_folder='static')

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client.tennis_courts
courts_collection = db.courts
reservations_collection = db.reservations

# Serve the front-end index.html
@app.route('/')
def index():
    return render_template('index.html')

# Serve other static files (CSS, JS)
@app.route('/<path:path>')
def serve_static_file(path):
    return send_from_directory(app.static_folder, path)

# Route to get all available courts
@app.route('/courts', methods=['GET'])
def get_courts():
    courts = list(courts_collection.find({}, {"_id": 0}))
    return jsonify(courts)

# Route to check availability for a specific court and date
@app.route('/courts/<int:court_number>/availability', methods=['GET'])
def check_availability(court_number):
    date = request.args.get('date')
    reservations = list(reservations_collection.find({
        "courtNumber": court_number,
        "date": date
    }, {"_id": 0}))
    return jsonify(reservations)

# Route to create a new reservation
@app.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.get_json()
    court_number = data['courtNumber']
    date = data['date']
    time = data['time']
    user = data['user']

    # Check if the court is already reserved at this time
    existing_reservation = reservations_collection.find_one({
        "courtNumber": court_number,
        "date": date,
        "time": time
    })

    if existing_reservation:
        return jsonify({"message": "Court already reserved at this time."}), 400

    # Create a new reservation
    reservation = {
        "courtNumber": court_number,
        "date": date,
        "time": time,
        "user": user
    }
    reservations_collection.insert_one(reservation)
    return jsonify(reservation), 201

if __name__ == '__main__':
    app.run(ssl_context='adhoc', debug=True, port=5000)
