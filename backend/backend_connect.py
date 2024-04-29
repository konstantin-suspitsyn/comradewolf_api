import psycopg2


def create_connection(db_name: str, user: str, password: str, host: str, port: str) -> psycopg2.connect:
    return psycopg2.connect(f"dbname={db_name} user={user} password={password} host={host} port={port}")


def get_data_from_db(sql_query: str):
    pass
