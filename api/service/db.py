import logging
from contextlib import contextmanager

from psycopg2.pool import ThreadedConnectionPool


logger = logging.getLogger(__name__)

LEVELS = dict(
        NOERROR = logging.INFO,
        WARNING = logging.WARNING,
        ERROR = logging.ERROR
    )

def api_method(name, func):
    def _func(self, **kwargs):
        params = kwargs.keys()
        values = kwargs
        got_class = False
        logger.debug('Вызван метод {0}. Параметры: {1}'\
            .format(name, tuple(params)))

        if len(params) == 1 and hasattr(list(kwargs.values())[0],
                '__dict__'):
            got_class = True
            values = list(kwargs.values())[0].__dict__

        try:
            result = self.execute_api_method(name, **values)
        except Exception as e:
            logger.error("ОШИБКА. %s", e)
            result = None

        if got_class and not 'get_data' in values:
            list(kwargs.values())[0]._id = result
        else:
            return result

    return _func


class Result(object):

    def __init__(self, result):
        assert type(result) == tuple
        self.from_string(result[0])

    def from_string(self, string):
        self.value = None
        tmp = string[1:-1].replace('"', '').split(',')
        self.code = tmp[0]
        self.type = tmp[1]
        self.name = tmp[2]
        self.description = tmp[3]
        self.details = tmp[4]
        self.date = tmp[5]
        self.value = tmp[6]

    def __str__(self):
        return "{code} {name}: {description}. ДЕТАЛИ: {details}"\
                .format(**self.__dict__)


class DB(object):

    def __init__(self, queries, minconn, maxconn, *args, **kwargs):
        self.queries = queries

        for method in self.queries.keys():
            setattr(DB, method, api_method(method, lambda self, **kwargs: None))
            logger.debug("Добавлен метод API базы данных: {}".format(method))

        self.pool = ThreadedConnectionPool(minconn, maxconn, *args, **kwargs)
        logger.debug('Создан пул соеднинений с базой данных размером {}'\
                'и минимальным количеством соединений {}'.format(maxconn, minconn))

    @contextmanager
    def _connect(self):
        logger.debug('Резервируется соединение с базой данных')
        con = self.pool.getconn()
        try:
            yield con.cursor()
            con.commit()
        finally:
            logger.debug('Освобождается соединение с базой данных')
            self.pool.putconn(con)

    def execute_api_method(self, method_name, **kwargs):
        if method_name not in self.queries:
            logger.error("DBAPI: Нет такого метода '{}'"
                .format(method_name))
            return

        with self._connect() as cursor:
            logger.info("DBAPI: Вызов '{}'".format(method_name))
            params = self.queries[method_name].format(**kwargs)
            if 'get_data' not in kwargs:
                query = "select {0}({1});".format(method_name, params)
            else:
                query = "select * from {0}({1});".format(method_name, params)
            logger.debug('ЗАПРОС: {}'.format(query))
            cursor.execute(query)
            if 'get_data' not in kwargs:
                result = Result(cursor.fetchone())
                logger.log(LEVELS[result.type], 'DBAPI: {}'.format(result))
                return result.value
            return cursor.fetchall()

#    def get_orders(date_from, date_to):
#        with self._connect() as cursor:
