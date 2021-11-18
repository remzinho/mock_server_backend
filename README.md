# Requirements:

<ul>
<li> python 3.8
<li> pipenv
</ul>

# How to run:
Install dependencies:
`pipenv install`

Run mocked server backend with:
`pipenv run python app.py`

Use either postman or curl or any other method to do calls against the server.


# Server description:

## Switches from one state/view to another

```
GET:
/login
/dashboard
/config
/items/{id}/details
/items/{id}/control
```

## login

Returns a randomized "token" every time the correct password is used. The token should then be used in all other calls, or the response will be 401.

```
POST /login
    body:
    {
        username: string,
        password: string
    }
```

## returns a list of items paginated/sorted/filtered
All of these are done under the dashboard view:
```
GET /items
GET /items?page=1
GET /items?page=1&pageSize=50
GET /items?page=1&pageSize=50&sortBy=date
GET /items?page=1&pageSize=50&sortBy=date&sortOrder=asc&filterField=state&filterValue=running
```

## config
Partially implemented. Missing allowed_items overwriting. Missing redirects.
```
POST/PUT/PATCH /config
    {username: xxx,
    password:  yyy,
    allowed_items: []
    }
```

All other view/state change requests besides /dashboard will redirect to either dashboard or login (if user settings changed).

## item details
Partially implemented. Missing redirects.

```
GET /items/{id}/details
    returns:
    {
        id: int,
        state: string (running/paused/stopped)
    }
```

## item control
Not implemented.
```
PUT /items/{id}
    {state: string}
```
