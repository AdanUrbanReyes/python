import sys
import logging
import pandas
import psycopg2

db_host = None
db_port = None
db_name = None
db_user = None
db_password = None
db_connection = None
db_query_prefix = None
csv_path = None
csv_column_read = None
csv_column_write = None
csv_chunk_size = None

logging.basicConfig(
    level='DEBUG',
    format="%(asctime)s:%(process)d:%(filename)s:%(funcName)s:%(lineno)d:%(levelname)s:%(message)s",
)

def set_attributes():
    global db_host, db_port, db_name, db_user, db_password, db_connection, db_query_prefix, csv_path, csv_column_read, csv_column_write, csv_chunk_size
    if len(sys.argv) == 11:
        db_host = sys.argv[1]
        db_port = sys.argv[2]
        db_name = sys.argv[3]
        db_user = sys.argv[4]
        db_password = sys.argv[5]
        db_query_prefix = sys.argv[6]
        csv_path = sys.argv[7]
        csv_column_read = sys.argv[8]
        csv_column_write = sys.argv[9]
        csv_chunk_size = int(sys.argv[10])
        logging.debug(f"db_host = {db_host}, db_port = {db_port}, db_name = {db_name}, db_user = {db_user}, db_password = {db_password}, db_query_prefix = {db_query_prefix}, csv_path = {csv_path}, csv_column_read = {csv_column_read}, csv_column_write = {csv_column_write}, csv_chunk_size = {csv_chunk_size}")
    else:
        raise KeyError(f"exeucte script as {sys.argv[0]} ${{db_host}} ${{db_port}} ${{db_name}} ${{db_user}} ${{db_password}} ${{db_query_prefix}} ${{csv_path}} ${{csv_column_read}} ${{csv_column_write}} ${{csv_chunk_size}}")
    db_params = {'host': db_host,'port': db_port,'dbname': db_name,'user': db_user,'password': db_password}
    db_connection = psycopg2.connect(**db_params)

def csv_process():
    df = pandas.read_csv(csv_path, quotechar='"')
    df[csv_column_write] = 'false'
    cursor = db_connection.cursor()
    for start in range(0, len(df), csv_chunk_size):
        end = start + csv_chunk_size - 1
        csv_values_chunk = df.loc[start:end, csv_column_read].dropna().str.lower().unique().tolist()
        placeholders = ','.join(['%s'] * len(csv_values_chunk))
        logging.info(f"values to validate: {csv_values_chunk}")
        query = f"{db_query_prefix} IN ({placeholders});"
        cursor.execute(query, csv_values_chunk)
        db_values = cursor.fetchall()
        db_values = set(value for (value,) in db_values)
        logging.info(f"database values found: {db_values}")
        df.loc[df[csv_column_read].str.lower().isin(db_values), csv_column_write] = 'true'
    df.to_csv(csv_path, index=False)

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