"""

from model.book import *
from model.user import *
from model.interchange import *


class Database:
    def __init__(self):
        self.users = {}
        self.books = {}
        self.interchangeEvents =  {}
        self._lastUserKey = 0
        self._lastBookKey = 0
        self._lastInterchangeKey = 0


    # USER METHODS
    def addUser(self, user):
        self._lastUserKey += 1
        self.users[self._lastUserKey] = user
        return self._lastUserKey

    def deleteUser(self, userKey):
        if userKey in self.users:
            del self.users[userKey]

    def getUser(self, userKey):
        user = self.users.get(userKey)
        if user is None:
            return None
        user_ = User(user.userId, user.userName, password = None,
                user.firstName, user.lastName, user.schoolName, user.campusName)
        return user_

    def get_users(self):
        users = []
        for userKey, user in self.users.items():
            user_ = User(user.userId, user.userName, password = None,
                    user.firstName, user.lastName, user.schoolName, user.campusName)
            users.append((userKey, user_))
        return users


    # BOOK METHODS
    def addBook(self, book):
        self._lastBookKey += 1
        self.books[self._lastBookKey] = book
        return self._lastBookKey

    def deleteBook(self, bookKey):
        if bookKey in self.books:
            del self.books[bookKey]

    def getBook(self, bookKey):
        book = self.books.get(bookKey)
        if book is None:
            return None
        book_ = Book(book.bookId, book.bookName, book.authorName, book.totalPages)
        return book_

    def get_books(self):
        books = []
        for bookKey, book in self.books.items():
            book_ =  Book(book.bookId, book.bookName, book.authorName, book.totalPages)
            books.append((bookKey, book_))
        return books


    # INTERCHANGE METHODS
    def addInterchange(self, interchange):
        self._lastInterchangeKey += 1
        self.interchangeEvents[self._lastInterchangeKey] = interchange
        return self._lastInterchangeKey

    def deletInterchange(self, interchangeKey):
        if interchangeKey in self.interchangeEvents:
            del self.interchangeEvents[interchangeKey]

    def getInterchange(self, interchangeKey):
        interchange = self.interchangeEvents.get(interchangeKey)
        if interchange is None:
            return None
        interchange_ = Interchange(interchange.interchangeId, interchange.lenderId, interchange.borrowerId, interchange.bookId, interchange.time)
        return interchange_

    def get_interchangeEvents(self):
        interchangeEvents = []
        for interchangeKey, interchange in self.interchangeEvents.items():
            interchange_ =  Interchange(interchange.interchangeId, interchange.lenderId, interchange.borrowerId, interchange.bookId, interchange.time)
            interchangeEvents.append((interchangeKey, interchange_))
        return interchangeEvents

"""
