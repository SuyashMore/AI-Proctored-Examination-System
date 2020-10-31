from borneo import NoSQLHandle, NoSQLHandleConfig, Regions
from borneo.iam import SignatureProvider
from borneo import PutRequest,GetRequest

#
# Required information:
#

# the region to which the application will connect
region = Regions.AP_MUMBAI_1

at_provider = SignatureProvider(
    tenant_id='ocid1.tenancy.oc1..aaaaaaaafbkif4taddoxvzwjjbcmbu4qrvbtv4w6s255lejfxepbx3d57a4q',
    user_id='ocid1.user.oc1..aaaaaaaat2rrjmfwb45n5due7ettqls6b4kv3wkso4zwppmkgp5cg6ejexqa',
    private_key=".oci/oci_api_key.pem",
    fingerprint='89:81:36:b8:49:90:c2:51:74:ed:92:c0:59:c8:55:4c')


#
# create a configuration object
#
config = NoSQLHandleConfig(region, at_provider)

#
# create a handle from the configuration object
#
handle = NoSQLHandle(config)



# # PutRequest requires a table name
# request = PutRequest().set_table_name('result')

# # set the value
# request.set_value({'student_id': 100, 'test_id': '3'})
# result = handle.put(request)

# # a successful put returns a non-empty version
# if result.get_version() is not None:
#    # success
#    print("Adding Value Success")
#    handle.close()

# GetRequest requires a table name
# request = GetRequest().set_table_name('result')

# # set the primary key to use
# request.set_key({'student_id': 100,'test_id': 1})
# result = handle.get(request)

# # on success the value is not empty
# if result.get_value() is not None:
#    # success
#    print("Result Received !")
#    print(result)
#    handle.close()


from borneo import QueryRequest

# Query at table named 'users" using the field 'name' where name may match 0
# or more rows in the table. The table name is inferred from the query
# statement
statement = 'select * from result where student_id = 100'
request = QueryRequest().set_statement(statement)
# loop until request is done, handling results as they arrive

result = handle.query(request)
# handle results
# handle_results(result) # do something with results
print("Result Received!")
print(result)
# if request.is_done():
handle.close()