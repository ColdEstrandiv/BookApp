# export functions here

#TODO: initialize tables    
#querey functions
from .models import User
def getUserLibraries(userId):
    ...


def createUser(userInfo: dict):
    newUser = {
        'firstName': userInfo['firstName'],
        'lastName': userInfo['lastName'],
        'email': userInfo['email']
    }
    createUser = User.create(newUser)

if __name__ == "__main__":


    user = createUser