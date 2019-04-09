# Internet Movie Pythonbase

> Any resemblance to real persons or names is purely coincidental.

Simple REST API - a basic movie database interacting with external API.

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

## Endpoints

### 1. Movies

#### `POST /movies`

Based on passed title, movie details are fetched from 
[www.omdbapi.com](http://www.omdbapi.com/) and saved to application database.

##### Request

​Request body contains only movie title in JSON.

```json
{
	"title": "Best Movie Ever Made" 
}
```

##### Response: 

Response includes full movie object as JSON, along with all data fetched from 
external API.

```json

```

#### `GET /movies`

​Should fetch list of all movies already present in application database.
Additional filtering, sorting is fully optional - but some implementation is a bonus.

### 2. Comments

#### `POST /comments`

​Request body should contain ID of movie already present in database, and comment text body.
Comment should be saved to application database and returned in request response.

#### `GET /comments`

​Should fetch list of all comments present in application database.
Should allow filtering comments by associated movie, by passing its ID.

### 3. Top

#### `GET /top`

​Should return top movies already present in the database ranking based on a number of comments added to the movie (as in the example) in the specified date range. The response should include the ID of the movie, position in rank and total number of comments (in the specified date range).
Movies with the same number of comments should have the same position in the ranking.
Should require specifying a date range for which statistics should be generated.

Example response:

```
[
    {
        "movie_id": 2,
        "total_comments": 4,
        "rank": 1
    },
    {
        "movie_id": 3,
        "total_comments": 2,
        "rank": 2
    },
    {
        "movie_id": 4,
        "total_comments": 2,
        "rank": 2
    },
    {
        "movie_id": 1,
        "total_comments": 0,
        "rank": 3
    }
]
```
