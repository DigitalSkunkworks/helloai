import os
import json
import uuid
import boto3
import math

# Get the service resource
dynamodb = boto3.resource('dynamodb')

# Retrieve table names from AWS environment variables
table = dynamodb.Table(os.environ['TABLE_NAME'])
output_table = dynamodb.Table(os.environ['OUTPUT_TABLE_NAME'])

'''
## NOT USED  ##

Insert test data into dynamodb

Parameters:
    N/A
Example output:
    N/A
'''
def put_test_data():
  table.put_item(
      Item={
          'id': str(uuid.uuid4()),
          'value': [1, 2, 0, 4, 2],
          'weight': [5, 6, 7, 8, 8]
      }
  )

'''
## NOT USED  ##

Retrieves data from DynamoDB

Parameters:
    weight:
    value:

Example output:
'''
def get_dynamo():
    response = table.get_item(
        Key={
            'id': 'a11ce4e4-bbee-4119-a39c-025451eda0cd'
        }
    )
    item = response['Item']
    print(item)

    return item

'''
Inserts data into the output DynamoDB table

Parameters:
    id - the ID extracted from the DynamoDB record - creates a relationship between the input/ouput tables
    output - the result from the calculation process

Example output:
    N/A
'''
def put_dynamo(id, output):
    output_table.put_item(
        Item={
            'id': id,
            'value': output
        }
    )

'''
This function checks whether the two arrays used in the calculation process are the same length
If they are equal in length True is returned, otherwise False

Parameters:
    weight: list containing the weight values
    value: list containing the values

Example output:
    True/False
'''


def length_check(weight, value):
    # Get length of each array
    value_length = len(value)
    weight_length = len(weight)

    # Check if arrays are the same length
    return False if value_length != weight_length else True

'''
Runs the sigmoid activation function against the output provided by the calculation function

Parameters:
    x: the cumulative value provided by the calculation function

Example output:
    float
'''
def sigmoid(x):
  return 1 / (1 + math.exp(-x))

'''
Runs the relu activation function against the output provided by the calculation function

Parameters:
    x: the cumulative value provided by the calculation function

Example output:
    float
'''
def ReLU(x):
    return x * (x > 0)

'''
Builds a list of floats from a list of objects
When retrieving a int list/array from DynamoDB, it is returned in the following format - [{'N': '5.5'}, {'N': '6'}, {'N': '7.6'}, {'N': '8'}, {'N': '8'}]
This function converts this to a list of floats ready for the calculation function

Parameters:
    data - array of objects passed by DynamoDB
    
Example output:
    [5.5, 6.0, 7.6, 8.0, 8.0]
'''
def build_array(data):

    list = []

    for x in data:
        list.append(float(x['N']))

    return list

'''
This is the main calculation function which multiplies the value from the weight array, with the value from the value array
Iterations containing 0s are ignored and the function will error if the arrays are of varying lengths
The result is returned to the main function

Parameters:
    weight: weight array of objects from DynamoDB
    value:  value array of objects from DynamoDB

Example output:
    int - 1 or 0
'''
def calculate(weight, value):
    # Initialise cumulative variable
    cumulative = 0

    # Check length of arrays are equal
    if not length_check(weight, value):
        print("ERROR lengths do not match")
        # TODO error handling

    # Initialise index variable
    i = 0

    # Loop through the first array
    for x in value:
        y = weight[i]

        # Debug output
        #print("Value = " + str(x))
        #print("Weight = " + str(y))

        # Check if either value is equal to 0, if yes, skip to the next iteration
        if 0 in (x, y):
            print("WARNING 0 found - SKIPPING ITERATION")
            continue

        # Multiply the value by the weight and add to the cumulative variable
        cumulative = cumulative + (x * y)

        # Increment the index for the weight array
        i = i + 1

    output = ReLU(cumulative)


    print(output)

    return output

'''
## Entry point for the AWS Lambda function ##

This function dissects the DynamoDB event and pulls out the required attributes ready for processing. 
If the event is not of type 'INSERT', the process is skipped.
 
Returns JSON back to the Lambda service

Parameters:
    event   - standard AWS Lambda parameter
    context - standard AWS Lambda parameter
    
Example output:
    {
      "statusCode": 200,
      "body": "{"message": "Serverless function executed successfully!},
      "output": 2
    }
'''
def main(event, context):

    print(event)

    weight_list = []
    value_list = []

    # Select the single record from the event data
    record = event['Records'][0]

    # If the event type is insert then process, otherwise skip
    if record['eventName'] == 'INSERT':
        print('inside insert code')

        # Filter to the required data
        data = record['dynamodb']['NewImage']

        # Pull required attributes from event object
        id          = data['id']['S']
        weight_data = data['weight']['L']
        value_data  = data['value']['L']

        # Convert the object array into a usuable python list
        weight = build_array(weight_data)
        value = build_array(value_data)

        print(weight)
        print(value)

        # Run core calculations and round output
        output = calculate(weight, value)

        #
        output = int(round(output))

        print(output)

        # Write result to output table
        put_dynamo(id, str(output))

    else:
        print('Not an insert event - Skipping')

    body = {
        "message": "Serverless function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "CumulativeValue": 'debug',
    #    "Data": data
    }

    return response
