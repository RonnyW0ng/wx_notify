# -*- coding: utf-8 -*-
# db.py

import web


class DB(object):
    def __init__(self, table: str, data_file: str = './db.sqlite3') -> None:
        self.data_file = data_file
        self.table = table
        self.db = web.database(dbn='sqlite', db=self.data_file)

    def _process_where_(self, where: dict):
        w_str = None
        w_items = enumerate(where.items())
        w_items_copy = enumerate(where.items())
        w_len = len(list(w_items_copy))

        if w_len:
            w_str = ''
            for inx, w in w_items:
                if inx == w_len-1:
                    w_str += f'`{w[0]}`="{w[1]}" '
                else:
                    w_str += f'`{w[0]}`="{w[1]}" and '
        return w_str

    def insert(self, data: dict):
        return self.db.insert(self.table, **data)

    def update(self, where: dict, data: dict):
        w_str = self._process_where_(where)
        return self.db.update(self.table, where=w_str, **data)

    def fetchRow(self, where: dict = {}, rows: int = 0, columns: list = ['*'], **kwargs):
        limit = None
        w_str = self._process_where_(where)

        if rows:
            limit = rows
        c_str = ''
        for i in columns:
            c_str += f'{i},'
        c_str = c_str.strip(',')
        r = self.db.select(self.table, where=w_str, what=c_str, limit=limit)
        if 'first' in kwargs and kwargs['first'] == True:
            return r.first()
        return r.list()
