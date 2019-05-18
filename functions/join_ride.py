import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')


def main(event, context):
    print("Printing the handler function event to console... ")
    print(event)

    event_query_parameters = event['queryStringParameters']
    passenger_id = event['requestContext']['authorizer']['principalId']

    if 'rideUID' not in event_query_parameters:
        print("Request to join a ride must include a rideUID")
        raise Exception("Couldn't update the passengers in this ride, no rideUID found")
    print("RideUID found:" + event_query_parameters.get('rideUID'))

    ride_uid = event_query_parameters.get('rideUID')
    rides_table_client = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


    # Updates the "passengers" attribute in a specific rideUID item, in DynamoDB
    response = rides_table_client.update_item(
        TableName='now8-dev',
        Key={
            'rideUID': ride_uid
        },
        UpdateExpression="set #passengersList = list_append(#passengersList, :newPassengerValue)",
        ExpressionAttributeNames={
            '#passengersList': 'passengers'
        },
        ExpressionAttributeValues={
            ':newPassengerValue': [passenger_id]
        },
        ReturnValues="UPDATED_NEW"
    )

    return{
        'statusCode': 200,
        'body': json.dumps(response)
    }
