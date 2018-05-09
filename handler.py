import os
import json
import uuid
import boto3

# Get the service resource
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table(os.environ['TABLE_NAME'])

# Set array values - TODO Get Arrays from external data source
value = [1, 2, 0, 4, 2]
weight = [5, 6, 7, 8, 8]

'''
Inserts data into dynamodb
'''
def put_dynamo():

   table.put_item(
       Item={
           'id': str(uuid.uuid4()),
           'username': 'janedoe',
           'first_name': 'Jane',
           'last_name': 'Doe',
           'age': 25,
           'account_type': 'standard_user',
       }
   )

'''
Retrieves data from dynamodb
'''
def get_dynamo():

    response = table.get_item(
        Key={
            'id': '8854b233-5807-4cb0-afce-4636d3d3783f'
        }
    )
    item = response['Item']
    print(item)

    return item


'''
Checks the length of the input arrays
Returns a boolean value
'''
def length_check():
    # Get length of each array
    value_length = len(value)
    weight_length = len(weight)

    # Check if arrays are the same length
    return False if value_length != weight_length else True

'''
The main calculations 
'''
def calculate():
    # Initialise cumulative variable
    cumulative = 0

    # Check length of arrays are equal
    if not length_check():
        print("ERROR lengths do not match")
        # TODO error handling

    # Set index variable
    i = 0

    # Loop through the first array
    for x in value:
        y = weight[i]

        # Debug output
        print("Value = " + str(x))
        print("Weight = " + str(y))

        # Check if either value is equal to 0, if yes, skip to the next iteration
        if 0 in (x, y):
            print("WARNING 0 found - SKIPPING ITERATION")
            continue

        # Multiply the value by the weight and add to the cumulative variable
        cumulative = cumulative + (x * y)

        # Increment the index for the weight array
        i = i + 1

    print(cumulative)

    return cumulative


# TODO apply activation function to cumulative value

'''
Entry point for lambda
'''
def main(event, context):
    total = calculate()
    put_dynamo()
    user = get_dynamo()

    body = {
        "message": "Serverless function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "CumulativeValue": total,
        "User":user
    }

    return response