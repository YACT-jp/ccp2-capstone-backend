# E-Mina Backend API Endpoints Documentation

### / - root path

Parameter: None

Result: You reached backend server for E-Mina

### POST /api/auth

Parameter: JSON in request body with following format

Result: Token will expire in 31 days

```json
{
  "_id": "<userId>",
  "email": "<email>"
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

Token required: Yes

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

Token required: Yes

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

Token required: Yes

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
    "_id": "6194639dbd51c43c5d434cd7",
    "coordinates": "{latitude: 35.6852600, longitude: 139.7299368}",
    "description": "Taki has a date with Miki and the meeting point is outside Yotsuya station.",
    "media_id": ["372058"],
    "name": "Yotsuya Station",
    "plus_code": "MPPH+4QH Shinjuku City, Tokyo",
    "address": "1 Chome Yotsuya, Shinjuku City, Tokyo 160-0004",
    "media_pic": [
      "https://japantour.xyz/wp-content/uploads/2019/11/Screen-Shot-2019-11-25-at-15.41.57.png"
    ],
    "loc_pics": [
      "https://japantour.xyz/wp-content/uploads/2019/11/Screen-Shot-2019-11-25-at-15.42.19.png"
    ],
    "media_name": "Your Name",
    "location_pic": "https://upload.wikimedia.org/wikipedia/commons/3/37/Yotsuya-Sta-Akasaka.JPG"
  }
]
```

### GET /api/media/<id>

Token required: Yes

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

Token required: Yes

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
    "_id": "6194639dbd51c43c5d434cd7",
    "coordinates": "{latitude: 35.6852600, longitude: 139.7299368}",
    "description": "Taki has a date with Miki and the meeting point is outside Yotsuya station.",
    "media_id": ["372058"],
    "name": "Yotsuya Station",
    "plus_code": "MPPH+4QH Shinjuku City, Tokyo",
    "address": "1 Chome Yotsuya, Shinjuku City, Tokyo 160-0004",
    "media_pic": [
      "https://japantour.xyz/wp-content/uploads/2019/11/Screen-Shot-2019-11-25-at-15.41.57.png"
    ],
    "loc_pics": [
      "https://japantour.xyz/wp-content/uploads/2019/11/Screen-Shot-2019-11-25-at-15.42.19.png"
    ],
    "media_name": "Your Name",
    "location_pic": "https://upload.wikimedia.org/wikipedia/commons/3/37/Yotsuya-Sta-Akasaka.JPG"
  }
]
```

Unsuccessful Reponse (if given ID does not exist):

```json
[]
```

### POST /api/user/<userId>/location/<locationId>/photo

Parameter: mediaId and locationId

Result: Return all locations of given media

Example:

### DELETE /api/photo/<id>

Parameter: id (photoId)

Result: Delete photo information from database and Cloud storage

Example:

### GET /api/user/<id>

Parameter: id (userId)

Result: Return user information given userId

Example:

### GET /api/user/<id>/photo

Parameter: id (photoId)

Result: Return all photo information given userId

Example:

### GET /api/location/<id>/photo

Parameter: id (locationId)

Result: Return all photo of specific location given id

Example:

### GET /api/user/<id>

RParameter: id (userId)

Result: Return all users given id

Example:

### GET | PATCH | DELETE /api/user/<id>/bookmarks

GET

Parameter: id (userID)

Result: Return all saved locations (bookmarks) of given user

Example:

PATCH

Parameter: id (userID)

Result:

Example:

DELETE

Parameter: id (userID)

Result:

Example:

### GET | PATCH /api/user/<id>/profile

GET

Parameter:

Result:

PATCH

Parameter:

Result:
