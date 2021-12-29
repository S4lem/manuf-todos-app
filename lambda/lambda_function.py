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

        # Example of a todo :
        # {
        #     "label": "Buy some cheese"
        # }

        # Hint : 
        # json.loads(payload) : converts Json string to Python dictionary

        # 1) Convert payload to dict
        # 2) assert 'label' key exists
        # 3) Push item to DB
        # 4) Return 200
        pass

    if method == 'DELETE' and endpoint == "/todos/{todoId}":
        # remove a todo

        # 1) fetch TodoId from path_parameters
        # 2) Delete the TodoId from DB 
        # 3) Return 200 
        pass

    if method == 'OPTIONS': 
        return {
            'statusCode': 200,
            'headers': {
                "Content-Type": "application/json",
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*'
                }
        }

    return {
        'statusCode': 501,
        'body': json.dumps({'message': 'Not Implemented.'})
    }