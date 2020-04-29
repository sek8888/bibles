import sqlite3
from collections import namedtuple


class DB:
    """ Wrapper for sqlite3 basic methods

    Parameters
    ----------
    db_file : str

    """
    insert = "INSERT INTO %s(%s) VALUES (%s) %s"
    batch_insert = "INSERT INTO %s(%s) VALUES %s"
    update = "UPDATE %s SET %s WHERE %s %s"
    select = "SELECT %s FROM %s %s WHERE %s %s"
    select_count = "SELECT SUM(src.count) as count FROM (%s) as src"
    delete = "DELETE FROM %s WHERE %s"
    debug = False
    # debug = True

    def __init__(self, db_file: str):
        self.transaction = False
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        self.conn.row_factory = DB.namedtuple_factory
        # self.conn.row_factory = DB.dict_factory

    def reconnect(self):
        """ Close the current connection and reconnect to the DB

        """
        self.conn.close()
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        self.conn.row_factory = DB.namedtuple_factory
        # self.conn.row_factory = DB.dict_factory

    def execute(self, query: str, args: dict = {}):
        self.cur = self.conn.cursor()
        if not self.conn or self.conn != self.cur.connection:
            self.reconnect()

        if self.debug:
            # TODO change to log
            print("\n---Begin query---\n{0}\n---End query---\n".format(
                DB.debug_query(query, args)))

        try:
            self.cur.execute(query, args)
            if not self.transaction:
                self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise Exception(e)

        return self.cur

    def commit(self):
        """ Commits the open transaction if any found """
        if self.transaction:
            self.conn.commit()
            self.transaction = False

    def rollback(self):
        """ Rallbacks current transaction """
        self.conn.rollback()
        self.transaction = False

    @staticmethod
    def debug_query(query: str, _args: dict = {}):
        for k, v in _args.items():
            tmp = query.split(':{}'.format(k))

            if len(tmp) == 1:
                query = "'".join([tmp[0], str(v)])
                query = "{}'".format(query)
            else:
                query = "'".join([tmp[0], str(v), tmp[1]])

        return query

    @staticmethod
    def dict_factory(cursor, row):
        return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

    @staticmethod
    def namedtuple_factory(cursor, row):
        Row = namedtuple("Record", [col[0] for col in cursor.description])
        return Row(*row)
