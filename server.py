from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)
STATE_FILE = 'power_state.json'

def read_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f).get('state', False)
    return False

def write_state(state: bool):
    with open(STATE_FILE, 'w') as f:
        json.dump({'state': state}, f)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/power', methods=['GET'])
def get_power():
    return jsonify({'state': read_state()})

@app.route('/power', methods=['POST'])
def set_power():
    data = request.get_json()
    if data is None or 'state' not in data:
        return jsonify({'error': 'no state'}), 400
    new_state = bool(data['state'])
    write_state(new_state)

    return jsonify({'state': new_state})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)