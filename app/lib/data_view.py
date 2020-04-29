import json
from contextlib import contextmanager
from typing import Iterable

from app import db


class DataView:
    """ Main class for database operations and data representation.

    Should contain table name assignment (self.table_name = "table").
    Should contain declaration of table's fields (self.fields = {}).
    {"id": {"rdonly": True, "alias": "number", "json": False, "expr": False}}

    """
    __slots__ = ('link', 'joins', 'join_fields', 'table_name', 'fields',
                 'attr_list', 'insert_row_count')

    def __init__(self):
        self.link = db
        self.joins = []
        self.join_fields = []
        # Define table name [self.table_name]

        self.update_fields()
        self.insert_row_count = 100

    def column_name(self, key: str) -> str:
        """ Generate full column name (with alias if specified)

        Parameters
        ----------
        key : str
            Column name from mapping

        Returns
        -------
        str

        """
        field_name = ''
        if self.fields[key].get('expr', False):
            field_name = f'({key})'
        else:
            field_name = f'{self.table_name}.{key}'

        # add alias for field
        if 'alias' in self.fields[key]:
            field_name = f'{field_name} AS {self.fields[key]["alias"]}'

        return field_name

    def update_fields(self, fields: dict = None):
        """ Updates fields definition

        Parameters
        ----------
        fields : dict

        """
        if fields is not None:
            self.fields = fields

        # set default options to the fields if options are None
        for key in self.fields:
            if self.fields[key] is None:
                self.fields[key] = {}
        self.attr_list = list(map(self.column_name, self.fields))

    def __encode_objects(self, key: str, value) -> str:
        """ Encode field flagged by "json"

        Parameters
        ----------
        key : str
            Column name from mapping
        value : variant
            Variant value

        Returns
        -------
        str
            JSON encoded string

        """
        # two ways from here: either json dumps you, either you're going back
        # with empty hands
        if self.fields[key].get('json', False) is True:
            return json.dumps(value, default=self.__date_handler)
        return value

    @staticmethod
    def __date_handler(obj: object) -> object:
        """ Generic method for handling the data during JSON encoding/decoding

        Parameters
        ----------
        obj : object

        Returns
        -------
        object
            Formatted date object or the same object

        """
        return obj.isoformat() if hasattr(obj, 'isoformat') else str(obj)

    def join(self, table: str, on: str, fields: list, jtype: str = 'LEFT'):
        """ Add join statements

        Parameters
        ----------
        table : str
            Name of the table to join with
        on : str
            Join conditions
        fields : list
            Fields to be included
        jtype : str
            Join type eg.: LEFT, RIGHT, INNER

        """
        self.joins.append(" ".join((jtype.upper(), "JOIN", table, "ON", on)))
        self.join_fields.extend(fields)

    def clear_joins(self):
        """ Remove all previously specified joins

        """
        self.joins = []
        self.join_fields = []

    def begin(self):
        """ Begin SQL transaction

        """
        self.link.transaction = True

    def commit(self):
        """ Commit previously begun SQL transaction

        """
        self.link.commit()

    def rollback(self):
        """ Rollback previously begun SQL transaction

        """
        self.link.rollback()

    def select(self, where: str = '', values: dict = {}, group_by: str = '',
               order_by: str = '', limit: int = -1, offset: int = -1,
               count: bool = False) -> Iterable:
        """ Wrapper for SQL SELECT statement

        Parameters
        ----------
        where : str
            SQL WHERE statement
        values : dict
            Values for WHERE statement
        group_by : str
            GROUP BY columns
        order_by : str
            ORDER BY columns
        limit : int
            Limit fetched results
        offset : int
            Offset of scanning
        count : bool
            Include count of selection

        Returns
        -------
        Iterable
            Iterator over namedtuple records

        """
        query_tail = []
        if group_by:
            query_tail.append(f'GROUP BY {group_by}')
        if order_by:
            query_tail.append(f'ORDER BY {order_by}')
        if limit > 0:
            query_tail.append('LIMIT :limit')
            values['limit'] = limit
        if offset > 0:
            query_tail.append('OFFSET :offset')
            values['offset'] = offset
        if len(where) == 0:
            where = "1"

        fields = self.attr_list + self.join_fields

        if count:
            fields += ['count(*) OVER () as all_count']

        query = self.link.select % (", ".join(fields), self.table_name,
                                    " ".join(self.joins),
                                    where, " ".join(query_tail))

        return self.link.execute(query, values)

    def find(self, where: str = '', values: dict = {}, order_by: str = '',
             group_by: str = '') -> object:
        """ Selects only one row with specified conditions

        Parameters
        ----------
        where : str
            SQL WHERE statement
        values : dict
            Values for WHERE statement
        order_by : str
            Columns for ORDER BY statement
        group_by : str
            Columns for GROUP BY statement

        Returns
        -------
        object

        """
        return self.select(where, values, group_by, order_by, 1).fetchone()

    def insert(self, values: dict) -> int:
        """ Wrapper for SQL INSERT statement

        Parameters
        ----------
        values : dict
            Mapping of column names and values

        Returns
        -------
        int

        """
        values = {key: self.__encode_objects(key, values[key])
                  for key in values if key in self.fields}
        field_list = {key: ":%s" % key
                      for key in values if key in self.fields and
                      self.fields[key].get("rdonly", False) is False}

        if len(field_list) == 0:
            return 0

        query = self.link.insert % \
            (self.table_name,
             ", " . join(field_list.keys()),
             ", " . join(field_list.values()),
             "")

        curr = self.link.execute(query, values)
        row_id = curr.lastrowid
        curr.close()

        return row_id

    def update(self, values: dict, where="1", condition: dict = {}) -> int:
        """ Wrapper for SQL UPDATE statement

        Parameters
        ----------
        values : dict
            Mapping of column names and values
        where : str
            Where conditions
        conditions : dict
            Condition mapping

        Returns
        -------
        int

        """
        values = {key: self.__encode_objects(key, values[key])
                  for key in values if key in self.fields}
        field_list = [
            "%s=:%s%s" % (key, key, f"::{self.fields[key]['cast']}"
                          if self.fields[key].get("cast") else '')
            for key in values if key in self.fields and
            self.fields[key].get("rdonly", False) is False
        ]

        if len(field_list) == 0:
            return 0

        values = dict(list(values.items()) + list(condition.items()))

        query = self.link.update % \
            (self.table_name, ", " . join(field_list), where, "")

        curr = self.link.execute(query, values)
        row_count = curr.rowcount
        curr.close()

        return row_count

    def delete(self, where="1", values: dict = {}) -> int:
        """ Wrapper for SQL DELETE statement

        Parameters
        ----------
        where : str
            Delete condition
        values : dict
            Mapping for condition

        Returns
        -------
        int
            Affected row count

        """
        query = self.link.delete % (self.table_name, where)

        curr = self.link.execute(query, values)
        if curr is None or curr.rowcount == 0:
            return 0

        count = curr.rowcount
        curr.close()
        return count

    def throw(self, message: str):
        """ Wrapper for Exception raising

        Parameters
        ----------
        message : str
            Exception message

        """
        raise Exception(f"DB error [{message}]")

# ------------------ do not tested --------------------------------
    def truncate(self) -> Iterable:
        """ Truncates the table

        """
        return self.link.execute(
            f"TRUNCATE {self.table_name} RESTART IDENTITY")

    def create_table(self, name: str, fields: list, indexes: dict = {}):
        """ Creates a table by specified definitions

        Parameters
        ----------
        name : str
        fields : list
        indexes : dict

        Returns
        -------

        """
        if len(fields) == 0:
            return False

        # iterate through fields
        ps = []
        for field in fields:
            ps.append(self._field_sql(field))

        # iterate through indexes
        for index in indexes:
            ps.append(self._index_sql(index))

        # iterate through indexes
        q = 'CREATE TABLE {} ({})'.format(name, ','. join(ps))
        return self.link.execute(q)

    def alter_table(self, name: str, fields: list, type: str = None) -> bool:
        if len(fields) == 0:
            return False

        q = 'ALTER TABLE {} {} {}'
        if len(fields) == 1:
            self.link.execute(q . format(name, 'ADD COLUMN',
                                         self._field_sql(fields[0])))
        elif len(fields) == 2:
            if fields[0] != fields[1]:
                self.link.execute(q . format(
                    name, 'RENAME COLUMN',
                    '{} TO {}'.format(fields[0], fields[1])))
            if type:
                self.link.execute(q . format(
                    name, 'ALTER COLUMN',
                    '{0} TYPE {1} USING ({0}::{1})'.format(fields[1], type)))

        return True

    def rename_table(self, name: str, new_name: str):
        return self.link.execute('ALTER TABLE {} RENAME TO {}'.format(
            name, new_name))

    def drop(self, table: str, field: str = None):
        if field is None:
            return self.link.execute('DROP TABLE {} CASCADE'.format(table))
        else:
            return self.link.execute(
                'ALTER TABLE {} DROP COLUMN {}'.format(table, field))

    @staticmethod
    def _field_sql(field_def):
        # name:type:not_null:ai
        # first_name:varchar(100):1

        _def = field_def.split(':')
        return '{} {} {} {}'. format(
            _def[0], _def[1], 'NOT NULL' if _def[2] == '1' else '',
            'DEFAULT {}'. format(_def[3]) if len(_def) > 3 else '')

    @staticmethod
    def _index_sql(index_def):
        # name:type
        _def = index_def.split(':')
        return ' {} KEY ({})'. format(_def[1], _def[0])

    def create_trigger(self, trigger_name: str, table_name: str,
                       function_name: str, when: str, events: list,
                       each: str = None, condition: str = None,
                       arguments: list = {}):
        self.link.execute(
            "CREATE TRIGGER {} {} {} ON {} {} {} EXECUTE PROCEDURE \
            {}({})".format(
                trigger_name, when, ' OR '. join(events), table_name,
                'FOR EACH {}'. format(each) if each else '',
                'WHEN ({})'. format(condition) if condition else '',
                function_name,
                ', '. join(arguments) if len(arguments) > 0 else ''))

    @contextmanager
    def transaction(self):
        try:
            self.begin()
            yield
            self.commit()
        except Exception as ex:
            self.rollback()
            raise ex

    def batch_insert(self, keys: tuple, values: list) -> int:
        """ Wrapper for SQL INSERT statement

        Parameters
        ----------
        keys : tuple
        values : list
            Tuples of column names and values mapping

        Returns
        -------
        int
            Inserted count

        """
        if not (values or values):
            return False

        my_transaction = False
        rowcount = 0

        for page in range(int(len(values)/self.insert_row_count)+1):
            value_group = values[page*self.insert_row_count:
                                 (page+1)*self.insert_row_count]
            if not value_group:
                break

            if not self.link.transaction:
                my_transaction = True
                self.begin()

            data = {}
            field_list = []
            for idx, row in enumerate(value_group):
                data[f'row_{idx}'] = row

                field_list.append(f'%(row_{idx})s')

                if len(field_list) == 0:
                    return False

            query = self.link.batch_insert % (self.table_name,
                                              ", ".join(keys),
                                              ", ".join(field_list))
            result = self.link.execute(query, data)

            if result is None:
                return False

            rowcount += result.rowcount

        if my_transaction:
            self.commit()

        return rowcount
# ------------------ do not tested --------------------------------
