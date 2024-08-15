import sys
import logging
import json
import os
import psycopg2
import csv
import io


# rds settings
user_name = os.environ['USER_NAME']
password = os.environ['PASSWORD']
rds_proxy_host = os.environ['RDS_PROXY_HOST']
db_name = os.environ['DB_NAME']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

print("HERE YO")

# create the database connection outside of the handler to allow connections to be
# re-used by subsequent function invocations.


def lambda_handler(event, context):
    """
    This function creates a new RDS database table and writes records to it
    """
    # message = event['Records'][0]['body']
    # print(message)

    # data = json.loads(message)
    # print(data)

    # CustID = data['CustID']
    # Name = data['Name']
    # print(CustID)
    # print(Name)
    
    
    try:
        conn = psycopg2.connect(
            host = rds_proxy_host,
            database = db_name,
            user = user_name,
            password = password,
            sslmode = "require"
        )
        print(conn)
        print("CONNECTED TO DATABASE")
    except Exception as e:
        logger.error("Failed to connect to database")
        logger.error(e)
        sys.exit(1)
    
    
    
    # Create a cursor object
    print("HERE IN FUNCTION")
    cur = conn.cursor()
    
    # Extract query parameters
    # table = event.get('queryStringParameters', {}).get('table', 'default_table')
    # query_filter = event.get('queryStringParameters', {}).get('filter', '')
    print("BELOW!")
    print(event.get('queryStringParameters', {}))
    iso = event.get('queryStringParameters', {}).get('iso', None)    
    
    # print("table: ", table)
    # print("query_filter: ", query_filter)
    print("iso: ", iso)

    # Extract query parameters from the event (from API Gateway)
    # table = event.get('queryStringParameters', {}).get('table', 'default_table')
    # query_filter = event.get('queryStringParameters', {}).get('filter', '')
    
    # Construct the SQL query
    query = f"SELECT * FROM {iso} LIMIT 100"
    
    
    
    # Execute the query
    cur.execute(query)
    
    # Fetch all results
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    
    print(columns)
    
    # Close the connection
    cur.close()
    conn.close()

    # Convert results to CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(columns)
    writer.writerows(rows)
    csv_content = output.getvalue()

    # Return a simple message
    # return {
    #     'statusCode': 200,
    #     'body': f'Hello, this is a simple message from Lambda! {str(columns)}'
    # }
    

    # Return the CSV content as a response
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment;filename=output.csv'
        },
        'body': csv_content
        # 'body': f"Worked! {iso}"
    }
