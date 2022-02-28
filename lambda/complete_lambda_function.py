import json, os
from db_fetcher import DatabaseManager

TABLE_NAME_TODOS = "todo-XX"

headers = {
    "X-Requested-With": '*',
    "Access-Control-Allow-Headers": 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with',
    "Access-Control-Allow-Origin": '*',
    "Access-Control-Allow-Methods": 'POST,GET,DELETE,OPTIONS'
}

def lambda_handler(event, context):
    """
    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    method = event.get('httpMethod')
    endpoint = event.get('resource')
    path_parameters = event.get('pathParameters')
    payload = event.get('body')


    if method == 'GET' and endpoint == "/todos":
        # Get a list todos
        todos = DatabaseManager.get_list_item_db(table_name=TABLE_NAME_TODOS)
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(todos)
        }

    if method == 'POST' and endpoint == "/todos":
        # Add a new todo

        # 1) Convert payload to dict
        try:
            payload = json.loads(payload)
        except Exception as e:
            print(e)
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Payload must be Json format.'})
            }
        # 2) assert 'label' key exists
        if not payload.get('label'):
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'label not found.'})
            }
        # 3) Push item to DB
        new_item_id = DatabaseManager.add_item_db(table_name=TABLE_NAME_TODOS, item=payload)

        # 4) Return 200
        return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': f'Todo with id {new_item_id} added'})
            }

    if method == 'DELETE' and endpoint == "/todos/{todoId}":
        # remove a todo

        # 1) fetch TodoId from path_parameters
        todo_id = path_parameters['todoId']
        try:
            # 2) Delete the TodoId from DB 
            DatabaseManager.delete_item_db(table_name=TABLE_NAME_TODOS, id_item=todo_id)
        except:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({'message': f"Couldn't remove todo"})
            }
        
        # 3) Return 200 
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': f"Todo with id {todo_id} deleted"})
        }

    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers
        }

    return {
            'statusCode': 404,
            'headers': headers,
            'body': json.dumps({'message': f"Unknown method"})
        }
