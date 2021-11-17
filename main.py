import os
from flask import Flask
import pymongo
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

DB_PROJECT_NAME = os.environ.get('DB_PROJECT_NAME')
DB_NAME = os.environ.get("DB_NAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

client = pymongo.MongoClient(
    f"mongodb+srv://{DB_PROJECT_NAME}:{DB_PASSWORD}@cluster0.y0meq.mongodb.net/{DB_NAME}?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
db = client['ccp2-capstone']
mediaCollection = db['media']

for media in mediaCollection.find():
    print(media)


@app.route('/')
def index():
    return 'Hello World from Python'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
