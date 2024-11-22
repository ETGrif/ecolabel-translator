from pymongo import MongoClient

class DBManager:

    def init_database(self):
        """
        Establishes and verifies connection to the database

        MUST be called before any other DB functions
        """
        try:
            self.database_client = MongoClient("mongodb://db.benjaminapplegate.com:25567")
            self.db = self.database_client.ecolabelDb
            self.testCollection = self.db.testing
            self.ecolabelCollection = self.db.ecolabels

            print(f"Found Collections: {self.db.list_collection_names()}")

            self.database_client.admin.command("ping")
            print("Database connected properly")
        except Exception as e:
            print("Failed to connect to database")

    def close_database_connection(self):
        """
        Closes database connection, should be called before app closes
        """
        self.database_client.close()

    def insert_testing_document(self, data):
        """
        Inserts a document into the testing database

        Args:
            data (dictionary): The data to store in the database

        Returns:
            ID of the newly inserted document
        """
        result = self.testCollection.insert_one(self, data)
        print("Inserted document ID: ", result.inserted_id)
        return result.inserted_id

    def get_all_testing_documents(self):
        return self.testCollection.find()

    def insert_ecolabel(self, data):
        """
        Inserts a document into the ecolabel database

        Args:
            data (dictionary): The data to store in the database

        Returns:
            ID of the newly inserted document
        """
        result = self.ecolabelCollection.insert_one(data)
        print("Inserted document ID: ", result.inserted_id)
        return result.inserted_id

    def get_all_ecolabels(self):
        """
        Fetches all ecolabels stored in the database

        Returns:
            A pymongo collection of documents (iterable)
        """
        return self.ecolabelCollection.find()

    def get_ecolabel_by_name(self, name):
        """
        Searches ecolabel database for document with a name field provided

        Args:
            name (string) - The name of the ecolabel stored in the database to fetch

        Returns:
            A pymongo document
        """
        result = self.ecolabelCollection.find_one({"name": name})
        return result

    def search_ecolabels_by_name(self, pattern):
        """
            Searches ecolabel database for all documents where the name matches the provided pattern

            Args:
                pattern (string) - A pattern to search through the names with
                NOTE: While pattern can just be a string to search for, it can be a regular expression if needed for more advanced searches
            Returns:
                A pymongo collection of documents (iterable)
        """
        matching_documents = self.ecolabelCollection.find({"name": {"$regex": pattern, "$options": "i"}})
        return matching_documents

if __name__ == "__main__":
    manager = DBManager()
    manager.init_database()
    print(manager.get_all_testing_documents())
    manager.close_database_connection()