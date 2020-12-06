import sys

import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine

HOST = "localhost"
USER = "root"
PWD = "root"
PORT = "3306"


def read_mysql(table):
    try:
        conn = pymysql.connect(host=HOST, user=USER, password=PWD, charset="utf8")
    except pymysql.err.OperationalError as e:
        print("Error is " + str(e))
        sys.exit()

    try:
        sql = f"SELECT * FROM {table};"
        df = pd.read_sql(sql, con=conn)
    except pymysql.err.ProgrammingError as e:
        print("Error is " + str(e))
        sys.exit()

    conn.close()

    df = df.replace("", np.nan)
    df["Tweet_time"] = pd.to_datetime(df["Tweet_time"])
    return df


def write_mysql(file, table_name, db_name="twitter_data"):
    try:
        engine = create_engine(f"mysql+pymysql://{USER}:{PWD}@{HOST}:{PORT}/ajx?charset=utf8")
    except pymysql.err.OperationalError as e:
        print("Error is " + str(e))
        sys.exit()

    df = pd.read_csv(file)

    try:
        df.to_sql(f"{db_name}.{table_name}", engine, if_exists="replace", index=False)
    except pymysql.err.ProgrammingError as e:
        print("Error is " + str(e))
        sys.exit()
