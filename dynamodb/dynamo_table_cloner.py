#===============================================================================#
#   Dynamo Table Cloner v 1.0                                                   #        
#                                                                               #
#   DynamoDB Script for table cloning                                           #
#                                                                               #
#   How to use:                                                                 #
#   - On the command line type:                                                 #
#   > python dynamo_table_cloner.py <table_name> <environment> copy             #
#                                                                               #
#   Auhor: Wagner Alves                                                         #                                         
#   Date : 28/03/2018                                                           #
#===============================================================================#

from __future__ import print_function # Python 2/3 compatibility
import boto3
import datetime
from time import sleep
import sys

if len(sys.argv) < 3:
    print('Usage: %s <source_table_name> <environment> copy' % sys.argv[0])
    sys.exit(1)

# input parameters
src_table_name = sys.argv[1]
environment = sys.argv[2]

copy_data = None
if len(sys.argv) > 3:
    copy_data = sys.argv[3]

## DynamoDB Client Configuration
#boto3.setup_default_session(profile_name=environment)
#client = boto3.client('dynamodb',region_name='us-east-1')

client = boto3.client('dynamodb')

dynamodb = boto3.resource('dynamodb',region_name='us-east-1') 

# 1. Read and copy the target table to be copied
table_struct = None
try:
    table = dynamodb.Table(src_table_name)
    print("Profile:"+environment)
    print(">>>>> Source Table: " + src_table_name)
    table_struct = client.describe_table(TableName=src_table_name)
    print(table_struct)
except Exception :
    print("%s not existing" % src_table_name)
    sys.exit(1)
    
print('*** Reading key schema from %s table' % src_table_name)

# 2. Create the new dest_table 
table_struct = None
try:    
    dst_table_name = src_table_name + '-CLONED-'+datetime.datetime.now().strftime("%y-%m-%d-%H-%M") 
    # table definition
    key_schema_src_table_name = client.describe_table(TableName=src_table_name)['Table']['KeySchema']
    attr_definitions = client.describe_table(TableName=src_table_name)['Table']['AttributeDefinitions']
    prov_throughput = client.describe_table(TableName=src_table_name)['Table']['ProvisionedThroughput']
    del prov_throughput['LastIncreaseDateTime']
    del prov_throughput['NumberOfDecreasesToday']

    response = client.create_table(
        TableName=dst_table_name, 
        KeySchema=key_schema_src_table_name,
        AttributeDefinitions=attr_definitions,
        ProvisionedThroughput=prov_throughput
    )
    print('*** Waiting for the new table %s becomes active' % dst_table_name)
    sleep(5)
    while client.describe_table(TableName=dst_table_name)['Table']['TableStatus'] != 'ACTIVE':
        print("TABLE STATUS: " + client.describe_table(TableName=dst_table_name)['Table']['TableStatus'])
        sleep(3)
    
except Exception :
    print("Error when creating table: " + dst_table_name)

# 3. Scan source table in order to copy to destiny table
if copy_data == 'copy':
    dynamo_items = []
    api_response = client.scan(TableName=src_table_name,Select='ALL_ATTRIBUTES')
    dynamo_items.extend(api_response['Items'])
    print("Collected total {0} items from table {1}".format(len(dynamo_items), src_table_name))

    while 'LastEvaluatedKey' in api_response:
        api_response = client.scan(TableName=src_table_name,
            Select='ALL_ATTRIBUTES',
            ExclusiveStartKey=api_response['LastEvaluatedKey'])
        dynamo_items.extend(api_response['Items'])
        print("Collected total {0} items from table {1}".format(len(dynamo_items), src_table_name))

    # 4.
    # split all items into chunks, not very optimal as memory allocation is doubled,
    # though this script not intended for unattented execution, so it shoudl be fine
    chunk_size = 20
    current_chunk = []
    chunks = [current_chunk]
    for item in dynamo_items:
        current_chunk.append(item)
        if len(current_chunk) == chunk_size:
            current_chunk = []
            chunks.append(current_chunk)

    # 5. Copy all items to dst_table
    print("Copying data from {0} --> {1}".format(src_table_name, dst_table_name))
    for index, chunk in enumerate(chunks):
        print("Writing chunk {0} out of {1} to table {2}".format(
            index+1,
            len(chunks),
            dst_table_name
        ))
        if len(chunk) > 0:
            write_request = {}
            write_request[dst_table_name] = list(map(lambda x:{'PutRequest':{'Item':x}}, chunk))
            # TODO error handling, failed write items, max is 16MB, but there are throughput limitations as well
            client.batch_write_item(RequestItems=write_request)
        else:
            print("No items in chunk - chunk empty")