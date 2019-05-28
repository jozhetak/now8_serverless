import json

# This function is triggered when the passengers in a ride change.
# for example when a passenger joins a ride


def main(event, context):

    return{
        'statusCode': 200,
        'body': json.dumps("Hello World")
    }
