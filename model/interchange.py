# INTERCHANGE EVENT'S DATA MODEL CLASS

class Interchange:
    def __init__(self, interchangeId, lenderId, borrowerId, bookId, time):
        self.interchangeId = interchangeId
        self.lenderId = lenderId
        self.borrowerId = borrowerId
        self.bookId = bookId
        self.time = time
