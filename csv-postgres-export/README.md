
# csv-postgres-export
The project main goal is to read a csv file and insert the data into database.

## requirements
- [python](https://www.python.org/downloads/)
- [docker](https://www.docker.com/products/docker-desktop/)

> Use latest LTS versions

## setup

### python

#### create environment
```shell
python3 -m venv env
```

#### activate environment
```shell
source env/bin/activate
```

#### install requirements
```shell
pip3 install -r requirements.txt
```

## local execution

### postgresql database

#### deploy
```shell
docker run -d --name test_postgres  -e POSTGRES_DB=test -e POSTGRES_PASSWORD=test -p 5432:5432 postgres
```

#### create table
```shell
docker exec -it test_postgres psql -U postgres -d test -c "CREATE TABLE IF NOT EXISTS test_table (string_column VARCHAR(255), int_column NUMERIC, double_column NUMERIC, boolean_column BOOLEAN,timestamp_column TIMESTAMP WITHOUT TIME ZONE);"
```

#### fetch data
```shell
docker exec -it test_postgres psql -U postgres -d test -c "SELECT * FROM test_table;"
```


```shell
#python3 csv-postgres-export.py "${db_host}" "${db_port}" "${db_name}" "${db_user}" "${db_password}" "${db_insert_statement}" "${csv_path}"
python3 csv-postgres-export.py "localhost" "5432" "test" "postgres" "test" 'INSERT INTO test_table (string_column,int_column,double_column,boolean_column,timestamp_column) VALUES (%s,%s,%s,%s,%s);' "test.csv"
```

> change:  <br/>
> ${db_host} database host <br/>
> ${db_port} database port <br/>
> ${db_name} database name <br/>
> ${db_user} database username <br/>
> ${db_password} database password <br/>
> ${db_insert_statement} database insert statement <br/>
> ${csv_path} csv absolute or relative file path <br/>