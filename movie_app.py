import requests
import random
from coreapi.exceptions import CoreAPIException


class MovieApp:
    def __init__(self, storage, api_key="24808d93"):
        self.storage = storage
        self.API_key = api_key

    def request_info_movie_api(self, title):
        """Obtains the information of the movie requests
        if the movie is available in the API"""
        movie_info = requests.get(f"http://www.omdbapi.com/",
                                  params={"apikey": self.API_key, "t": title}).json()
        if 'Error' in movie_info:
            if movie_info['Error'] == 'Invalid API key!':
                raise CoreAPIException
            if movie_info['Error'] == 'Movie not found!':
                raise Exception
        return movie_info["Title"], movie_info["Year"], movie_info["imdbRating"], movie_info["Poster"]

    def _command_quit(self):
        """Quits the application"""
        quit()

    def _command_list_movies(self):
        """Returns a list of all the movies with their information"""
        return list(self.storage.list_movies().items())

    def _command_get_sorted_list_of_movies(self):
        """Returns a list of all the movies, ordered by rating"""
        return sorted(self.storage.list_movies(), key=lambda x: float(self.storage.list_movies()[x]['rating']), reverse=True)

    def _command_movie_stats(self):
        """Returns the mean, median, maximum and minimum of the values of the movies"""
        list_of_values = sorted([float(value['rating']) for value in self.storage.list_movies().values()])
        if len(list_of_values) % 2 == 0:
            median = (list_of_values[len(list_of_values) // 2] + list_of_values[(len(list_of_values) // 2) + 1]) / 2
        else:
            median = list_of_values[(len(list_of_values) // 2) + 1]
        return sum(list_of_values) / len(list_of_values), median, self._command_get_sorted_list_of_movies()[0], \
            self._command_get_sorted_list_of_movies()[-1]

    def _command_add_movie(self, title):
        """Access to the API and if found, adds the information of this one to the database"""
        if title in self.storage.list_movies():
            print(f"Movie {title} already exists!")
        else:
            movie_info = self.request_info_movie_api(title)
            self.storage.add_movie(movie_info[0], movie_info[1], movie_info[2], movie_info[3])
            print(title, "added to the list")

    def _command_delete_movie(self, title):
        """Deletes the movie of the database in case it is in this one"""
        if title in self.storage.list_movies():
            self.storage.delete_movie(title)
            print(f"Movie {title} successfully deleted")
        else:
            print(f"Movie {title} is not in the list")

    def _command_update_movie(self, title, rating):
        """Gives the movie the specified rating"""
        if title in self.storage.list_movies():
            self.storage.update_movie(title, rating)
            print(f"Movie {title} successfully updated")
        else:
            print(f"No movie with title \"{title}\" was found in the list")

    def _command_get_random_movie(self):
        """Returns a random movie from the list of movies"""
        return random.choice(self._command_list_movies())

    def _command_search_movie(self, title):
        """Returns a list of movies with all the movies that match the title, specified in the parameter"""
        list_of_keys = list(self.storage.list_movies().keys())
        list_of_movies_that_match = []
        for movie in list_of_keys:
            if movie.lower().startswith(title.lower()):
                list_of_movies_that_match.append(movie)
        return list_of_movies_that_match

    def _generate_website(self):
        """Generates a website with all the movies in the database"""
        string_of_html = ""
        for movie in self._command_list_movies():
            movie_title = movie[0]
            movie_year = movie[1]["year"]
            movie_img = movie[1]["poster"]
            string_of_html += f"\n<li class=\"movie\">\n<img class=\"movie-poster\" src=\"{movie_img}\" \
                alt=\"Poster of movie\"><p class=\"movie-title\" >{movie_title}</p><p class=\"movie-year\">{movie_year}</p>\n</li>\n"
        with open("_static/index_template.html", "r") as fileobj:
            html_template = fileobj.read()
        with open("_static/index.html", "w") as fileobj:
            fileobj.write(html_template.replace("__TEMPLATE_TITLE__", "Movie App").replace("__TEMPLATE_MOVIE_GRID__",
                                                                                           string_of_html))
        print("Movie website generated\n")

    def run(self):
        """Runs the movie application, obtaining the information from the specified database"""
        print("""********** My Movies Database **********

                Menu:
                0. Exit the program
                1. List movies
                2. Add movie
                3. Delete movie
                4. Update movie
                5. Stats
                6. Random movie
                7. Search movie
                8. Movies sorted by rating
                9. Generate website
                """)

        choice = int(input("Enter choice (0-9): "))

        if choice == 0:
            self._command_quit()
        elif choice == 1:
            list_of_movies = self._command_list_movies()
            for movie in list_of_movies:
                print(f"{movie[0]}: -Rating = {movie[1]['rating']}, -Year = {movie[1]['year']}")
            print()
        elif choice == 2:
            try:
                title = input("Which movie would you like to add? ")
                self._command_add_movie(title)
            except CoreAPIException:
                print("Invalid API key")
            except Exception:
                print("The movie was not found in the API")
            print()
        elif choice == 3:
            title = input("Which movie would you like to delete? ")
            self._command_delete_movie(title)
            print()
        elif choice == 4:
            title = input("Which movie would you like to update? ")
            rating = int(input("Which rating do you want to give it? "))
            self._command_update_movie(title, rating)
            print()
        elif choice == 5:
            average, median, first_value, last_value = self._command_movie_stats()
            print("Average rating: {}".format(average))
            print("Median rating: {}".format(median))
            print("Best movie: {}".format(first_value))
            print("Worst movie: {}".format(last_value))
            print()
        elif choice == 6:
            random_movie = self._command_get_random_movie()
            print(f"Your movie for tonight: {random_movie[0]}, it's rated {random_movie[1]['rating']} out of 10")
            print()
        elif choice == 7:
            title = input("Which movie are you searching for? ")
            movies_that_match = self._command_search_movie(title)
            if len(movies_that_match) == 0:
                print(f"No movie with that title was found in the list")
            else:
                for movie in movies_that_match:
                    print(f"{movie}, {self.storage.list_movies()[movie]['rating']} out of 10, released on {self.storage.list_movies()[movie]['year']}")
            print()
        elif choice == 8:
            ordered_list_of_movies = self._command_get_sorted_list_of_movies()
            for movie in ordered_list_of_movies:
                print(f"{movie}: {self.storage.list_movies()[movie]['rating']}")
            print()
        elif choice == 9:
            self._generate_website()
