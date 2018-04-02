# Summary

This CRUD API leverages the [apistar](https://github.com/encode/apistar) Python 3 library to manage a list of books.

## Tool/Library Summary

* Python 3
  * `apistar` - API library
    * `sqlalchemy` - database abstraction
    * `sqlite` - selected database
* Docker
  * `docker-compose`

# Requirements

- `docker`
- `docker-compose`

# Usage

You can optionally bootstrap the environment using the following command.

`docker-compose build --no-cache`

This command should produce a few images `docker-compose` will leverage to orchestrate the process.

## Running Tests

To run tests, issue the following command.

`docker-compose run test`

NOTE: This will create a sqlite database called `db.sqlite3`in your `[project_root]/api/` directory.

### Test Driven Development

The codebase is structured to support TDD out of the box. The test framework utilized is  `py.test`.

To begin, open `api/tests.py` and create new tests prior to adding additional functionality in the views, routes, etc.

Once you've added your desired tests and features, simply run another `docker-compose run test` to see your results.

## Running the API (local)

Similar to running tests, we leverage `docker-compose` with the following command.

`docker compose up api`

## Running the API (kubernets)

A helm chart has been provided. The chart has been tested with `minikube`. The steps to deploy onto kubernetes follow.

1. Ensure your kubernetes system can access the image repository you're working with.
2. Build the images with `docker-compose`, or `docker build`. 
3. Install the helm chart from the root repo directory. `helm install --debug helm/books/`

## Running the API on "production" web server

From the apistar docs, we can leverage gunicorn to run the API with a more robust server.

```
$ pip install gunicorn
$ pip install meinheld
$ gunicorn app:app --workers=4 --bind=0.0.0.0:5000 --pid=pid --worker-class=meinheld.gmeinheld.MeinheldWorker
```

### Accessing the API

`apistar` provides a nice interface for viewing our API schema. Once your api comes up, simply navigate to `http://localhost:8080/docs/` to view all available API functionality, experiment with the API calls themselves, etc.

If you're already running the API, access the doc schema [here](http://localhost:8080/docs/).

NOTE: This will create a sqlite database called `db.sqlite3`in your `[project_root]/api/` directory.

# Design notes

While you can use `docker` to manually navigate the images and codebase, `docker-compose.yml` is provided to orchestrate running the app, tests, and for using `kompose` against to deploy the codebase to Kubernetes.

(Note, I've not yet tested converting this to k8s with `kompose`.)

The `docker-compose.yml` is designed to map the ports you'll need to access the API, and map the `[project_directory]/*` to `/app` in the container. This means the `db.sqlite3` database will be created in that directory.

If you fundamentally alter your database abstraction in `[project_directory]/api/project/models.py` you'll need to re-run your `docker compose build --no-cache` command, and remove your database file, lest your database get out of sync with your model(s).

### sqlite? wtf

I find `sqlite` fine for proof of concept purposes, and `apistar` + `SQLAlchemy` abstract the type of SQL database we use to an extent.  

It's quite possible to replace `sqlite` with `mysql` or `postgres` without changing the application codebase very much. The general steps required to do this follow.

-  Update `docker-compose.yml` to include and refer to an image that includes your desired database. 

`docker-compose.yml` (truncated example, untested)
```
  api:
  [..]
    environment:
      - DATABASE_URL=postgresql+psycopg2://foo:bar@redeam/api
      - DEBUG=True
    depends_on:
      - db

  db:
    image: postgres:9.6-alpine
    environment:
      POSTGRES_DB: "redeam"
      POSTGRES_USER: "foo"
      POSTGRES_PASSWORD: "bar"
      
```

- Update `app.py` to read from your new settings

```
settings = {
    'DEBUG': env['DEBUG'],
    'DATABASE': {
        'URL': env['DATABASE_URL'],
        'METADATA': Base.metadata,
    }
}
```

- Rebuild your images: `docker-compose build --no-cache`
- Test: `docker-compose run test`
