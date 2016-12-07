import logging

from flask import Flask
from flask_spyne import Spyne

from spyne.application import Application
from spyne.protocol.soap.soap11 import Soap11
from spyne.server.wsgi import WsgiApplication

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.contrib.fixers import LighttpdCGIRootFix

import api.default
from api.rest import rest
from api.soap import UTPService
from api.dbapi import DBAPI

import config as globals


logger = logging.getLogger(__name__)


def create_soap_wsgi(db):
    logger.debug('Creating SOAP interface')
    soap = Application(
            [UTPService],
            tns=globals.TARGET_NAMESPACE,
            name=globals.NAME,
            in_protocol=Soap11(validator='lxml'),
            out_protocol=Soap11(),)
    soap.db = db
    return WsgiApplication(soap)

def create_app():
    logging.basicConfig(level=logging.DEBUG)
    app = Flask(__name__)
    app.config.from_object('api.default.settings')
    app.db = DBAPI(globals.DB_MIN_CONN, globals.DB_MAX_CONN, dsn=globals.DSN)

    logger.debug('Starting RESTful API on URL {}'.format(globals.REST_URL))
    app.register_blueprint(rest, url_prefix=globals.REST_URL)

    logger.debug('Starting SOAP API on URL {}'.format(globals.SOAP_URL))
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app,
            {globals.SOAP_URL : create_soap_wsgi(app.db)})

    app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)
    return app

app= create_app()
logger.info('Application {} started'.format(globals.NAME))
