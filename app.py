import sys

# Set array values - TODO Get Arrays from external data source
value = [1, 2, 0, 4, 2]
weight = [5, 6, 7, 8, 8]


# Function which checks the length of each array
def length_check():

    # Get length of each array
    value_length = len(value)
    weight_length = len(weight)

    # Check if arrays are the same length
    return False if value_length != weight_length else True


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

        # Multiple the value by the weight and add to the cumulative variable
        cumulative = cumulative + (x * y)

        # Increment the index for the second array
        i = i + 1

    # Print total value
    print(cumulative)
    return cumulative
# TODO apply activation function to cumulative

if __name__ == "__main__":
    calculate()
