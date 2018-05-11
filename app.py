import os
import json
import uuid
import boto3
import math

# Get the service resource
#dynamodb = boto3.resource('dynamodb')

#table = dynamodb.Table(os.environ['TABLE_NAME'])
#output_table = dynamodb.Table(os.environ['OUTPUT_TABLE_NAME'])

# Set array values - TODO Get Arrays from external data source
# value = [1, 2, 0, 4, 2]
# weight = [5, 6, 7, 8, 8]

'''
Inserts data into dynamodb
'''


def put_dynamo(id, output):
    output_table.put_item(
        Item={
            'id': id,
            'value': output
        }
    )

def put_test_data():
  table.put_item(
      Item={
          'id': str(uuid.uuid4()),
          'value': [1, 2, 0, 4, 2],
          'weight': [5, 6, 7, 8, 8]
      }
  )

'''
Retrieves data from dynamodb
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
Checks the length of the input arrays
Returns a boolean value
'''


def length_check(weight, value):
    # Get length of each array
    value_length = len(value)
    weight_length = len(weight)

    # Check if arrays are the same length
    return False if value_length != weight_length else True

'''
Sigmoid function required by the calculate function
'''
def sigmoid(x):
  return 1 / (1 + math.exp(-x))
'''
The main calculations 
'''
def calculate(weight, value):
    # Initialise cumulative variable
    cumulative = 0

    # Check length of arrays are equal
    if not length_check(weight, value):
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


    # TODO CONVERT ME TO DECIMAL - DOES NOT CURRENTLY WORK
    print(cumulative)
    output = sigmoid(cumulative)


    print(output)

    return output


# TODO apply activation function to cumulative value

'''
Builds arrays from dynamodb event object
'''
def build_array(data):

    list = []

    for x in data:
        list.append(int(x['N']))

    return list

'''
Entry point for lambda
'''
def main(event, context):
  #  put_test_data()
  #  data = get_dynamo()

    weight_list = []
    value_list = []

    # Select the single record from the event data
    record = event['Records'][0]

    # Filter to the required data
    data = record['dynamodb']['NewImage']

    # If the event type is insert then process, otherwise skip
    if record['eventName'] == 'INSERT':
        print('inside insert code')

        # Pull required attributes from event object
        id          = data['id']['S']
        weight_data = data['weight']['L']
        value_data  = data['value']['L']

        # Convert the object array into a usuable python list
        weight = build_array(weight_data)
        value = build_array(value_data)

        print(weight)
        print(value)

        # Run core calculations
        output = calculate(weight, value)

        # Write result to output table
        put_dynamo(id, output)

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


def main_local():
    value = [1.1, 2, 0, 4.5, 2]
    weight = [5, 6.7, 7, 8, -0.8]
    print(weight)
    output = calculate(weight, value)


if __name__ == "__main__":
    main_local()
