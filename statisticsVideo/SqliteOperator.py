#encode-UTF-8
import sqlite3
#
# --------------------------------------- cursor operation ---------------------------------------#
#
def db_get_cursor(conn, sql, condition_pair, order=None):
    if condition_pair:
        where, values = condition_pair
        sql += ' where %s' % where
        if order:
            sql = '%s order by %s' % (sql, order)

        cursor = conn.execute(sql, values)
    else:
        if order:
            sql = '%s order by %s' % (sql, order)
        cursor = conn.execute(sql)
    return cursor


def db_cursor_get_count(conn, sql, condition_pair):
    cursor = db_get_cursor(conn, sql, condition_pair)
    if cursor:
        row = cursor.fetchone()
        if row:
            return row[0]
    return 0

def db_cursor_has_item(conn, sql, condition_pair):
    return db_cursor_get_count(conn, sql, condition_pair) > 0


def db_cursor_get_field_names(cursor):
    return (i[0] for i in cursor.description)

#
# --------------------------------------- table operation ---------------------------------------#
#
def db_table_get_cursor(conn, table, condition_pair, order=None, fields=None):
    return db_get_cursor(conn, 'select %s from %s' % (fields if fields else '*', table), condition_pair, order)


def db_table_get_count(conn, table, condition_pair):
    return db_cursor_get_count(conn, 'select count(*) from %s' % table, condition_pair)


def db_table_has_item(conn, table, condition_pair):
    return db_table_get_count(conn, table, condition_pair) > 0


def db_table_get_field_names(conn, table):
    return db_cursor_get_field_names(conn.execute('select * from %s where 1<>1' % table))


def db_has_table(conn, table):
    return db_table_has_item(conn, 'sqlite_master', ('name=?', [table]))


def db_table_add_rows(conn, table, rows, keys):
    if not rows:
        return
    header = rows[0]
    condition_key_index = [header.index(key) for key in keys]
    condition_where = ' and '.join(('%s=?' % key for key in keys))

    def has_item(row):
        return db_table_has_item(conn, table, [condition_where, [row[i] for i in condition_key_index]])

    sql = 'insert into %s(%s) values(%s)' % (table, ','.join(header), ','.join('?' * len(header)))
    for row in rows[1:]:
        if not has_item(row):
            conn.execute(sql, row)
    conn.commit()


def db_table_remove(conn, table, condition_pair):
    sql = 'delete from ' + table
    if condition_pair:
        where, values = condition_pair
        sql = '%s where %s' % (sql, where)
        conn.execute(sql, values)
    else:
        conn.execute(sql)
    conn.commit()

def db_get_results(conn,table):
    sql = 'select * from ' + table
    cursor = conn.cursor()
    return cursor.execute(sql)

def db_create_table(conn, table, fields_define, index_fields):
    if not db_has_table(conn, table):
        conn.execute('''create table %s(%s)''' % (table, ','.join(fields_define)))
        for index_field in index_fields:
            conn.execute('create index idx_%s_%s on %s(%s)' % ((table, index_field) * 2))
        conn.commit()


# if __name__ == '__main__':
#
#     conn = sqlite3.connect('videos')
#     table = 'processedVideo'
#
#     fields = ('videoName', 'successful')
#     db_create_table(conn, table, fields, ['videoName'])
#
#     rows = [fields]
#     rows.append(('1.mp4','successful'))
#     db_table_add_rows(conn, table, rows, ['videoName'])
#
#     print(db_has_table(conn, table))
#     print(db_table_get_count(conn, table, ('videoName=?', ['1.mp5'])))
#     print(db_table_get_count(conn, table, ('videoName=?', ['1.mp4'])))
#
#     results = db_get_results(conn,table)
#     for r in results:
#         print(r)
    # import unittest
    #
    #
    # class CTest(unittest.TestCase):
    #     def setUp(self):
    #
    #         self.conn = sqlite3.connect(':memory:')
    #
    #         self.table = 'ta'
    #         self.fields = ('a', 'b')
    #         db_create_table(self.conn, self.table, self.fields, 'a')
    #
    #     def tearDown(self):
    #         self.conn = None
    #
    #     def test001_table_query(self):
    #         conn = self.conn
    #         table = self.table
    #         assert (db_has_table(conn, table))
    #         assert (db_table_get_count(conn, table, ('a=?', ['1'])) == 0)
    #         assert (db_table_get_count(conn, table, None) == 0)
    #         assert (tuple(db_table_get_field_names(conn, table)) == self.fields)
    #         assert (tuple(db_cursor_get_field_names(db_table_get_cursor(conn, table, None))) == self.fields)
    #
    #     def build_rows(self):
    #         rows = [self.fields]
    #         rows.extend((i, i) for i in range(10000))
    #         print(rows)
    #         return rows
    #
    #     def test002_table_add_remove_rows(self):
    #         conn = self.conn
    #         table = self.table
    #
    #         rows = self.build_rows()
    #         db_table_add_rows(conn, table, rows, 'a')
    #         assert (db_table_get_count(conn, table, None) == len(rows) - 1)
    #         for row in rows[1:]:
    #             assert (db_table_has_item(conn, table, ('a=?', [row[0]])))
    #
    #         cursor = conn.execute('select * from ta where 1<>1')
    #         assert (tuple(db_table_get_field_names(conn, table)) == self.fields)
    #         assert (cursor.fetchone() == None)
    #
    #         db_table_remove(conn, table, None)
    #         assert (db_table_get_count(conn, table, None) == 0)
    #
    #
    # unittest.main()