import argparse

from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation

import bcrypt
from models import User

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters")
parser.add_argument("-n" "--new_password", help="new password (min 8 characters)")
parser.add_argument("-l" "list", help="list all users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")

args = parser.parse_args()

def list_user(cur):
    users = User.load_all_users(cur)
    for user in users:
        print(user.username)
def create_user(cur, username, password):
    if len(password) < 8:
        print("Password must be at least 8 characters")
    else:
        try:
            user = User(username=username, password=password)
            user.save_to_db(cur)
            print("User created successfully")
        except UniqueViolation as e:
            print("User alredy exist.", e)
def delete_user(cur, username, password):
    user = User.load_user_by_username(cur, username)
    if not user:
        print("User does not exist!")
    elif bcrypt.checkpw(password, user.hashed_password):
        user.delete(cur)
        print("User deleted successfully")
    else:
        print("Incorrect password")

def edit_user(cur, username, password, new_pass):
    user = User.load_user_by_username(cur, username)
    if not user:
        print("User does not")
    elif bcrypt.checkpw(password, user.hashed_password):
        if len (new_pass) < 8:
            print("Password must be at least 8 characters")
        else:
            user.hashed_password = new_pass
            user.save_to_db(cur)
            print("password changed.")
    else:
        print("Incorrect password")

if __name__ == '__main__':
    try:
        cnx = connect(database="workshop", user="postgres", password="coderslab", host="127.0.0.1")
        cnx.autocommit = True
        cursor = cnx.cursor()
        if args.username and args.password and args.edit and args.new_pass:
            edit_user(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)
        elif args.username and args.password:
            create_user(cursor, args.username, args.password)
        elif args.list:
            list_user(cursor)
        else:
            parser.print_help()
        cnx.close()
    except OperationalError as err:
        print("Connection Error: ", err)