import logging

from api.service.db import DB
from api.globals.queries import QUERIES


logger = logging.getLogger(__name__)


class DBAPI(object):
    def __init__(self, minconn, maxconn, *args, **kwargs):
        self._db = DB(QUERIES, minconn, maxconn, *args, **kwargs)

    def api_method(func):
        def _func(self, **kwargs):
            params = kwargs.keys()
            values = kwargs
            got_class = False
            logger.debug('Вызван метод {0}. Параметры: {1}'\
                .format(func.__name__, tuple(params)))

            if len(params) == 1 and hasattr(list(kwargs.values())[0],
                    '__dict__'):
                got_class = True
                values = list(kwargs.values())[0].__dict__

            result = None
            try:
                result = self._db._execute_api_method(func.__name__, **values)
            except:
                pass

            if got_class:
                list(kwargs.values())[0]._id = result
            else:
                return result

        return _func

    @api_method
    def create_city(self, **kwargs):
    """ parameters:
            City()
        or
            cityName: Unicode(255)
            cityTZDeltaSeconds: Integer(ge=-43200, le=43200)
    """
        pass

    @api_method
    def create_place(self, **kwargs):
    """ parameters:
            Place()
        or
            placeCity: City()
            placeName: Mandatory.Unicode(255)
            placeType: PlaceType (0, 1 or 2)
    """
        pass

    @api_method
    def create_address(self, **kwargs):
    """ parameters:
            address()
        or
            addressPlace: Place()
            addressStreet: Unicode(255)
            addressHouse: Unicode(255)
            addressPorch: Unicode(255)
            addressInfo: Unicode
    """
        pass

    @api_method
    def create_passenger(self, **kwargs):
    """ parameters:
            Passenger()
        or
            cityName: Unicode(255)
            cityTZDeltaSeconds: Integer(ge=-43200, le=43200)
    """
        pass

    @api_method
    def create_order(self, **kwargs):
        pass

    @api_method
    def create_service(self, **kwargs):
        pass

    @api_method
    def add_address_to_service(self, **kwargs):
        """ all named parameters only (look at api.globals.queries)
        """
        pass

    @api_method
    def add_passenger_to_service(self, **kwargs):
        """ all named parameters only (look at api.globals.queries)
        """
        pass

