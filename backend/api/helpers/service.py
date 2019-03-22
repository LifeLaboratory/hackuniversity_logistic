# -*- coding: utf-8 -*-
import json
import psycopg2
from config.config import DATABASE
from datetime import date, datetime
from psycopg2.extras import RealDictCursor
import api.helpers.base_errors as errors
import backend.api.helpers.base_name as names


def db_connect_new():
    try:
        connect = psycopg2.connect(
            "dbname='{dbname}' user='{user}' host='{host}' password='{password}'".format(**DATABASE))
        return connect, connect.cursor(cursor_factory=RealDictCursor)
    except:
        print('Fatal error: connect database')
        raise


class Gis:
    @staticmethod
    def SqlQuery(query):
        """
        Метод выполняет SQL запрос к базе
        :param query: str SQL запрос
        :return: dict результат выполнения запроса
        """
        connect, current_connect = db_connect_new()
        result = None
        try:
            current_connect.execute(query)
            connect.commit()
        except psycopg2.Error as e:
            return result
        finally:
            try:
                result = current_connect.fetchall()
            except psycopg2.Error as e:
                return result
            connect.close()
            return result

    @staticmethod
    def __converter_data(param):
        if isinstance(param, date):
            return param.strftime('%Y.%m.%d %H:%M:%S')
        if isinstance(param, datetime):
            return param.strptime('%Y.%m.%d %H:%M:%S')

    @staticmethod
    def converter(js):
        """
        Метод преобразовывает передаваемый json в Dict и наоборот
        :param js: str или json
        :return: str или dict преобразованный элемент
        """
        return json.dumps(js, default=Gis.__converter_data) if isinstance(js, dict) \
            else json.loads(js)


class Sql:
    @staticmethod
    def connect():
        config_connect = "dbname='{dbname}' user='{user}' host='{host}' password='{password}'"
        try:
            connect = psycopg2.connect(config_connect.format(**DATABASE))
            return connect, connect.cursor(cursor_factory=RealDictCursor)
        except:
            return {names.ANSWER: errors.DATABASE_CONNECT}

    @staticmethod
    def exec(query=None, args=None, file=None):
        try:
            return Sql._switch(query=query, args=args, file=file)
        except:
            return None

    @staticmethod
    def _switch(query=None, args=None, file=None):
        if query and args:
            return Sql._query_exec_args(query, args)
        if query and not args:
            return Sql._query_exec(query)
        if file and args:
            return Sql._query_file_args_exec(file, args)
        if file:
            return Sql._query_file_exec(file)
        return None

    @staticmethod
    def _query_exec(query):
        return Sql._exec(query)

    @staticmethod
    def _query_file_exec(file):
        with open(file, 'r') as f:
            query = f.read()
            return Sql._exec(query)

    @staticmethod
    def _query_file_args_exec(file, args):
        with open(file, 'r') as f:
            query = f.read().format(**args)
            print()
            print(query)
            return Sql._exec(query)

    @staticmethod
    def _query_exec_args(query, args):
        query.format(**args)
        return Sql._exec(query)

    @staticmethod
    def _exec(query):
        """
        Метод выполняет SQL запрос к базе
        :param query: str SQL запрос
        :return: dict результат выполнения запроса
        """
        connect, current_connect = Sql.connect()
        result = None
        try:
            current_connect.execute(query)
        except psycopg2.Error as e:
            print(e.pgerror)
            print(e.diag.message_primary)
            print(psycopg2.errorcodes.lookup(e.pgcode))
        finally:
            try:
                result = current_connect.fetchall()
                connect.commit()
            except:
                connect.rollback()
            finally:
                connect.close()
                return result
