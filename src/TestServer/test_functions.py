from dbManager import dbManager

class testFunction:

    def __init__(self):
        self.db = dbManager()
        

    def connect2DB(self):
        self.db.connect()


    def createTest(self,test_id,testDetails):
        jsonData = {'test_id':test_id,
                    'test_details':testDetails}

        return self.db.insertEntry("test",jsonData)

    def getTest(self,test_id):
        query = 'select test_details from test where test_id='+test_id
        result = self.db.runQuery(query)
        if len(result)==0:
            return {"Error":"test_id Not Found "}
        result=result[0];

        return result

    def getAllTest(self):
        query = 'select test_details from test'
        result = self.db.runQuery(query)
        return result


