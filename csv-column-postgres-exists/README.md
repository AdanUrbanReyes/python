
# csv-column-postgres-exists
The project main goal is to read a csv column values, and validate if they exists on postgresql database table.

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
docker exec -it test_postgres psql -U postgres -d test -c "CREATE TABLE IF NOT EXISTS test_table (test_column VARCHAR(255));"
```

#### insert dummy data
```shell
docker exec -it test_postgres psql -U postgres -d test -c "INSERT INTO test_table VALUES ('test_value_11');"
```


```shell
#python3 csv-column-postgres-exists.py "${db_host}" "${db_port}" "${db_name}" "${db_user}" "${db_password}" "${db_query_prefix}" "${csv_path}" "${csv_column_read}" "${csv_column_write}" ${csv_chunk_size}
python3 csv-column-postgres-exists.py "localhost" "5432" "test" "postgres" "test" 'SELECT LOWER(TRIM(test_column)) FROM test_table WHERE LOWER(TRIM(test_column))' "test.csv" "TEST COLUMN 1" "TEST COLUMN 3" 100
```

> change: 
> ${db_host} database host
> ${db_port} database port
> ${db_name} database name
> ${db_user} database username
> ${db_password} database password
> ${db_query_prefix} database query prefix to fetch existing database values
> ${csv_path} csv absolute or relative file path
> ${csv_column_read} csv column header name where values to fetch will be taken
> ${csv_column_write} csv column heaer name to write if they value exists (true) or not (false)
> ${csv_chunk_size} csv chunk size of values to validate