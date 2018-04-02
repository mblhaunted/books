from apistar import typesystem

class BookRating(typesystem.Integer):
    minimum = 1
    maximum = 3
    default = 1

class Book(typesystem.Object):
    properties = {
        'id': typesystem.Integer,
        'title': typesystem.string(max_length=256),
        'author': typesystem.string(max_length=256),
        'publisher': typesystem.string(max_length=256),
        'publish_date': typesystem.string(max_length=10),
        'rating': BookRating,
        'checked_out': typesystem.boolean(default=False)
    }
