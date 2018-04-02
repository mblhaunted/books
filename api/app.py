from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from apistar.backends import sqlalchemy_backend

from project.routes import routes as project_routes
from project.models import Base

# Boilerplate generated by apitest.

def welcome(name=None):
    if name is None:
        return {'message': 'Welcome to Redeam API Project!'}
    return {'message': 'Welcome to Redeam API Project, %s!' % name}

routes = [
    Route('/', 'GET', welcome),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

# Update our routes with our custom project_routes

routes.extend(project_routes)

# Configure the database.
# SQLAlchemy supports sqlite, mysql and postgres

settings = {
    "DATABASE": {
        "URL": "sqlite:///db.sqlite3",
        "METADATA": Base.metadata
    }
}

# Bootstrap app object with DB settings and table commands
# These are executed when "apistar create_tables" is run.

app = App(
    routes=routes,
    settings=settings,
    commands=sqlalchemy_backend.commands,
    components=sqlalchemy_backend.components)

if __name__ == '__main__':
    app.main()
