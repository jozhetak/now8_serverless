import json
import os

import jwt

from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate

# Set by serverless.yml
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_PUBLIC_KEY = os.getenv('AUTH0_CLIENT_PUBLIC_KEY')


def main(event, context):
    whole_auth_token = event.get('authorizationToken')
    if not whole_auth_token:
        print('No Authentication Token in the request')
        raise Exception('No Authentication Token in the request')

    print('Client token: ' + whole_auth_token)
    print('Method ARN: ' + event['methodArn'])

    token_parts = whole_auth_token.split(' ')
    token_method = token_parts[0]
    auth_token = token_parts[1]

    if not (token_method.lower() == 'bearer' and auth_token):
        print("Failing due to invalid format (Bearer) or invalid token")
        raise Exception('Failing due to invalid format (Bearer) or invalid token')

    try:
        principal_id = jwt_verify(auth_token, AUTH0_CLIENT_PUBLIC_KEY)
        policy = generate_policy(principal_id, 'Allow', event['methodArn'])
        return policy
    except Exception as e:
        print(f'Exception encountered: {e}')
        raise Exception('Unauthorized')


def jwt_verify(auth_token, public_key):
    public_key = format_public_key(public_key)
    pub_key = convert_certificate_to_pem(public_key)  # pub_key is a PEM-encoded certificate with a public key
    payload = jwt.decode(auth_token, pub_key, algorithms=['RS256'], audience=AUTH0_CLIENT_ID)
    return payload['nickname'] + '@' + payload['sub']


def generate_policy(principal_id, effect, resource):
    return {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": resource

                }
            ]
        },
    }


def convert_certificate_to_pem(public_key):
    cert_obj = load_pem_x509_certificate(str.encode(public_key), default_backend())
    pub_key = cert_obj.public_key()
    return pub_key


def format_public_key(public_key):
    public_key = public_key.replace('\n', ' ').replace('\r', '')
    public_key = public_key.replace('-----BEGIN CERTIFICATE-----', '-----BEGIN CERTIFICATE-----\n')
    public_key = public_key.replace('-----END CERTIFICATE-----', '\n-----END CERTIFICATE-----')
    return public_key


def create_200_response(message):
    headers = {
        # Required for CORS support to work
        'Access-Control-Allow-Origin': '*',
        # Required for cookies, authorization headers with HTTPS
        'Access-Control-Allow-Credentials': True,
    }
    return create_aws_lambda_response(200, {'message': message}, headers)


def create_aws_lambda_response(status_code, message, headers):
    return {
        'statusCode': status_code,
        'headers': headers,
        'body': json.dumps(message)
    }
