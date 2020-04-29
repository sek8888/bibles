import json
from app import app


def json_response(data: dict):
    return app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
