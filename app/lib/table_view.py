from typing import Any, Iterable
from app.lib.data_view import DataView


class TableView(DataView):
    """ Database table wrapper

    """
    __slots__ = 'PAGE_SIZE'

    def __init__(self):
        self.PAGE_SIZE = 10
        super().__init__()

    def get(self, **kwargs: dict) -> object:
        """ Finds one record by fields

        Parameters
        ----------
        kwargs : dict
            Mapping of fields and values (field=value) and
            "order_by", "ci" (case insensitive) and op arguments

        Returns
        -------
        object

        """
        order_by = kwargs.pop('order_by', '')
        group_by = kwargs.pop('group_by', '')
        op = kwargs.pop('op', None)
        fn = kwargs.pop('fn', 'find')

        if fn not in {'find', 'select'}:
            fn = 'find'

        ops = {
            str: 'ILIKE' if kwargs.pop('ci', False) else 'LIKE',
            int: '=',
            float: '=',
            list: '=ANY',
            tuple: '=ANY'
        }

        where = []
        for key, val in kwargs.items():
            # try cast to numeric string to integer
            if isinstance(val, str) and val.isdecimal() and val[0] != 0:
                val = int(val)

            if val is None:
                where.append("{self.table_name}.{key} IS NULL")
            else:
                where.append("{0}.{1} {2} (:{1})".format(
                    self.table_name, key, op or ops.get(type(val), '=')))

        func = getattr(self, fn, self.find)

        return func(where=' AND '.join(where), values=kwargs,
                    order_by=order_by, group_by=group_by)

    def delete_by_id(self, item_id: int) -> int:
        """ Deletes a row by id field

        Parameters
        ----------
        item_id : int

        Returns
        -------
        int

        """
        return self.delete('id=:item_id', {'item_id': item_id})

    def update_by_id(self, values: dict, item_id: int) -> int:
        """ Updates a row by id field

        Parameters
        ----------
        values : dict
        item_id : int

        Returns
        -------
        int

        """
        return self.update(values, 'id=:item_id', {'item_id': item_id})

    def select_page(self, where: str = '', values: dict = {},
                    group_by: str = '', order_by: str = '', limit: int = 10,
                    page: int = 1, count: bool = False) -> Iterable:
        """ Selects one configurable page from a table

        Parameters
        ----------
        where : str
        values : dict
        group_by : str
        order_by : str
        limit : int
        page : int
        count : bool

        Returns
        -------
        Iterable

        """
        return self.select(where, values, group_by, order_by, limit,
                           (int(page) - 1) * int(limit), count=count)

    def update_order_between(self, parent_id: Any, what: int, where: int):
        """ Reorder and fix gaps in records between two order ids

        Parameters
        ----------
        parent_id : Any
        what : int
        where : int

        """
        if what > where:
            self.link.execute(
                "UPDATE {} SET order_id=order_id+1 \
                WHERE parent_id IS NOT DISTINCT FROM %(p_id)s \
                AND order_id>%(where)s AND order_id<%(what)s".
                format(self.table_name),
                {"p_id": parent_id, "what": what, "where": where})
        else:
            self.link.execute(
                "UPDATE {} SET order_id=order_id-1 \
                WHERE parent_id IS NOT DISTINCT FROM %(p_id)s \
                AND order_id>%(what)s AND order_id<=%(where)s".
                format(self.table_name),
                {"p_id": parent_id, "what": what, "where": where})

    def update_order_between_flat(self, what: int, where: int,
                                  cond: str = '', values: dict = {}):
        """ Reorder and fix gaps in records between two order ids

        Parameters
        ----------
        what: int
        where: int
        cond: str
        values: dict

        """
        if what > where:
            self.link.execute(
                "UPDATE {} SET order_id=order_id+1 WHERE order_id>%(where)s "
                "AND order_id<%(what)s {}".format(self.table_name, cond),
                dict(**{"what": what, "where": where}, **values))
        else:
            self.link.execute(
                "UPDATE {} SET order_id=order_id-1 WHERE order_id>%(what)s "
                "AND order_id<=%(where)s {}".format(self.table_name, cond),
                dict(**{"what": what, "where": where}, **values))

    def remove_from_stack(self, parent_id: Any, what: int):
        """ Remove one row from ordering stack

        Parameters
        ----------
        parent_id : Any
        what : int

        """
        self.link.execute(
            "UPDATE {} SET order_id=order_id-1 WHERE \
            parent_id IS NOT DISTINCT FROM %(p_id)s \
            AND order_id>%(what)s".format(self.table_name),
            {"p_id": parent_id, "what": what})

    def add_to_stack(self, parent_id: Any, where: int):
        """ Add a row to ordering stack

        Parameters
        ----------
        parent_id : Any
        where : int

        """
        self.link.execute(
            "UPDATE {} SET order_id=order_id+1 WHERE \
            parent_id IS NOT DISTINCT FROM %(p_id)s \
            AND order_id>=%(where)s".format(self.table_name),
            {"p_id": parent_id, "where": where + 1})

    def get_max_order(self, parent_id: Any) -> int:
        """ Get maximum order id within parent

        Parameters
        ----------
        parent_id : Any

        Returns
        -------
        int

        """
        res = self.link.execute('SELECT MAX(order_id) as order_id FROM {0}\
                                WHERE parent_id IS NOT DISTINCT FROM %(p_id)s'.
                                format(self.table_name), {'p_id': parent_id}
                                ).fetchone()

        return res.order_id if res.order_id else 0

    def get_item_path(self, item_id: Any) -> list:
        """ Recursively get parent IDs as a path

        Parameters
        ----------
        item_id : Any

        Returns
        -------
        list

        """
        query = """
        WITH RECURSIVE parents AS (
            SELECT id, parent_id, ARRAY[id] as path, order_id
                FROM {0} WHERE id = %(item_id)s
            UNION ALL
            SELECT r.id, r.parent_id, p.path || r.id, r.order_id
                FROM parents p JOIN {0} r ON p.parent_id = r.id
        ) select path from parents where parent_id is null
        """.format(self.table_name)

        return self.link.execute(query, {"item_id": item_id}).fetchone().path
