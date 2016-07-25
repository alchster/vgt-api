import logging

from flask import Flask

import api.default
from api.service.db import DB


def create_app():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    app = Flask(__name__)
    app.config.from_object('api.default.settings')
    app.db = DB(3, 10, dsn='host=localhost dbname=vgt user=vgt password=hhSFq544sf port=5432')
    return app

app = create_app()

import api.routes
