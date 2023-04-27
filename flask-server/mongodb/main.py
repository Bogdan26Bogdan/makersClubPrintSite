from dotenv import load_dotenv
load_dotenv()

import os 
username = os.environ.get("username") 
password = os.environ.get("password")

import database
db = database.Database(username, password)



import sys
script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir, '..', ".." , "classes")
sys.path.append( mymodule_dir )
import printer



x = printer.Printer("1", "Working")
print(f"Object id of the newly added printer: {db.add_value(x)}")
print(db.find_object(x.data, {"ID": "1"}))



print(db.get_all_collections())





