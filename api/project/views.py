from datetime import datetime

from apistar.http import Response
from apistar.backends.sqlalchemy_backend import Session

from project.models import BookModel
from project.types import Book as BookType

def list_books(session: Session) -> Response:
    queryset = session.query(BookModel).all()
    return [
        {'id': book.id, 'title': book.title, 'checked_out': book.checked_out}
        for book in queryset
    ]

def patch_book(session: Session, book_id: int, checked_out: bool) -> Response:
    book = session.query(BookModel).get(book_id)
    book.checked_out = checked_out
    session.commit()
    session.flush()
    return {'id': book.id, 'title': book.title, 'checked_out': book.checked_out}

def add_book(session: Session, book: BookType) -> Response:
    try:
        publish_date = datetime.strptime(book.get('publish_date'), '%Y-%m-%d').date()
    except ValueError:
        return(Response({'publish_date': 'invalid date. use YYYY-MM-DD'}, status=400))
    new_book = BookModel(
        title=book.get('title'),
        author=book.get('author'),
        publisher=book.get('publisher'),
        publish_date=publish_date,
        rating=book.get('rating'),
        checked_out=book.get('checked_out')
    )
    session.add(new_book)
    session.commit()
    return {'id': new_book.id, 'title': new_book.title, 'checked_out': new_book.checked_out}

def delete_book(session: Session, book_id: int) -> Response:
    book = session.query(BookModel).get(book_id)
    session.delete(book)
    session.flush()
    return {'id': book.id, 'title': book.title}
