from dotenv import load_dotenv
load_dotenv()

import os 
username = os.environ.get("username") 
password = os.environ.get("password")

import connect
connect.connect_to_db(username, password)
