import logging
import datetime

from spyne.decorator import rpc, srpc
from spyne.service import ServiceBase
from spyne.model.enum import Enum
from spyne.model.complex import Iterable, ComplexModel, Mandatory as ComplexMandatory
from spyne.model.primitive import Mandatory, Duration, DateTime, Integer, UnsignedInteger, Unicode, Boolean, Uuid

from api.service.utils import to_dates, to_datetime

logger = logging.getLogger(__name__)
ID = Mandatory.UnsignedInteger(type_name='ID')
Status = Mandatory.Integer(ge=1, le=8, type_name='Status')              # см. таблицу статусов заказа в БД
PlaceType = Mandatory.Integer(ge=0, le=2, type_name="PlaceType")        # 0 - по адресу, 1 - аэропорт, 2 - вокзал
ServiceType = Mandatory.Integer(ge=0, le=1, type_name='ServiceType')    # 0 - трансфер, 1 - аренда


class ComplexModelBase(ComplexModel):
    def __init__(self, *args, **kwargs):
        ComplexModel(self, *args, **kwargs)
        self._id = ''

    def __str__(self):
        return self._id


class MandatoryDateTime(Mandatory.DateTime):
    def __init__(cls, *args, **kwargs):
        print("------------------------------------ here --------------------------------------")


class CarClass(ComplexModelBase):
    carClassCode = Mandatory.UnsignedInteger
    carClassName = Mandatory.Unicode(50)


class City(ComplexModelBase):
    cityName = Unicode(255)
    cityTZDeltaSeconds = Integer(ge=-43200, le=43200)


class Place(ComplexModelBase):
    placeCity = City
    placeName = Mandatory.Unicode(255)
    placeType = PlaceType


class Address(ComplexModelBase):
    addressPlace = Place
    addressStreet = Unicode(255)
    addressHouse = Unicode(255)
    addressPorch = Unicode(255)
    addressInfo = Unicode


class Passenger(ComplexModelBase):
    passengerName = Mandatory.Unicode(255)
    passengerPatronymic = Unicode(255)
    passengerSurname = Unicode(255)
    passengerPhone = Mandatory.Unicode(255)
    passengerDescription = Unicode


class Service(ComplexModelBase):
    _order = None
    serviceID = ID
    serviceType = ServiceType
    serviceStatus = Status
    serviceCarClassID = ID
    servicePassengers = Iterable(Passenger, nillable=False)
    servicePassengersCount = Mandatory.UnsignedInteger      # число пассажиров может отличаться от списка выше

    serviceMeetDateTime = MandatoryDateTime
    serviceMeetPlate = Unicode

    serviceAddresses = Iterable(Address)

    serviceBaggage = Unicode
    serviceBabyChairs = Mandatory.UnsignedInteger()
    serviceComment = Unicode


class Order(ComplexModelBase):
    orderID = ID
    orderPartnerID = ID
    orderManagerID = ID
    orderCreateDateTime = MandatoryDateTime
    orderServices = Iterable(Service, nillable=False)
    orderFeedbackURL = Unicode(255)


class Response(ComplexModel):
    responseCode = Mandatory.UnsignedInteger
    responseMessage = Mandatory.Unicode

    def __init__(self, c, m):
        self.responseCode = c
        self.responseMessage = m


class DatesRange(object):
    dateFrom = DateTime
    dateTo = DateTime

    def __init__(self, f, t):
        self.dateFrom, self.dateTo = to_dates(f, t)
        self.get_data = True


# описание протокола
class UTPService(ServiceBase):

    @srpc(_returns=DateTime)
    def utc():
        return datetime.datetime.utcnow()

    @srpc(_returns=DateTime)
    def now():
        return datetime.datetime.now()

    @srpc(_returns=ComplexMandatory(Response, type_name='Response'))
    def hello():
        logger.debug('hello called')
        return Response(0, 'OK')

    @srpc(Iterable(City, nillable=False),
          _returns=ComplexMandatory(Response, type_name='Response'))
    def updateCities(cities):
        return Response(0, 'OK')

    @srpc(Iterable(CarClass, nillable=False),
          _returns=ComplexMandatory(Response, type_name='Response'))
    def updateCarClasses(classes):
        return Response(0, 'OK')

    @srpc(Iterable(Place, nillable=False),
          _returns=ComplexMandatory(Response, type_name='Response'))
    def updatePlaces(places):
        return Response(0, 'OK')

    @rpc(Iterable(Order, nillable=False),
          _returns=ComplexMandatory(Response, type_name='Response'))
    def addOrUpdateOrders(self, orders):
        for order in orders:
            self.app.db.create_or_update_order(order)
        return Response(0, 'OK')

    @rpc(DateTime, DateTime,
          _returns=Iterable(Order))
    def getOrders(self, dateFrom, dateTo):
        orders = self.app.db.get_orders(DatesRange(dateFrom, dateTo))
        for order in orders:
            order['orderCreateDateTime'] = to_datetime(order['orderCreateDateTime'])
            for service in order['orderServices']:
                service['serviceMeetDateTime'] = to_datetime(service['serviceMeetDateTime'])
        return orders
