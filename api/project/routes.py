from apistar import Include, Route
from project.views import list_books, add_book, delete_book, patch_book

book_routes = [
    Route('/', 'GET', list_books),
    Route('/', 'POST', add_book),
    Route('/{book_id}/', 'DELETE', delete_book),
    Route('/{book_id}/', 'PATCH', patch_book),
]

routes = [
    Include('/book', book_routes),
]
