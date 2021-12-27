import json
from db_fetcher import DatabaseManager

TABLE_NAME_TODOS = "todos"

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
        'body': json.dumps(todos)
    }

    if method == 'POST' and endpoint == "/todos":
        # Add a new todo
        try:
            payload = json.loads(payload)
        except Exception as e:
            print(e)
            return {
                'statusCode': 401,
                'body': json.dumps({'message': 'Bad request.'})
            }
        if not payload.get('description'):
            return {
                'statusCode': 401,
                'body': json.dumps({'message': 'Bad request.'})
            }
        
        new_item_id = DatabaseManager.add_item_db(table_name=TABLE_NAME_TODOS, item=payload)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Todo with id {new_item_id} deleted'})
        }

    if method == 'DELETE' and endpoint == "/todos/{todoId}":
        # remove a todo
        todo_id = path_parameters['todoId']
        try:
            DatabaseManager.delete_item_db(table_name=TABLE_NAME_TODOS, id_item=todo_id)
        except:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Unexpected error.'})
            }
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Todo with id {todo_id} deleted'})
        }
    return {
        'statusCode': 404,
        'body': json.dumps({'message': 'Not found.'})
    }