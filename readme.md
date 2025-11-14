# MavPulse Backend

## How to run 

### Creates docker image
`docker build -t backend .`

### Run the container
`docker run --rm backend`

### Different way to run container (No need to build image)
`docker-compose run --rm backend .`

## Debugging
you can also use venv environment

### 1. Create virtual environment:
> python3 -m venv venv

### 2. Activate virtual environment:
> source venv/bin/activate

### Linux
Some Python packages (like `psycopg2-binary`) require system dependencies on Linux.: `sudo apt install libpq-dev python3-dev build-essential`

### 3. Install project dependencies:
> pip install -r requirements.txt

### 4. To stop virtual environment:
> deactivate

## Endpoints

#### Base url: `https://mavpulsebackend.onrender.com`

### Auth

**Signup new user**
> **POST** `/auth/signup`

Body
> {
  "username": `"exampleuser"`,
  "email": `"example@example.com"`,
  "password": `"supersecret"`
}

**Return Values**

Success
> response_data = {
            "message": "user successfully created!",
            "access_token": access_token,
            "expires_at": expires_at,
            "expires_in": expires_in,
            "refresh_token": refresh_token,
}

**Login user**
> **POST** `/login`

#### Parameters
**Body**
>  {
    "email": `"example@example.com"`,
    "password": `"password"`
}

**Return Values**

Success
> {
    "accessToken": accessToken,
    "response": "200",
    "username": username
}

<br>

**NOTE**: Any further calls to below endpoint require `access_token` in the header.
Every api call needs to have header field:
note the extra space after "Bearer"
> header: {
    "Authorization": "Bearer " + access_token
}


## Courses

**Returns all departments**
> **GET** `/courses`

**Return Values**

On success, returns array of all departments objects
> [ {"department": "Accounting ","id": id}, {"department": "Advertising ", "id": id} ]


**Optional parameters**:
`limit` - only returns requested amount
`offset` - offset from begginning

Example with `limit` and `offset`
> **GET** `/courses?limit=3&offset=4`

**Return Values**

On success, would return **3** department objects skipping the first **4**


## Rooms






