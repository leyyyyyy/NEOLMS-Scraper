import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table = dynamodb.create_table(
    TableName='Assignments',
    KeySchema=[
        {
            'AttributeName': 'subject_name',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'task_name',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'subject_name',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'task_name',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

print("Table status:", table.table_status)
