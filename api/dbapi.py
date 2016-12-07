import logging
import datetime
import json

from api.service.db import DB
from api.globals.queries import QUERIES


logger = logging.getLogger(__name__)


class DBAPI(object):
    def __init__(self, minconn, maxconn, *args, **kwargs):
        self._db = DB(QUERIES, minconn, maxconn, *args, **kwargs)

    def create_address(self, address):
        self._db.create_city(city=address.addressPlace.placeCity)
        self._db.create_place(place=address.addressPlace)
        self._db.create_address(address=address)

    def create_passenger(self, passenger):
        self._db.create_passenger(passenger=passenger)

    def create_order(self, order):
        self._db.create_order(order=order)
        for s in order.orderServices:
            s._order = order._id

    def create_service(self, service):
        self._db.create_service(service=service)

    def add_addresses(self, service):
        for i, address in enumerate(service.serviceAddresses):
            self.create_address(address)
            self._db.add_address_to_service(
                    serviceID=service._id,
                    addressID=address._id,
                    serial = i+1)

    def add_passengers(self, service):
        for i, passenger in enumerate(service.servicePassengers):
            self.create_passenger(passenger)
            self._db.add_passenger_to_service(
                    serviceID=service._id,
                    passengerID=passenger._id,
                    serial = i+1)

    def create_or_update_order(self, order):
        self.create_order(order)
        for service in order.orderServices:
            self.create_service(service)
            self.add_addresses(service)
            self.add_passengers(service)

    def get_orders(self, dates_range):
        try:
            tmp = self._db.get_orders_json(dates=dates_range)
            orders = tmp[0][0]
        except Exception as e:
            logger.error("DBAPI: {}".format(e))
            orders = None
        return orders
