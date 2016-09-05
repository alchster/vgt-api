import logging
import json

from flask import Blueprint, request


rest = Blueprint('rest', __name__)
logger = logging.getLogger(__name__)


@rest.route('/test', methods=['GET'])
def test():
    logger.debug('Called test method')
    return 'OK', 200

@rest.route('/order', methods=['POST', 'PUT'])
def create_order():
    order_data = request.get_json()
    if not order_data:
        return json.dumps({'error':'No data or it is not in JSON format or request header is not valid'}), 400

    return 'OK', 200

@rest.route('/order/<path:oid>', methods=['GET'])
def get_order(oid):
    return oid, 200

@rest.route('/order/<path:oid>', methods=['PATCH'])
def update_order(oid):
    return oid, 200

@rest.route('/order/<path:oid>', methods=['DELETE'])
def delete_order(oid):
    return oid, 200

@rest.route('/orders', methods=['GET'])
def list_orders():
    return 'OK', 200
