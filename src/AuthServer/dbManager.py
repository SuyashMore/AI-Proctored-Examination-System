from borneo import NoSQLHandle, NoSQLHandleConfig, Regions
from borneo.iam import SignatureProvider
from borneo import PutRequest,GetRequest
from borneo import QueryRequest

class dbManager:

    def __init__(self):
        self.region  =  Regions.AP_MUMBAI_1
        self.at_provider = SignatureProvider(
        tenant_id='ocid1.tenancy.oc1..aaaaaaaafbkif4taddoxvzwjjbcmbu4qrvbtv4w6s255lejfxepbx3d57a4q',
        user_id='ocid1.user.oc1..aaaaaaaat2rrjmfwb45n5due7ettqls6b4kv3wkso4zwppmkgp5cg6ejexqa',
        private_key=".oci/oci_api_key.pem",
        fingerprint='89:81:36:b8:49:90:c2:51:74:ed:92:c0:59:c8:55:4c')
        self.config =  NoSQLHandleConfig(self.region, self.at_provider)

    def connect(self):
        self.handle = NoSQLHandle(self.config)

    def insertEntry(self,table,jsonObj):
        request = PutRequest().set_table_name(table)
        request.set_value(jsonObj)
        print(f"Insert Entry : {jsonObj}")
        result = self.handle.put(request)
        return result

    def getEntry(self,table,jsonKey):
        request = GetRequest().set_table_name(table)
        request.set_key(jsonKey)
        result = self.handle.get(request)
        return result

    def runQuery(self,query):
        request = QueryRequest().set_statement(query)
        result = self.handle.query(request)
        return result

    def deleteEntry(self,table,jsonKey):
        request = DeleteRequest().set_table_name(table)
        request.set_key(jsonKey)
        result = self.handle.delete(request)
        return result



    def close(self):
        self.handle.close()

if __name__=="__main__":
    db = dbManager()
    db.connect()
    jsonData = {'student_id':2,
                    'name':"sss",
                    'email':"ggg",
                    'photo_url':"ppp",
                    'password':"plls",
                    'tests_given':{'test1':'hello World'}}
    result = db.insertEntry('student',jsonData)
    db.close()

