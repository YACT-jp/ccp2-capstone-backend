import pymongo
from dotenv import load_dotenv
import os
import tmdbsimple as tmdb
import requests
load_dotenv()


tmdb.REQUESTS_SESSION = requests.Session()
tmdb.API_KEY = os.environ.get('tmdb_API')

stop = "y"
while stop == "y":
    # prompts user to enter the name of a movie or tv series
    search = tmdb.Search()
    q = input("Please enter media name: ")

    response = search.multi(query=q)

    print(search.results)
    # prompts user to enter to choose which result in the array yo send to DB (must enter the index num)
    result_choice = input("Please please choose the result to send to DB: ")

    DB_PROJECT_NAME = os.environ.get('DB_PROJECT_NAME')
    DB_NAME = os.environ.get("DB_NAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")

    client = pymongo.MongoClient(
        f"mongodb+srv://{DB_PROJECT_NAME}:{DB_PASSWORD}@cluster0.y0meq.mongodb.net/{DB_NAME}?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client['ccp2-capstone']
    mediaCollection = db['media']
    # inputs value into media collection in the DB
    y = mediaCollection.insert(search.results[int(result_choice)])
    print(y)

    # prompts user to ask if they will continue to search
    stop = input("Search for another media (y/n): ")
