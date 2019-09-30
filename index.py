import json
import boto3
import decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def lambda_handler(event, context):
   
    dynamodb = boto3.resource('dynamodb')
    dynamodbTable = dynamodb.Table('tableAylin')
   
    
    print('ESTE ES MI EVENTO')
    print(event)
    
    if (event['httpMethod'] == 'GET'):
        print("ES GET")
        data = dynamodbTable.scan(TableName='tableAylin', Select='ALL_ATTRIBUTES')
        dataJSON = json.dumps(data["Items"], cls=DecimalEncoder)
        return {
            'body': dataJSON
        }
        
    if (event['httpMethod'] == 'POST'):
        print("ES POST")
        dataJSON = event['multiValueQueryStringParameters']
        print(dataJSON['id'][0])
        dynamodbTable.put_item(
            Item = {
                'ID': int(dataJSON['id'][0]),
                'FirstName': dataJSON['firstName'][0],
                'LastName': dataJSON['lastName'][0]
            }
        )
        return {
            'body': json.dumps('Se ha insertado el registro con exito')
        }
    else:
        print("Problema al Ejecutar")
        return {
            'body': json.dumps('Hello from Lambda!')
        }
