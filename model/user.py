# USER DATA MODEL CLASS

class User:
    def __init__(self):
        self.id = ""
        self.username = ""
        self.email = ""
        self.password = ""
        self.firstname = ""
        self.lastname = ""
        self.schoolName = ""
        self.campusName = ""
        self.wishlistId = ""

    def setId(self, id):
        self.id = id
    def setUsername(self,username):
        self.username = username
    def setEmail(self,email):
        self.email = email
    def setPassword(self,password):
        self.password = password
    def setFirstname(self,firstname):
        self.firstname = firstname
    def setLastname(self,lastname):
        self.lastname = lastname
    def setSchoolName(self,schoolName):
        self.schoolName = schoolName
    def setCampusName(self,campusName):
        self.campusName = campusName
    def setWishlistId(self,wishlistId):
        self.wishlistId = wishlistId

    def getId(self):
        return self.id
    def getUsername(self):
        return self.username
    def getEmail(self):
        return self.email
    def getPassword(self):
        return self.password
    def getName(self):
        return self.name
    def getLastname(self):
        return self.lastname
    def getSchoolName(self):
        return self.schoolName
    def getCampusName(self):
        return self.campusName
    def getWishlistId(self):
        return self.wishlistId
