from flask_restful import Resource
from flask import request, jsonify
import json, os

class Feedback(Resource):
    def post(self):
        content = request.get_json(silent=True)
        os.makedirs('logs', exist_ok=True)
        with open('logs/feedback.txt', 'a') as f:
            json.dump(content, f)
            f.write('\n')
        return jsonify({'status':'ok'})
