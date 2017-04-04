import string, random

def keygen(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

mdbHost = "localhost"
mdbPort = 27017
mdbUser = "arosiclair"
mdbPass = "cse356"
mdbName = "Fwitter"
mongoDBUri = "mongodb://{0}:{1}@{2}:{3}/{4}".format(mdbUser, mdbPass, mdbHost, mdbPort, mdbName)