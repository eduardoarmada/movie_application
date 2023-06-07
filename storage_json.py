from istorage import IStorage
import json
import os


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path
        if file_path not in os.listdir():
            with open(file_path, "w") as fileobj:
                fileobj.write("")

    def list_movies(self):
        """
            Returns a dictionary of dictionaries that
            contains the movies information in the database.

            The function loads the information from the JSON
            file and returns the data.

            For example, the function may return:
            {
              "Titanic": {
                "rating": 9,
                "year": 1999
              },
              "..." {
                ...
              },
            }
            """
        with open(self.file_path, "r") as fileobj:
            return json.loads(fileobj.read())

    def add_movie(self, title, year, rating, poster):
        """
            Adds a movie to the movie database.
            Loads the information from the JSON file, add the movie,
            and saves it. The function doesn't need to validate the input.
            """
        json_data = self.list_movies()
        json_data[title] = {"rating": rating, "year": year, "poster": poster}
        with open(self.file_path, "w") as fileobj:
            fileobj.write(json.dumps(json_data))

    def update_movie(self, title, rating):
        """
            Updates a movie from the movie database.
            Loads the information from the JSON file, updates the movie,
            and saves it. The function doesn't need to validate the input.
            """
        json_data = self.list_movies()
        json_data[title] = {"rating": rating, "year": json_data[title]["year"], "poster": json_data[title]["poster"]}
        with open(self.file_path, "w") as fileobj:
            fileobj.write(json.dumps(json_data))

    def delete_movie(self, title):
        """
            Deletes a movie from the movie database.
            Loads the information from the JSON file, deletes the movie,
            and saves it. The function doesn't need to validate the input.
            """
        json_data = self.list_movies()
        del json_data[title]
        with open(self.file_path, "w") as fileobj:
            fileobj.write(json.dumps(json_data))



