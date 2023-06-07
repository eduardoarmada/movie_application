from storage_json import StorageJson
from movie_app import MovieApp
from storage_csv import StorageCsv
import random
import time

storageCSV = StorageCsv('movies.csv')
storageJSON = StorageJson("movies.json")
movie_app = MovieApp(random.choice([storageCSV, storageJSON]))

while True:
    movie_app.run()
    time.sleep(1)

