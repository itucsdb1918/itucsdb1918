# USER DATA MODEL CLASS

class User:
    def __init__(self, userId, userName, password, firstName, lastName, schoolName, campusName):
        self.userId = userId
        self.userName = userName
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.schoolName = schoolName
        self.campusName = campusName
