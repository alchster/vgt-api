import logging
import json

from flask import request

from api import app

@app.route('/test', methods=['GET'])
def test():
    return 'OK', 200

@app.route('/order', methods=['POST', 'PUT'])
def order():
    order_data = request.get_json()
    if not order_data:
        return json.dumps({'error':'No data or it is not in JSON format or request header is not valid'}), 400

    return 'OK', 200

@app.route('/orders/<path:oid>', methods=['GET', 'PATCH', 'DELETE'])
def orders(oid):
    return oid, 200
