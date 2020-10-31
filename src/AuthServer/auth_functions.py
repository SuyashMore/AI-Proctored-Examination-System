from dbManager import dbManager

class authFunctions:

    def __init__(self):
        self.db = dbManager()
        

    def connect2DB(self):
        self.db.connect()


    def addStudent(self,id,name,email,photoURL,password):
        jsonData = {'student_id':id,
                    'name':name,
                    'email':email,
                    'photo_url':photoURL,
                    'password':password,
                    'tests_given':{'TestAmt':0}}

        return self.db.insertEntry("student",jsonData)

    def addAdmin(self,id,name,email,password):
        jsonData = {'admin_id':id,
                    'name':name,
                    'email':email,
                    'password':password,
                    'tests_created':{'TestAmt':0}}

        return self.db.insertEntry("admin",jsonData)

    def verifyStudent(self,email,password):
        query = "select email,password from student where email='"+email+"'"
        studentData = self.db.runQuery(query)
        if len(studentData)==0:
            return False
        
        studentData=studentData[0]
        if studentData['password']==password:
            return True
        return False

    def verifyAdmin(self,email,password):
        query = "select email,password from admin where email='"+email+"'"
        adminData = self.db.runQuery(query)
        if len(adminData)==0:
            return False
        
        adminData=adminData[0]
        if adminData['password']==password:
            return True
        return False

    
    def validateStudent(self,student_id,photo_url):
        return True
