# Internet Movie Pythonbase

> Any resemblance to real persons or names is purely coincidental.

Simple REST API - a basic movie database interacting with external API.

There are 3 endpoints:

- `/movies` - to search for details about particular movie or get list of all 
movies present in application database,
- `/comments` - to add comments for movies already present in application 
database,
- `/top` - to get ranking of movies in application database based on number of 
comments.

Details about movies are retrieved from 
[OMDb - The Open Movie Database](https://www.omdbapi.com/). Application tries 
to limit queries to external API by saving made queries that point to given 
movie so consecutive requests with the same title use data already stored in 
application database.

Details about application's possibilities are documented in **Endpoints** 
section.

## Tools and frameworks

### Django

Why? Well, let's take a look at Django's main page:

> Django makes it easier to build better Web apps more quickly and with less 
> code.

and

> The web framework for perfectionists with deadlines.

Django makes it easy to implement and control web app without much boilerplate. 
With it's ORM defining domain objects and controlling them is straightforward 
and butter-smooth.

### Django REST Framework

If Django and REST API, then DRF is a given. It build on top of Django for even
better and more robust approach for creating web apps implementing REST API.

### PostgreSQL

> The World's Most Advanced Open Source Relational Database

Battle tested database system with performance and robustness in mind. It 
scales well and works perfectly with Django.

### Docker

'Strange, it works on my machine.' killer. Makes deployment easy and platform 
independent. Ideal for work on web apps which can have parts of the system 
running on different servers. Allows isolation of assets and portability of 
code.

### pytest

> The pytest framework makes it easy to write small tests, yet scales to 
> support complex functional testing for applications and libraries.

Unit testing in python was never easier. Ties in with django nicely by 
`pytest-django` with mocking sponsored by `pytest-mock` which enables easy use 
of `mock` library in `pytest` context.

## Installation

You have to create `docker/env/dev.env` file in existing `docker/` directory.
File should have following environmental variables defined:

```
POSTGRES_HOST=postgres_dev
POSTGRES_DB=<postgres_db_name>
POSTGRES_USER=<postgres_user>
POSTGRES_PASSWORD=<postgres_password>
ALLOW_IP_RANGE=0.0.0.0/0
DJANGO_SECRET=<your_secret_value>
OMDB_KEY=<your_omdb_api_key>
```

Specific values are left to you. `POSTGRES_HOST` value can be changed but it 
has to match docker container with PostgreSQL. (If you have no idea about 
docker leave it as it is). You can get free OMDB API key at 
[www.omdbapi.com](https://www.omdbapi.com/apikey.aspx) that allows 1,000 
requests per day.

Provided Docker images and scripts allow easy start with:

```bash
$ ./docker/run-manage.sh createsuperuser
$ ./docker/run-manage.sh makemigrations
$ ./docker/run-manage.sh migrate
$ ./docker/run-server.sh
```

To access bash use: 

```bash
$ ./docker/run-bash.sh
``` 

To run tests:

```bash
$ ./docker/run-pytest.sh
```

## Endpoints

### 1. Movies

#### `POST /movies`

Based on passed title, movie details are fetched from 
[www.omdbapi.com](http://www.omdbapi.com/) and saved to application database. 
Title does not have to be exact, it is case insensitive. OMDB API returns best 
match. Queried title is saved in database in `Movie.tags` for later retrieval 
of similar queries without calling external OMDB API.

##### Request

​Request body has to contain movie title as JSON, example:

```json
{
	"title": "Scott Pilgrim" 
}
```

##### Response - `HTTP 201 Created`

Returned when movie details were fetched correctly and saved in database. 
Response includes movie object as JSON with `id`, `tags` and with all data 
fetched from external API as `details`.

```json
{
    "id": 7,
    "tags": [
        "scott pilgrim"
    ],
    "details": {
        "title": "Scott Pilgrim vs. the World",
        "year": "2010",
        "rated": "PG-13",
        "released": "13 Aug 2010",
        "runtime": "112 min",
        "genre": "Action, Comedy, Fantasy, Romance",
        "director": "Edgar Wright",
        "writer": "Michael Bacall (screenplay), Edgar Wright (screenplay), Bryan Lee O'Malley (Oni Press graphic novels)",
        "actors": "Michael Cera, Kieran Culkin, Anna Kendrick, Alison Pill",
        "plot": "Scott Pilgrim must defeat his new girlfriend's seven evil exes in order to win her heart.",
        "language": "English",
        "country": "USA, UK, Canada, Japan",
        "awards": "17 wins & 62 nominations.",
        "poster": "https://m.media-amazon.com/images/M/MV5BMTkwNTczNTMyOF5BMl5BanBnXkFtZTcwNzUxOTUyMw@@._V1_SX300.jpg",
        "ratings": [
            {
                "source": "Internet Movie Database",
                "value": "7.5/10"
            },
            {
                "source": "Rotten Tomatoes",
                "value": "81%"
            },
            {
                "source": "Metacritic",
                "value": "69/100"
            }
        ],
        "metascore": "69",
        "imdb_rating": "7.5",
        "imdb_votes": "334,787",
        "imdb_id": "tt0446029",
        "type": "movie",
        "dvd": "09 Nov 2010",
        "box_office": "$31,494,270",
        "production": "Universal Pictures",
        "website": "http://www.scottpilgrimthemovie.com",
        "response": "True"
    }
}
```

##### Response - `HTTP 302 Found`

Returned if movie matching query already exists in database. Response includes 
the same data as for `HTTP 201 Created` response.

##### Response - `HTTP 400 Bad Request`

Returned when there is no `title` value in request body or when it's value is 
empty.

```json
{
    "detail": "title required in request body"
}
```

##### Response - `HTTP 404 Not Found`

Returned when OMDB API did not return any movie for given title.

```json
{
    "detail": "no movie matching 'whatever some long meaningless title' found"
}
```

#### `GET /movies?tags=&released=&country=&metascore=&imdb_rating=`

Fetches list of all movies already present in application database. Allows 
filtering with query parameters by:
 
 - `tags`: string, 
 - `released`: date (YYYY-MM-DD format),
 - `country`: string,
 - `metascore`: int (0-100),
 - `imdb_rating`: float (0.0-10.0).

### 2. Comments

#### `POST /comments`

Allows adding comments to movies. ​Request has to contain ID of movie 
already present in database, and comment text body.

##### Request

Request has to contain `movie_id` and `text` as JSON:

```json
{
    "text": "That was very pleasant screening, 10/10 would recommend.",
    "movie_id": 1
}
```

##### Response - `HTTP 201 Created`

Returned when movie for given ID was found and comment was saved. Response 
contains comment object with `movie_id`, `text` and creation date as `created`.

```json
{
    "text": "That was very pleasant screening, 10/10 would recommend.",
    "created": "2019-04-12",
    "movie_id": 1
}
```

##### Response - `HTTP 400 Bad Request`

Returned when no movie with given ID exists in database:

```json
{
    "movie_id": [
        "Invalid pk \"21435264\" - object does not exist."
    ]
}
```

or when request body does not contain one or both of required values:

```json
{
    "text": [
        "This field is required."
    ],
    "movie_id": [
        "This field is required."
    ]
}
```

#### `GET /comments?movie_id=&created=`

Fetches list of all comments present in application database. Allows filtering 
with query parameters by:

- `movie_id`: int,
- `created`: date (YYYY-MM-DD format)

### 3. Top

#### `GET /top?from_date=YYYY-MM-DD&to_date=YYYY-MM-DD`

Returns ranking of movies present in the database based on a number of 
comments added to the movies in the specified date range. Movies with the same 
number of comments have the same rank. Movies without comments are also 
included with last rank.

Request **requires** date range query parameters:

- `from_date`: date (YYYY-MM-DD format),
- `to_date`: date (YYYY-MM-DD format).

Response includes 
`movie_id`, `total_comments` count and `rank`.

Example response:

```
[
    {
        "movie_id": 1,
        "total_comments": 4,
        "rank": 1
    },
    {
        "movie_id": 4,
        "total_comments": 2,
        "rank": 2
    },
    {
        "movie_id": 2,
        "total_comments": 2,
        "rank": 2
    },
    {
        "movie_id": 6,
        "total_comments": 0,
        "rank": 3
    },
    {
        "movie_id": 3,
        "total_comments": 0,
        "rank": 3
    }
]
```
