from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "localhost"



CREATE_DB = "CREATE DATABASE workshop;"

CREATE_TB_USERS = """CREATE TABLE users(
    id serial PRIMARY KEY,
    username varchar(255) UNIQUE,
    hashed_password varchar(80)
);"""

CREATE_MSG_TABLE = """CREATE TABLE messages(
    id serial PRIMARY KEY,
    from_id INTEGER REFERANCES user(id) ON DELETE CASCADE,
    to_id INTEGER REFERANCES user(id) ON DELETE CASCADE,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    text VARCHAR(255)
);"""



cnx = connect(database="workshop", user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
cnx.autocommit = True
cursor = cnx.cursor()
try:
    cursor.execute(CREATE_TB_USERS)
    print("database created successfully")
    cnx.close()
except DuplicateDatabase as e:
    print("database already exists", e)


try:
    cnx = connect(database="workshop", user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cnx.autocommit = True
    cursor = cnx.cursor()

    try:
        cursor.execute(CREATE_TB_USERS)
        print("Table user created successfully")
    except DuplicateTable as e:
        print("table already exists", e)

    try:
        cursor.execute(CREATE_MSG_TABLE)
        print("Table message created successfully")
    except DuplicateTable as e:
        print("table already exists", e)

    cnx.close()
except OperationalError as e:
    print("Connection error", e)