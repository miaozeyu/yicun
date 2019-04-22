import json
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

path = os.path.join(__location__, 'db_creds')
with open(path, "r") as read_file:
    creds = json.load(read_file)


username = creds['username']
password = creds['password']
host = creds['host']
port = creds['port']
database = creds['database']