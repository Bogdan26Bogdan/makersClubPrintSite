from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def connect_to_db(user: str, password: str):
    """This returns the client object for mongoDB,
    with the given username and password
    """

    uri = f"mongodb+srv://{user}:{password}@makersclub-testing.fgocnhe.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi("1"))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    print("There are no current reasons to run this file")
