from flask import Flask, jsonify, request
from flask_cors import CORS
from search_model import fetch_from_db_date_range,fetch_from_db_location 
from tracking_model import add_to_tracking, retrieve_all_tracked_conventions, untrack_convention

app = Flask(__name__)
CORS(app) 

@app.route('/api/search_conventions_by_date', methods=['GET'])
def search_conventions():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    
    if not start_date or not end_date:
        return jsonify({"error": "Missing start or end date parameters."}), 400

    try:
        data = fetch_from_db_date_range(start_date, end_date)
        return jsonify(data)
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": "A server error occurred while fetching data."}), 500

@app.route('/api/search_conventions_by_location', methods=['GET'])
def search_conventions_by_location():
    location = request.args.get('location')
    
    if not location:
        return jsonify({"error": "Missing location."}), 400
    try:
        data = fetch_from_db_location(location)
        return jsonify(data)
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": "A server error occurred while fetching data."}), 500

@app.route('/api/add_to_tracking', methods=['POST'])
def add_convention_to_tracking():
    id = request.args.get('id')
    name = request.args.get('name')
    
    if not id:
        return jsonify({"error": "Missing id."}), 400
    try:
        data = add_to_tracking(id,name)
        return jsonify(data)
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": "A server error occurred while fetching data."}), 500

@app.route('/api/get_all_tracked_conventions', methods=['GET'])
def get_all_tracked_conventions():
    try:
        data = retrieve_all_tracked_conventions()
        return jsonify(data)
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": "A server error occurred while fetching data."}), 500

@app.route('/api/delete_from_tracking', methods=['DELETE'])
def delete_from_tracking():
    id = request.args.get('id')
    
    if not id:
        return jsonify({"error": "Missing id to delete."}), 400
    try:
        data = untrack_convention(id)
        return jsonify(data)
    except Exception as e:
        print(f"Database error: {e}")
        return jsonify({"error": "A server error occurred while fetching data."}), 500
                    
if __name__ == '__main__':
    app.run(debug=True, port=5000)