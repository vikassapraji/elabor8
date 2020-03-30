import unittest2 as unittest
import logging
import unidecode
import inspect
import csv
import json
from RESTRequests import REST

logFileName="testCats.log"
logging.basicConfig(filename=logFileName,
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
logger = logging.getLogger()


url = "https://cat-fact.herokuapp.com"
restRequest = REST()

class CatsData:
    def __init__(self, _id, text, type,userId,userFirstName,userLastName,upVotes,userUpVoted):
        self._id = _id
        self.text = text
        self.type = type
        self.userId = userId
        self.userFirstName = userFirstName
        self.userLastName = userLastName
        self.upVotes = upVotes
        if userUpVoted=='null':
            userUpVoted=None
        self.userUpVoted = userUpVoted
    def __str__(self):
        return self._id + "," + self.text+"," + self.type

catsFile = "Test Automation - Dataset.csv"
f = open(catsFile, "r")
reader = csv.DictReader(f, delimiter=',')
catsRecords = {}
for row in reader:
    catsRecords[row['_id']] = CatsData(row['_id'], row['text'].encode('cp1252').decode('utf-8'), row['type'], row['user.id'],
                           row['user.name.first'], row['user.name.last'],
                           row['upvotes'], row['userUpvoted'])



class testCats(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        funcName = inspect.stack()[0][3]
        self.printDebug(funcName)

    def tearDown(self):
        funcName = inspect.stack()[0][3]
        self.printDebug(funcName)

    def printDebug(self, msg):
        logger.debug(msg)

    #@unittest.skip('')
    def test_1_GetAllCats(self):
        testCaseName = inspect.stack()[0][3]
        self.printDebug("Executing : " + testCaseName)
        route = url+"/facts"
        response = restRequest.doGetRequest(route)
        logger.debug("Response=" + json.dumps(json.loads(response.text), indent=4))
        catsResponse = json.loads(response.text)['all']
        catsResponseDict = dict([(x['_id'], x) for x in catsResponse])
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(catsResponse) >= len(catsRecords))
        for id, catRecord in catsRecords.items():
            catResponse = catsResponseDict[catRecord._id]
            self.assertTrue(catResponse['type'] == catRecord.type)
            self.assertTrue(catResponse['user']['_id'] == catRecord.userId)
            self.assertTrue(catResponse['user']['name']['first']== catRecord.userFirstName)
            self.assertTrue(catResponse['user']['name']['last'] == catRecord.userLastName)
            self.assertTrue(int(catResponse['upvotes']) >= int(catRecord.upVotes))
            self.assertTrue(catResponse['userUpvoted'] == catRecord.userUpVoted)
            self.assertEqual(catRecord.text,catResponse['text'])

    #@unittest.skip('')
    def test_2_GetACat(self):
        testCaseName = inspect.stack()[0][3]
        self.printDebug("Executing : " + testCaseName)
        for id,catRecord in catsRecords.items():
            route = url + "/facts/"+catRecord._id
            response = restRequest.doGetRequest(route)
            logger.debug("Response="+json.dumps(json.loads(response.text), indent=4))
            catResponse = json.loads(response.text)
            self.assertTrue(response.status_code == 200)
            self.assertTrue(catRecord._id == catResponse["_id"])
            self.assertTrue(catResponse["type"]=="cat")
            self.assertTrue(catRecord.userId == catResponse["user"])
            self.assertEqual(catRecord.text, catResponse['text'])
            self.assertTrue(catResponse["used"] == False)
            self.assertTrue(catResponse["source"] == "user")
            self.assertTrue(catResponse["deleted"] == False)
            self.assertTrue(catResponse["__v"] == 0)
            #self.assertTrue(catResponse["status"]["verified"] == True)
            #self.assertTrue(catResponse["status"]["sentCount"] == 1)

    #@unittest.skip('')
    def test_3_GetNonExistentCat(self):
        testCaseName = inspect.stack()[0][3]
        self.printDebug("Executing : " + testCaseName)
        invalidCats = ['123','cat','-1','0','999','@#']
        for invalidCat in invalidCats:
            route = url + "/facts/"+invalidCat
            response = restRequest.doGetRequest(route)
            self.assertTrue(response.status_code == 400)


def suite():
        tests = ['test_1_GetAllCats','test_2_GetACat','test_3_GetNonExistentCat']
        return unittest.TestSuite(map(testCats, tests))


if __name__ == '__main__':
    unittest.main()