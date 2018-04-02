import random
import uuid

import pytest

from apistar.test import TestClient
from app import app, welcome

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

def test_welcome():
    data = welcome()
    assert data == {'message': 'Welcome to Redeam API Project!'}

def test_http_request(client):
    response = client.get('http://localhost/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to Redeam API Project!'}

# CRUD Tests
BOOK_URI = '/book/'
BOOK_ID = 'id'
BOOK_TITLE = 'title'
BOOK_DATE = 'publish_date'
BOOK_RATING = 'rating'
BOOK_AUTHOR = 'author'
BOOK_PUBLISHER = 'publisher'
BOOK_CHECKED_OUT = 'checked_out'
NEW_BOOK = {
    BOOK_TITLE: str(uuid.uuid1()),
    BOOK_AUTHOR: str(uuid.uuid1()),
    BOOK_PUBLISHER: str(uuid.uuid1()),
    BOOK_DATE: '2001-01-01',
    BOOK_RATING: random.choice(['1', '2', '3'])
}
RATING_MAX = 3
RATING_MAX_ERROR = 'Must be less than or equal to {}.'.format(RATING_MAX)
TOO_LONG = 'Must have no more than 256 characters.'
INVALID_DATE = 'invalid date. use YYYY-MM-DD'
NOT_FOUND = 'Not found'
DATE_CHAR_LIMIT = 10
DATE_LIMIT = 'Must have no more than {} characters.'.format(DATE_CHAR_LIMIT)
RATING_INVALID_NUMBER = 'Must be a valid number.'

def test_add_books(client):
    '''
        Add books and confirm response
    '''
    resp = client.post(BOOK_URI, NEW_BOOK)
    assert resp.status_code == 200
    assert NEW_BOOK.get(BOOK_TITLE) in resp.json()[BOOK_TITLE]
    new_book_2 = dict(NEW_BOOK)
    new_book_2[BOOK_TITLE] = 'Extra Book'
    resp = client.post(BOOK_URI, new_book_2)
    assert resp.status_code == 200
    assert new_book_2.get(BOOK_TITLE) in resp.json()[BOOK_TITLE]

def test_add_bad_book_title(client):
    '''
        Add a book with a title that's a bit too long.
    '''
    bad_book = dict(NEW_BOOK)
    bad_book[BOOK_TITLE] = bad_book.get(BOOK_TITLE) * 1000
    resp = client.post(BOOK_URI, bad_book)
    assert resp.status_code == 400
    assert resp.json().get(BOOK_TITLE) == TOO_LONG

def test_add_bad_book_date(client):
    '''
        Add a book with a bad date.
    '''
    bad_book = dict(NEW_BOOK)
    bad_book[BOOK_DATE] = bad_book.get(BOOK_TITLE)
    resp = client.post(BOOK_URI, bad_book)
    assert resp.status_code == 400
    assert resp.json().get(BOOK_DATE) == DATE_LIMIT
    bad_book = dict(NEW_BOOK)
    bad_book[BOOK_DATE] = '9999/10/01'
    resp = client.post(BOOK_URI, bad_book)
    assert resp.status_code == 400
    assert resp.json().get(BOOK_DATE) == INVALID_DATE

def test_add_bad_book_rating(client):
    '''
        Add a few books with bad ratings.
    '''
    bad_book = dict(NEW_BOOK)
    bad_book[BOOK_RATING] = 'threehundred'
    resp = client.post(BOOK_URI, bad_book)
    assert resp.status_code == 400
    assert resp.json().get(BOOK_RATING) == RATING_INVALID_NUMBER
    bad_book[BOOK_RATING] = 3000
    resp = client.post(BOOK_URI, bad_book)
    assert resp.status_code == 400
    assert resp.json().get(BOOK_RATING) == RATING_MAX_ERROR

def test_list_added_book(client):
    '''
        Ensure book added exists in database and is accessible via API
    '''
    resp = client.get(BOOK_URI)
    assert resp.status_code == 200
    book_titles = []
    for book in resp.json():
        assert book.get(BOOK_CHECKED_OUT) is False
        book_titles.append(book.get(BOOK_TITLE))
    assert NEW_BOOK.get(BOOK_TITLE) in book_titles

def test_patch_books(client):
    '''
        Ensure books can be checked out.
            NOTE:   I can (easily) change this to allow patching(updates) for the entire book model,
                    if this is what you prefer to see.

                    Currently, the CRUD operations only support "checking out" functionality.

                    If the user wants to update more than the status, that is probably a data entry
                    error and might warrant a delete/add.
    '''
    list_resp = client.get(BOOK_URI)
    for book in list_resp.json():
        assert book.get(BOOK_CHECKED_OUT) is False
        patch_uri = '{0}{1}/?{2}=True'.format(BOOK_URI, book.get(BOOK_ID), BOOK_CHECKED_OUT)
        patch_resp = client.patch(patch_uri)
        assert patch_resp.status_code == 200
    list_resp = client.get(BOOK_URI)
    for book in list_resp.json():
        assert book.get(BOOK_CHECKED_OUT) is True

def test_patch_books_false(client):
    '''
        Set all books to not checked out.
    '''
    list_resp = client.get(BOOK_URI)
    for book in list_resp.json():
        assert book.get(BOOK_CHECKED_OUT) is True
        patch_uri = '{0}{1}/?{2}='.format(BOOK_URI, book.get(BOOK_ID), BOOK_CHECKED_OUT)
        patch_resp = client.patch(patch_uri)
        assert patch_resp.status_code == 200
        assert patch_resp.json().get(BOOK_CHECKED_OUT) is False
    list_resp = client.get(BOOK_URI)
    for book in list_resp.json():
        assert book.get(BOOK_CHECKED_OUT) is False


def test_delete_books(client):
    '''
        Delete all books added and verify empty list.
    '''
    list_resp = client.get(BOOK_URI)
    for book in list_resp.json():
        assert book.get(BOOK_CHECKED_OUT) == False
        del_uri = '{0}{1}/'.format(BOOK_URI, book.get(BOOK_ID))
        del_resp = client.delete(del_uri)
        assert del_resp.status_code == 200
        assert del_resp.json()[BOOK_ID] == book.get(BOOK_ID)
    list_resp = client.get(BOOK_URI)
    assert list_resp.json() == []

def test_delete_books_bad_id(client):
    '''
        Try to delete a book that's not there.
    '''
    test_add_books(client)
    list_resp = client.get(BOOK_URI)
    for book in list_resp.json():
        assert book.get(BOOK_CHECKED_OUT) == False
        del_uri = '{0}{1}/'.format(BOOK_URI, 'ghostbusters')
        del_resp = client.delete(del_uri)
        assert del_resp.status_code == 404
        assert del_resp.json().get('message') == NOT_FOUND
        del_uri = '{0}{1}/'.format(BOOK_URI, book.get(BOOK_ID))
        del_resp = client.delete(del_uri)
        assert del_resp.status_code == 200
    list_resp = client.get(BOOK_URI)
    assert len(list_resp.json()) == 0
