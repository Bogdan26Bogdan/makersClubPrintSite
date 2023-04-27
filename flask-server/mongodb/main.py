from dotenv import load_dotenv
load_dotenv()

import os 
username = os.environ.get("username") 
password = os.environ.get("password")

import database
db = database.Database(username, password)
print(db.get_all_collections())





