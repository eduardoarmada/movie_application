from istorage import IStorage
import os


class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path
        if file_path not in os.listdir():
            with open(file_path, "w") as fileobj:
                fileobj.write("title,rating,year,poster")

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
            list_of_information = fileobj.read().split("\n")[1:]

        dict_of_movies = {}
        for movie in map(lambda x: x.split(","), list_of_information):
            title = movie[0]
            rating = movie[1]
            release_year = movie[2]
            poster = movie[3]
            dict_of_movies[title] = {"rating": rating, "year": release_year, "poster": poster}

        return dict_of_movies

    def add_movie(self, title, year, rating, poster):
        """
            Adds a movie to the movie database.
            Loads the information from the JSON file, add the movie,
            and saves it. The function doesn't need to validate the input.
            """
        movie_to_add = ",".join([title, rating, year, poster])
        with open(self.file_path, "a") as fileobj:
            fileobj.write("\n" + movie_to_add)

    def update_movie(self, title, rating):
        """
            Updates a movie from the movie database.
            Loads the information from the JSON file, updates the movie,
            and saves it. The function doesn't need to validate the input.
            """
        movies_information = self.list_movies()
        movies_information[title] = {"rating": str(rating), "year": movies_information[title]["year"],
                                     "poster": movies_information[title]["poster"]}

        string_to_add = ""
        for movie in movies_information.items():
            string_to_add += "\n"
            string_to_add += ",".join([movie[0], movie[1]["rating"], movie[1]["year"], movie[1]["poster"]])

        with open(self.file_path, "w") as fileobj:
            fileobj.write("title,rating,year,poster" + string_to_add)

    def delete_movie(self, title):
        """
            Deletes a movie from the movie database.
            Loads the information from the JSON file, deletes the movie,
            and saves it. The function doesn't need to validate the input.
            """
        movies_information = self.list_movies()
        del movies_information[title]

        string_to_add = ""
        for movie in movies_information.items():
            string_to_add += "\n"
            string_to_add += ",".join([movie[0], movie[1]["rating"], movie[1]["year"], movie[1]["poster"]])

        with open(self.file_path, "w") as fileobj:
            fileobj.write(f"title,rating,year,poster" + string_to_add)
