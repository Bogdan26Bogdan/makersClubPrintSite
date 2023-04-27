from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from constants import *


class Database:
    """A class for interacting with the mongoDB database"""

    def __init__(self, username: str, password: str):
        """Sets up the initial info needed for interacting with the database"""
        self.username = username
        self.password = password
        self.client = None
        self.db = None

    def _get_client(self) -> None:
        """Creates a client to communicate with mongoDB"""
        uri = f"mongodb+srv://{self.username}:{self.password}@makersclub-testing.vydjske.mongodb.net/?retryWrites=true&w=majority"

        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi("1"))

        # Send a ping to confirm a successful connection
        try:
            client.admin.command("ping")
        except Exception as e:
            print(e)
        self.client = client

    def _connect_to_db(self, database: str = DATABASE_NAME) -> None:
        """Sets up the database connection"""
        if self.client is None:
            self._get_client()
        self.db = self.client[f"{database}"]

    def _clean_connections(self) -> None:
        """Closes the connection to the DB once it is no longer being used."""
        if self.client is not None:
            self.client.close()
        self.client = None
        self.db = None

    def _check_connections(self) -> None:
        """Checks if there is a current DB connection and if there isn't it makes one."""
        if self.db is None:
            self._connect_to_db()

    def _collection_exists(self, name: str) -> bool:
        """returns true if the collection exists and false if it does not"""
        return name in self.get_all_collections()

    def get_all_collections(self) -> list[str]:
        """Returns a list of the names of all collections in the database"""
        self._check_connections()
        names = self.db.list_collection_names()
        self._clean_connections()

        return names

    def add_value(self, value):
        """Adds the data from the value to it's collection

        The class of value must have a data value that is it's name,
        and a method to_dictionary to upload

        Returns the objectID of the inserted value.
        """
        # setup a connection to the database if not already set
        self._check_connections()
        collection = self.db[value.data]

        # Check to see if it already exists
        if collection.count_documents(value.to_dictionary()):
            return None

        objectID = collection.insert_one(value.to_dictionary())

        self._clean_connections()

        return objectID

    def delete_value(self, value) -> None:
        """Deletes the specified value assuming that it exists. Nothing happens if the value does not exist."""
        self._check_connections()
        collection = self.db[value.data]

        collection.delete_one(value.to_dictionary())

        self._clean_connections()


    def find_object(
        self, collection: str, primary_key: dict, return_values: dict = None
    ) -> list[dict]:
        """Returns a list of the objects that match the key

        return values is simply a filter for what values to include in the returned list
        """
        self._check_connections()
        collection = self.db[collection]

        if return_values is not None:
            values = [x for x in collection.find(primary_key, return_values)]
        else:
            values = [x for x in collection.find(primary_key)]

        self._clean_connections()
        return values


if __name__ == "__main__":
    print("There are no current reasons to run this file")

    x = Database("username", "password")
