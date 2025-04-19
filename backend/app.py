from flask import Flask, request, jsonify
from coordinator import Coordinator
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
coordinator = Coordinator()

@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    data = request.json
    user_input = data.get('user_input', '')
    result = coordinator.process(user_input)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)
