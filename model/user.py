# USER DATA MODEL CLASS

class User:
    def __init__(self, id=-1, username="", email="", password="", firstname="", lastname="", schoolid="", campusName="", wishlistId=-1):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.schoolid = schoolid
        self.campusName = campusName
        self.wishlistId = wishlistId

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
    def setSchoolid(self,schoolName):
        self.schoolid = schoolid
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
    def getSchoolid(self):
        return self.schoolid
    def getCampusName(self):
        return self.campusName
    def getWishlistId(self):
        return self.wishlistId
