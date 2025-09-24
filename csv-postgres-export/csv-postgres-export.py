import sys
import logging
import pandas
import psycopg2
from psycopg2 import sql

db_host = None
db_port = None
db_name = None
db_user = None
db_password = None
db_connection = None
db_insert_statement = None
csv_path = None

logging.basicConfig(
    level='DEBUG',
    format="%(asctime)s:%(process)d:%(filename)s:%(funcName)s:%(lineno)d:%(levelname)s:%(message)s",
)

def set_attributes():
    global db_host, db_port, db_name, db_user, db_password, db_connection, db_insert_statement, csv_path
    if len(sys.argv) == 8:
        db_host = sys.argv[1]
        db_port = sys.argv[2]
        db_name = sys.argv[3]
        db_user = sys.argv[4]
        db_password = sys.argv[5]
        db_insert_statement = sys.argv[6]
        csv_path = sys.argv[7]
        logging.debug(f"db_host = {db_host}, db_port = {db_port}, db_name = {db_name}, db_user = {db_user}, db_password = {db_password}, db_insert_statement = {db_insert_statement}, csv_path = {csv_path}")
    else:
        raise KeyError(f"exeucte script as {sys.argv[0]} ${{db_host}} ${{db_port}} ${{db_name}} ${{db_user}} ${{db_password}} ${{db_insert_statement}} ${{csv_path}}")
    db_params = {'host': db_host,'port': db_port,'dbname': db_name,'user': db_user,'password': db_password}
    db_connection = psycopg2.connect(**db_params)

def csv_process():
    df = pandas.read_csv(csv_path, quotechar='"')
    for col in df.columns:
        df[col] = df[col].apply(lambda x: None if pandas.isna(x) else x)
    with db_connection.cursor() as cursor:
        for _, row in df.iterrows():
            last = row
            insert_statement = sql.SQL(db_insert_statement)
            cursor.execute(insert_statement, tuple(row))
        db_connection.commit()

def main():
    try:
        set_attributes()
        try:
            csv_process()
        except Exception as e:
            logging.error(f"falure processing csv data; {e}")
        db_connection.close()
    except KeyError as ke:
        logging.error(str(ke))
    except Exception as e:
        logging.error(f"failure connecting to database; {e}")

main()
