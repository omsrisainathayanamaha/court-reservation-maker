from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__, static_folder='static')

# MongoDB setup
import os
import subprocess


def create_data_directory():
    """Create the MongoDB data directory if it doesn't exist."""
    data_directory = "./data/db"
    if not os.path.exists(data_directory):
        print(f"Creating data directory at {data_directory}...")
        os.makedirs(data_directory)
        print(f"Data directory created at {data_directory}.")
    else:
        print(f"Data directory already exists at {data_directory}.")

def create_config_file():
    """Create or modify the MongoDB configuration file."""
    config_content = """
storage:
  dbPath: ./data/db
net:
  bindIp: 127.0.0.1
  port: 27017
systemLog:
  destination: file
  path: ./data/mongod.log
  logAppend: true
"""
    config_path = "./mongodb.conf"
    print(f"Creating or updating MongoDB configuration file at {config_path}...")
    with open(config_path, "w") as config_file:
        config_file.write(config_content)
    print("MongoDB configuration file created/updated successfully.")

def start_mongo():
    """Start MongoDB using the configuration file."""
    config_path = "./mongodb.conf"
    try:
        print("Starting MongoDB...")
        subprocess.run(["mongod", "--config", config_path, "--verbose"], check=True)
        print("MongoDB started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting MongoDB: {e}")
    except FileNotFoundError:
        print("MongoDB executable not found. Ensure MongoDB is installed and in your PATH.")
    except Exception as e:
        print(f"An error occurred: {e}")
    




client = MongoClient("mongodb://127.0.0.1:27017/")
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


if __name__ == "__main__":
    create_data_directory()
    create_config_file()
    start_mongo()
    app.run(ssl_context='adhoc', debug=True, port=2000)
