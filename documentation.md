# Endpoints Documentation

### Base url: `https://mavpulsebackend.onrender.com`

## Auth

**Signup new user**
> **POST** `/auth/signup`

HTTP request Body
``` 
{
  "username": `"exampleuser"`,
  "email": `"example@example.com"`,
  "password": `"supersecret"`
}
```

<br>

**Return Values**

Success
``` 
response_data = {
    "message": "user successfully created!",
    "access_token": access_token,
    "expires_at": expires_at,
    "expires_in": expires_in,
    "refresh_token": refresh_token,
    "user_id": user_id,
    "username": username
}
```

<br>
<br>

**Login user**
> **POST** `/login`

**Body**
```  
{
    "email": `"example@example.com"`,
    "password": `"password"`,
}
```

<br>

**Return Values**

Success
``` 
{
    "accessToken": accessToken,
    "user_id": user_id
    "response": "200",
    "username": username,
}
```
<br>

**NOTE**: Any further calls to below endpoint require `access_token` in the header.
Every api call needs to have header field:
note the extra space after "Bearer"
``` 
header: {
    "Authorization": "Bearer " + access_token
}
```

<br>
<br>

## Courses

**Returns all departments**
> **GET** `/courses`

<br>

**Return Values**

On success, returns array of all departments objects
``` 
[ 
    {
        "department": "Accounting ",
        "id": id
    }, 
    {
        "department": "Advertising ",
        "id": id
    } 
]
```


<br>

**Optional parameters**:
`limit` - only returns requested amount
`offset` - offset from begginning

Example with `limit` and `offset`
> **GET** `/courses?limit=3&offset=4`

**Return Values**

On success, would return **3** department objects skipping the first **4**

<br>
<br>

**Returns all courses for given department**
> **GET** `/courses{department}`

<br>

**Return Values**

On success, returns array of all courses, in this example for Accounting (first 3).
``` 
[ 
  {
    "course_code": "ACCT 2301",
    "course_name": "PRINCIPLES OF ACCOUNTING I",
    "course_name_backend": "ACCT 2301  PRINCIPLES OF ACCOUNTING I"
  },
  {
    "course_code": "ACCT 2302",
    "course_name": "PRINCIPLES OF ACCOUNTING II",
    "course_name_backend": "ACCT 2302  PRINCIPLES OF ACCOUNTING II"
  },
  {
    "course_code": "ACCT 2303",
    "course_name": "ACCOUNTING AND COMPLIANCE OF NON-PROFIT ORGANIZATIONS",
    "course_name_backend": "ACCT 2303  ACCOUNTING AND COMPLIANCE OF NON-PROFIT ORGANIZATIONS"
  },
]
```

<br>
<br>

## Events

<br>

**Get all events**
> **GET** `/events`


<br>

**Optional parameters**:
`limit` - only returns requested amount
`offset` - offset from begginning


<br>

**Return values**

```
[
    {
        "course_id": string (null for now),
        "created_at": string,
        "date": string,
        "event_id": string,
        "image_url": string,
        "title": string,
        "type": "upcoming" or "trending"
    },
    ...
]

```


<br>
<br>

## Rooms

**Get all rooms for a course**
> **GET** `/rooms/{course_name_backend}`


<br>

**Return Values**

On success, returns an array of room objects
``` 
[
    {
        "members": 5,
        "owner": "spongebob",
        "room_id": room_id,
        "room_name": "calc 3 final"
    },
    {
        "members": 3,
        "owner": "tim",
        "room_id": room_id,
        "room_name": "lock in"
    }
]
```

<br>

**Optional parameters**:
`limit` - only returns requested amount
`offset` - offset from begginning

<br>
<br>

**Create chat room**
> **POST** `/rooms/new_room`

<br>

**Request Body**

```  
{
    "course_id": string,
    "creator_id": string,
    "name": string,
    "role": "owner",
    "encrypted_room_key": string,
}
```

<br>

**Return Values**
Returns object with `member` and `room` objects

```  
{
    "member": {
        "encrypted_room_key": string
        "joined_at": string
        "role": string
        "room_id": string
        "user_id": string
    },
    "room": {
        "course_id": string
        "created_at": string
        "creator_id": string
        "id": string
        "room_name": string
        "size": 1
    }
}
```

<br>
<br>

**Request to join room**
> **POST** `/rooms/{room_id}`

<br>

**Request Body**

**`requester_key` is the user's public key**
**You should make this call when user clicks on a room**
```  
{
    "requester_key": requester_key,
    "requester_name": requester_name,
    "requester_id": requester_id       
}
```

<br>

**Return Values**
**If user was granted access, then once user clicks on room, backend returns this**

<br>

```
{
    "course_id": string,
    "creator_id": string,
    "name": string,
    "role": "owner",
    "encrypted_room_key": string,
    "joined_at": string
}
```

**Get pending requests**
>**GET** `rooms/{room_id}/{user_id}/`

<br>

**Return Values**
**Use the `requester_key` to encrypt the room key and that will be what u use in the post request to accept a request**

```
[
    {
        "request_id": string,
        "requester_id": string,
        "requester_key": string,
        "requester_name": "owner",
        "room_id": string,
    }
]
```

<br>
<br>


**Accept request to join room**
> **POST** `rooms/{room_id}/{request_id}`

<br>

**Request body**

```
{
    "user_id": string,
    "encrypted_key": string,
}

```

<br>
<br>


**Send a message**
> **POST** `/rooms/chat/{room_id}`

<br>

**Request Body**
**Note that user only can send max of `500` messages, and each room only can have `300` messages**


```
{
    "sender_id": string,
    "content": string,
    "sender_name": string
}
```

<br>
<br>


**Get chat from a room**
> **GET** `/rooms/chat/{room_id}`

<br>

**Return Values**

On success, return array of messages, ordered from newest to oldest
```
[
    {
        "content": "I'm ready!",
        "message_id": message_id,
        "timestamp": "2025-11-14T00:07:30.81251+00:00",
        "user_id": user_id,
        "username": "spongebob"
    },
    {
        "content": "lock in lads",
        "message_id": message_id,
        "timestamp": "2025-11-14T00:06:41.852963+00:00",
        "user_id": user_id,
        "username": "krabs"
    }
]
```


<br>

**Optional parameters**:
`limit` - only returns requested amount
`offset` - offset from begginning

<br>
<br>

**Delete a message**
> **DELETE** `/rooms/chat/{message_id}

<br>

**For now, can only delete one message per request**
**Return Values**

On success

```
{
    "content": string,
    "created_at": string,
    "message_id": string,
    "room_id": string,
    "sender_id": string,
    "sender_name": string
}

```

<br>
<br>

## Notes

**Upload Notes to a room**
> **POST** `/rooms/{room_id}/files`

<br>

**Request Body**
**Must use multipart/form-data, NOT JSON, max of 6MB file size**
```  
{
    "is_public": boolean,
    "title": string,
    "file: file,
    "course_name": course_name_backend,
    "user_id": string,
    "room_id": string
}
```

<br>

**Return Values**


```
[
    {
        "bucket_path": string,
        "course_name": string,
        "created_at": 2025-11-22T18:07:11.756136+00:00,
        "file_path": string,
        "is_public": boolean,
        "note_id": string,
        "room_id": string,
        "title": string,
        "user_id": string
    }
]
```

`bucket_path` - you can ignore this
`file_path` - actual path for note

<br>
<br>

**Upload notes to a course**

> **POST** `/courses/{course_name_backend}/files`

<br>

**Request Body**

```
{
    "course_name": string,
    "file_path": string,
    "title": string,
    "user_id": string
}
```

<br>

**Return Values**

```
[
    {
        "bucket_path": string,
        "course_name": string,
        "created_at": "2025-11-22T21:37:49.931821+00:00",
        "file_path": string,
        "is_public": true,
        "note_id": "f8811d62-10bb-451f-920e-7afe719b6fea",
        "room_id": null,
        "title": string,
        "user_id": string
    }
]
```

<br>
<br>

**Get Notes from a course (includes notes submitted inside room that are public)**
> **GET** `/courses/{course_name_backend}/files`

<br>

**Return Values**


```
[
    {
        "bucket_path": string,
        "course_name": string,
        "created_at": 2025-11-22T18:07:11.756136+00:00,
        "file_path": string,
        "is_public": boolean,
        "note_id": string,
        "room_id": string,
        "title": string,
        "user_id": string
    },
    {
        "bucket_path": string,
        "course_name": string,
        "created_at": 2025-11-22T18:07:11.756136+00:00,
        "file_path": string,
        "is_public": boolean,
        "note_id": string,
        "room_id": string,
        "title": string,
        "user_id": string
    },
    ...
]
```


<br>
<br>

**Delete Notes**
> **DELETE** `/courses/{note_id}`

**Return Values**

On Success, returns success message and file is deleted of database

```
{
    "response": "successfully deleted note"
}
```

<br>
<br>

## Notes

<br>

**Get all notes that user has uploaded**

> **GET** `/user/notes/{user_id}`

<br>

**Return Values**
Returns array of objects
```
[
    {
        "bucket_path": string,
        "course_name": string,
        "created_at": "2025-11-22T20:25:47.733712+00:00",
        "file_path": string,
        "is_public": boolean,
        "note_id": string,
        "room_id": string,
        "title": string,
        "user_id": string
    },
    ...
]
```

<br>
<br>

**Favorite a note**

> **POST** `user/favorites`

<br>

**Request Body**

```
{
   "user_id": "f3ece1c9-90e5-4825-a40e-060a7b7c1165",
   "note_id": "f2881202-8aaf-401d-a2f4-f259069a7135"
}
```

<br>

**Return Values**

```
{
    "favorite_id": string,
    "note_id": string,
    "user_id": string
}
```

<br>
<br>

**Get favoritted notes**

> **GET** `user/favorites/{user_id}`

<br>

**Return Values**

```
[
    {
        "note_id": string,
        "notes": {
            "bucket_path": string,
            "course_name": string,
            "created_at": string,
            "file_path": string,
            "is_public": boolean,
            "note_id": string,
            "room_id": string (can be null),
            "title": string,
            "user_id": string
        }
    },
    ...
]

```
