import logging
from contextlib import contextmanager

from psycopg2.pool import ThreadedConnectionPool


class DB(object):

    def __init__(self, minconn, maxconn, *args, **kwargs):
        logging.debug(
                'Creating PostgreSQL connection pool total width %d with minimal %d connections'%(maxconn, minconn))
        self.pool = ThreadedConnectionPool(minconn, maxconn, *args, **kwargs)

    @contextmanager
    def _connect(self):
        logging.debug('Getting connection from pool')
        con = self.pool.getconn()
        try:
            yield con
        finally:
            logging.debug('Putting connection back to the pool')
            self.pool.putconn(con)
