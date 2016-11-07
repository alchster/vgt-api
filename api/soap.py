import logging

from spyne.decorator import srpc
from spyne.service import ServiceBase
from spyne.model.enum import Enum
from spyne.model.complex import Iterable, ComplexModel, Mandatory as ComplexMandatory
from spyne.model.primitive import Mandatory, Duration, DateTime, Integer, UnsignedInteger, Unicode, Boolean, Uuid


logger = logging.getLogger(__name__)
ID = Mandatory.UnsignedInteger(type_name='ID')
Status = Mandatory.Integer(ge=1, le=8, type_name='Status')              # см. таблицу статусов заказа в БД
PlaceType = Mandatory.Integer(ge=0, le=2, type_name="PlaceType")        # 0 - по адресу, 1 - аэропорт, 2 - вокзал
ServiceType = Mandatory.Integer(ge=0, le=1, type_name='ServiceType')    # 0 - трансфер, 1 - аренда


class ComplexModelBase(ComplexModel):
    def __init__(self):
        self._id = ''

    def __str__(self):
        return self._id


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
    passengerPantronymic = Unicode(255)
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

    serviceMeetDateTime = Mandatory.DateTime
    serviceMeetPlate = Unicode

    serviceAddresses = Iterable(Address)

    serviceBaggage = Unicode
    serviceBabyChairs = Mandatory.UnsignedInteger()
    serviceComment = Unicode


class Order(ComplexModelBase):
    orderID = ID
    orderPartnerID = ID
    orderManagerID = ID
    orderCreateDateTime = Mandatory.DateTime
    orderServices = Iterable(Service, nillable=False)
    orderFeedbackURL = Unicode(255)


class Response(ComplexModel):
    responseCode = Mandatory.UnsignedInteger
    responseMessage = Mandatory.Unicode

    def __init__(self, c, m):
        self.responseCode = c
        self.responseMessage = m


# описание протокола
class UTPService(ServiceBase):

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

    @srpc(Iterable(Order, nillable=False),
          _returns=ComplexMandatory(Response, type_name='Response'))
    def addOrUpdateOrders(orders):
        for order in orders:
            self.app.db.create_or_update_order(order)
        return Response(0, 'OK')
