# E-Mina Backend API Endpoints Documentation

### / - root path

Parameter: None

Result: You reached backend server for E-Mina

### POST /api/auth

Parameter: JSON in request body with following format

Result: Token will expire in 31 days

```json
{
	"_id":"<userId>",
	"email":"<email>"
}
```

Successful response:

```json
{
    "data": {
        "token": "<token>",
        "user": {
            "_id": "61af603bb6d8c8f8041bbff3",
            "bio": "no bio",
            "bookmarks": ["<array of locations>"],
            "email": "<email>",
            "user_content": [],
            "user_id": "61af603bb6d8c8f8041bbff3",
            "username": "<username>"
        }
    },
    "message": "user authenticated",
    "status": "successful"
}
```

Unsuccessful response:

```json
{
    "data": {},
    "message": "invalid login details",
    "status": "fail"
}
```

### GET /api/media

Parameter: None

Result: Return all media results 

Example:

```bash
{URL}/api/media
```

Successful response (Excerpt):

```json
[
   {
      "id":13916,
      "name":"Death Note",
      "overview":"Light Yagami is an ace student with great prospects\u2014and he\u2019s
bored out of his mind. But all that changes when he finds the Death Note, a notebook dropped by a rogue Shinigami death
god. Any human whose name is written in the notebook dies, and Light has vowed to use the power of the Death Note to rid
the world of evil. But will Light succeed in his noble goal, or will the Death Note turn him into the very thing he
fights against?",
      "poster_path":"/iigTJJskR1PcjjXqxdyJwVB3BoU.jpg"
   }
][
   {
      "_id":"6194639dbd51c43c5d434cd7",
      "coordinates":"{latitude: 35.6852600, longitude: 139.7299368}",
      "description":"Taki has a date with Miki and the meeting point is outside Yotsuya station.",
      "media_id":[
         "372058"
      ],
      "name":"Yotsuya
Station",
      "plus_code":"MPPH+4QH Shinjuku City, Tokyo",
      "address":"1 Chome Yotsuya, Shinjuku City, Tokyo 160-0004",
      "media_pic":[
         "https://japantour.xyz/wp-content/uploads/2019/11/Screen-Shot-2019-11-25-at-15.41.57.png"
      ],
      "loc_pics":[
         "https://japantour.xyz/wp-content/uploads/2019/11/Screen-Shot-2019-11-25-at-15.42.19.png"
      ],
      "media_name":"Your Name",
      "location_pic":"https://upload.wikimedia.org/wikipedia/commons/3/37/Yotsuya-Sta-Akasaka.JPG"
   }
]
```

### GET /api/locations

Parameter: None

Result: Return all location results 

Example: 

```bash
{URL}/api/locations
```

Successful response (Excerpt with some example):

```json
[
   {
      "_id":"6194639dbd51c43c5d434cd7",
      "coordinates":"{latitude: 35.6852600, longitude: 139.7299368}",
      "description":"Taki has a date with Miki and the meeting point is outside Yotsuya station.",
      "media_id":[
         "372058"
      ],
      "name":"Yotsuya
Station",
      "plus_code":"MPPH+4QH Shinjuku City, Tokyo",
      "address":"1 Chome Yotsuya, Shinjuku City, Tokyo 160-0004",
      "media_pic":[
         "https://japantour.xyz/wp-content/uploads/2019/11/Screen-Shot-2019-11-25-at-15.41.57.png"
      ],
      "loc_pics":[
         "https://japantour.xyz/wp-content/uploads/2019/11/Screen-Shot-2019-11-25-at-15.42.19.png"
      ],
      "media_name":"Your Name",
      "location_pic":"https://upload.wikimedia.org/wikipedia/commons/3/37/Yotsuya-Sta-Akasaka.JPG"
   }
]
```

### GET /api/locations/<id>

Parameter: locationId

Result: Return detailed information about specific location

Example: 

```bash
{URL}/api/locations/6194639dbd51c43c5d434cd7
```

Successful Response: 

```json
[
   {
      "_id":"6194639dbd51c43c5d434cd7",
      "coordinates":"{latitude: 35.6852600, longitude: 139.7299368}",
      "description":"Taki has a date with Miki and the meeting point is outside Yotsuya station.",
      "media_id":[
         "372058"
      ],
      "name":"Yotsuya Station",
      "plus_code":"MPPH+4QH Shinjuku City, Tokyo",
      "address":"1 Chome Yotsuya, Shinjuku City, Tokyo 160-0004",
      "media_pic":[
         "https://japantour.xyz/wp-content/uploads/2019/11/Screen-Shot-2019-11-25-at-15.41.57.png"
      ],
      "loc_pics":[
         "https://japantour.xyz/wp-content/uploads/2019/11/Screen-Shot-2019-11-25-at-15.42.19.png"
      ],
      "media_name":"Your Name",
      "location_pic":"https://upload.wikimedia.org/wikipedia/commons/3/37/Yotsuya-Sta-Akasaka.JPG"
   }
]
```

### GET /api/media/<id>

Parameter: mediaId

Result: Return detailed information about specific media 

Example: 

```bash
{URL}/api/media/372058
```

Successful Response:

```json
{
   "_id":"61961f2a03bfae1317234bf1",
   "adult":false,
   "backdrop_path":"/dIWwZW7dJJtqC6CgWzYkNVKIUm8.jpg",
   "genre_ids":[
      10749,
      16,
      18
   ],
   "id":372058,
   "media_type":"movie",
   "original_language":"ja",
   "original_title":"\u541b\u306e\u540d\u306f\u3002",
   "overview":"High schoolers Mitsuha and Taki are complete strangers living separate
lives. But one night, they suddenly switch places. Mitsuha wakes up in Taki\u2019s body, and he in hers. This bizarre
occurrence continues to happen randomly, and the two must adjust their lives around each other.",
   "popularity":144.58,
   "poster_path":"/q719jXXEzOoYaps6babgKnONONX.jpg",
   "release_date":"2016-08-26",
   "title":"Your Name",
   "video":false,
   "vote_average":8.6,
   "vote_count":8051
}
```

### GET /api/media/<id>/locations

Parameter: mediaId

Result: Return all locations of given media

Example: 

```bash
{URL}/api/media/372058/locations
```

Succesful Response: 

```json
[
   {
      "_id":"6194639dbd51c43c5d434cd7",
      "coordinates":"{latitude: 35.6852600, longitude: 139.7299368}",
      "description":"Taki has a date with Miki and the meeting point is outside Yotsuya station.",
      "media_id":[
         "372058"
      ],
      "name":"Yotsuya Station",
      "plus_code":"MPPH+4QH Shinjuku City, Tokyo",
      "address":"1 Chome Yotsuya, Shinjuku City, Tokyo 160-0004",
      "media_pic":[
         "https://japantour.xyz/wp-content/uploads/2019/11/Screen-Shot-2019-11-25-at-15.41.57.png"
      ],
      "loc_pics":[
         "https://japantour.xyz/wp-content/uploads/2019/11/Screen-Shot-2019-11-25-at-15.42.19.png"
      ],
      "media_name":"Your Name",
      "location_pic":"https://upload.wikimedia.org/wikipedia/commons/3/37/Yotsuya-Sta-Akasaka.JPG"
   }
]
```

Unsuccessful Reponse (if given ID does not exist):

```json
[]
```

### POST /api/user/<userId>/location/<locationId>/photo

Parameter: mediaId and locationId

Others: user

Result: Upload photo to Google Cloud Storage and returns ObjectID of record in Mong

Example: 

```jsx
var axios = require('axios');
var FormData = require('form-data');
var fs = require('fs');
var data = new FormData();
data.append('file', fs.createReadStream('/path/to/file'));

var config = {
  method: 'get',
  url: '',
  headers: { 
    'Authorization': 'Bearer <your token>', 
    ...data.getHeaders()
  },
  data : data
};

axios(config)
.then(function (response) {
  console.log(JSON.stringify(response.data));
})
.catch(function (error) {
  console.log(error);
});
```

Succesful Response: 

```json
{
    "_id": "61e6ab9adaeb8421ec602624",
    "blob_name": "61af603bb6d8c8f8041bbff3+6194670dbd51c43c5d434ce5+20220118115922",
    "description": "This is radio Kaikan!",
    "location_id": "6194670dbd51c43c5d434ce5",
    "timestamp": "20220118115922",
    "url": "<Link of image in Cloud Storage>",
    "user_id": "61af603bb6d8c8f8041bbff3"
}
```

Unsuccessful Response (if file is not attached): 

```jsx
FileNotFoundError(2, 'No such file or directory')
```

### DELETE /api/photo/<id>

Parameter: photoId

Result: Delete photo information from database and Cloud storage

Example: 

```bash
{URL}/api/photo/61e6ab9adaeb8421ec602624
```

Successful Response (Returns PhotoID):

```json
61e6ab9adaeb8421ec602624
```

Unsuccessful Response (This is given ID does not exist). Later fix this to return 404 Error properly.

```jsx
TypeError("'NoneType' object is not subscriptable")
```

### GET /api/user/<id>/photo

Parameter: photoId

Result: Return all photo information given userId

Example: 

```bash
{URL}/api/user/61b9e964f1273900d0901224/locations
```

Successful Response:

```json
[
    {
        "_id": "61b9e9cb0d0659a9a87dca66",
        "url": "<Link of image in Cloud Storage>",
        "user_id": "61b9e964f1273900d0901224",
        "location_id": "61a33342080d12c9b9450e3e",
        "blob_name": "61b9e964f1273900d0901224+61a33342080d12c9b9450e3e+20211215131243",
        "timestamp": "20211215131243",
        "description": "Looking for my nemesis, L... 😈🤓"
    }
]
```

### GET /api/location/<id>/photo

Parameter: locationId

Result: Return all photo of specific location given id

Example: 

```bash
{URL}/api/location/61946658bd51c43c5d434ce0/photo
```

Successful Response:

```json
[
    {
        "_id": "61b9e86c0d0659a9a87dca65",
        "url": "https://storage.googleapis.com/ccp2-capstone-backend-image/619e29c9cb856caa2689ec35%2B61946658bd51c43c5d434ce0%2B20211215130651",
        "user_id": "619e29c9cb856caa2689ec35",
        "location_id": "61946658bd51c43c5d434ce0",
        "blob_name": "619e29c9cb856caa2689ec35+61946658bd51c43c5d434ce0+20211215130651",
        "timestamp": "20211215130651",
        "description": "These long underground hallways... so spooky! 😱😱😱"
    }
]
```

Unsuccessful Response (location ID does not exist). 

```json
[]
```

### GET /api/user/<id>

Parameter: userId

Result: Return user information given userId

Example: 

```bash
{URL}/api/user/61b9e964f1273900d0901224
```

Successful Response:

```json
[
    {
        "_id": "61b9e964f1273900d0901224",
        "username": "Light Yagami",
        "email": "<email>",
        "bio": "Up 2 no good 😈",
        "bookmarks": [],
        "user_content": [],
        "user_id": "61b9e964f1273900d0901224"
    }
]
```

Unsuccessful Response(if ID does not exist). Fix this later to return HTTP 404 Status.

```bash
[]
```

### GET | PATCH | DELETE /api/user/<id>/bookmarks

Parameter: userId

Result: Return all saved locations (bookmarks) of given user

Example: 

```json
{URL}/api/user/61ab23e13b7a73c8388b422c/bookmarks
```

GET

Successful Response:

```json
[
    {
        "bookmarks": [
            {
                "_id": "61a1d025080d12c9b9450e1a",
                "name": "Shirakawa Hachiman Temple",
                "coordinates": "{latitude: 36.254831, longitude: 136.905537}",
                "description": "Ep. 16",
                "location_pic": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Shirakawa-hachiman-jinja1.jpg/1280px-Shirakawa-hachiman-jinja1.jpg",
                "media_id": [
                    "31724"
                ],
                "plus_code": "7W34+W8 Shirakawa, Gifu",
                "address": "559 Ogimachi, Shirakawa, Ono District, Gifu 501-5627",
                "media_pic": [
                    "https://img.mipon.org/wp-content/uploads/2018/12/04033801/Kururugi_Shrine_Lelouch_Susaku03.jpg",
                    "https://img.mipon.org/wp-content/uploads/2018/12/04033753/Kururugi_Shrine_Susaku-1-e1544967533954.jpg"
                ],
                "loc_pics": [
                    "https://img.mipon.org/wp-content/uploads/2018/12/04033700/Kururugi-temple_CodeGeass_RealLife.jpg"
                ]
            }
        ]
    }
]
```

Unsuccessful Response (if userId does not exist):

```json
[null]
```

PATCH

Result: 

DELETE 

Result:

### GET | PATCH /api/user/<id>/profile

Parameter: userId

Example:

```bash
{URL}/api/user/61ab23e13b7a73c8388b422c/profile
```

GET 

Result:

```json
[
    {
        "username": "genkiRabbit",
        "bio": "I'm a rabbit who hopped all the way to Japan",
        "email": "<email>"
    }
]
```

PATCH 

Result: