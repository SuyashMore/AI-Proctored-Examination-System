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

    def addAdmin(self,id,name,email,photoURL,password):
        jsonData = {'admin_id':id,
                    'name':name,
                    'email':email,
                    'password':password,
                    'tests_created':None}

        return self.db.insertEntry("admin",jsonData)

    def loginStudent(self,email,password):
        query = "select email,password from student where email="+email
        studentData = runQuery(self,query)

        # if(studentData['password']==password)
        #     return studentData['student_id']

        return None

    def loginAdmin(self,email,password):
        query = "select email,password from admin where email="+email
        adminData = runQuery(self,query)
        # if(adminData['password']==password)
        #     return adminData['student_id']
        return None
    
    def validateStudent(self,student_id,photo_url):
        return True
