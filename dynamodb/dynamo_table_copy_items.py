#===============================================================================================================#
#   Dynamo Table Copy Table Items v 1.0                                                                         #        
#                                                                                                               #
#   DynamoDB Script for copying table items between accounts                                                    #
#                                                                                                               #
#   How to use:                                                                                                 #
#   - On the command line type:                                                                                 #
#   > python dynamo_table_copy_items.py <source_table_name> <destiny_table_name> <src_profile> <dst_profile>    #
#                                                                                                               #
#   Auhor: Wagner Alves                                                                                         #                                         
#   Data : 02/04/2018                                                                                           #
#===============================================================================================================#

#!/usr/bin/env python
import boto3
import sys

src_region = 'us-east-1'
src_profile = None
dst_region = 'us-east-1'
dst_profile = None
src_client = None
dst_client = None

if len(sys.argv) < 3:
    print('Usage: %s <source_table_name> <destiny_table_name> <src_profile> <dst_profile>' % sys.argv[0])
    sys.exit(1)

src_table = sys.argv[1]
dst_table = sys.argv[2]
src_profile = sys.argv[3]  

if len(sys.argv) > 4:
    dst_profile = sys.argv[4]
    print("Profile: {0} --> {1}".format(src_profile, dst_profile))

print("Copy items from {0} --> {1}".format(src_table, dst_table))

# source client
#boto3.setup_default_session(profile_name=src_profile)
src_client = boto3.Session(profile_name=src_profile).client('dynamodb', region_name= src_region)

# dest client
if dst_profile is not None:
    dst_client = boto3.Session(profile_name=dst_profile).client('dynamodb', region_name= dst_region)
    print("Connect by Session to dest profile: {0}".format(dst_profile))
else:
    dst_client = src_client
    print("Connect to same profile: {0}".format(src_profile))

# Scan Source Table
dynamo_items = []
api_response = src_client.scan(TableName=src_table,Select='ALL_ATTRIBUTES')
dynamo_items.extend(api_response['Items'])
print("Collected total {0} items from table {1}".format(len(dynamo_items), src_table))

while 'LastEvaluatedKey' in api_response:
    api_response = src_client.scan(TableName=src_table,
        Select='ALL_ATTRIBUTES',
        ExclusiveStartKey=api_response['LastEvaluatedKey'])
    dynamo_items.extend(api_response['Items'])
    print("Collected total {0} items from table {1}".format(len(dynamo_items), src_table))

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

for index, chunk in enumerate(chunks):
    print("Writing chunk {0} out of {1} to table {2}".format(
        index+1,
        len(chunks),
        dst_table
    ))
    if len(chunk) > 0:
        write_request = {}
        write_request[dst_table] = list(map(lambda x:{'PutRequest':{'Item':x}}, chunk))
        # TODO error handling, failed write items, max is 16MB, but there are throughput limitations as well
        dst_client.batch_write_item(RequestItems=write_request)
    else:
        print("No items in chunk - chunk empty")