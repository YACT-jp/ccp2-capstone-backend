import pymongo
from dotenv import load_dotenv
import os
import tmdbsimple as tmdb
import requests
load_dotenv()


tmdb.REQUESTS_SESSION = requests.Session()
tmdb.API_KEY = os.environ.get('tmdb_API')

search = tmdb.Search()
q = input("Please enter media name: ")
# type = input("Please input t for TV/m for movie: ")

# if type == "m":
#     response = search.movie(query=q)
# elif type == "t":
#     response = search.tv(query=q)
# else:
#     print("Invalid Input!!!")
response = search.multi(query=q)

print(search.results)

result_choice = input("Please please choose the result to send to DB: ")


DB_PROJECT_NAME = os.environ.get('DB_PROJECT_NAME')
DB_NAME = os.environ.get("DB_NAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

client = pymongo.MongoClient(
    f"mongodb+srv://{DB_PROJECT_NAME}:{DB_PASSWORD}@cluster0.y0meq.mongodb.net/{DB_NAME}?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
db = client['ccp2-capstone']
mediaCollection = db['media']

y = mediaCollection.insert(search.results[int(result_choice)])
print(y)
