import sys

import numpy as np
import pandas as pd
import pymysql

HOST = 'localhost'
USER = 'root'
PWD = 'root'


def read_mysql(table):
    try:
        conn = pymysql.connect(host=HOST, user=USER, password=PWD, charset='utf8')
    except pymysql.err.OperationalError as e:
        print('Error is ' + str(e))
        sys.exit()

    try:
        sql = f"SELECT * FROM {table};"
        df = pd.read_sql(sql, con=conn)
    except pymysql.err.ProgrammingError as e:
        print('Error is ' + str(e))
        sys.exit()

    conn.close()

    df = df.replace("", np.nan)
    df["Tweet_time"] = pd.to_datetime(df["Tweet_time"])
    return df
