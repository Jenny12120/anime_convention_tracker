from flask import Flask, jsonify, request
from flask_cors import CORS
from search_model import fetch_from_db_date_range,fetch_from_db_location 

app = Flask(__name__)
CORS(app) 

@app.route('/api/search_conventions', methods=['GET'])
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
        
if __name__ == '__main__':
    app.run(debug=True, port=5000)