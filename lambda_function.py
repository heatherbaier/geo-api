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

def lambda_handler(event, context):
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=rds_proxy_host,
            database=db_name,
            user=user_name,
            password=password,
            sslmode="require"
        )
        logger.info("CONNECTED TO DATABASE")
    except Exception as e:
        logger.error("Failed to connect to database")
        logger.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error: could not connect to the database.'})
        }
    
    # Create a cursor object
    cur = conn.cursor()
    
    # Extract query parameters
    iso = event.get('queryStringParameters', {}).get('iso', None)    
    
    if not iso:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Bad request: Missing or invalid ISO parameter.'})
        }
    
    # Construct the SQL query safely
    query = f"SELECT * FROM {iso} LIMIT 5"
    
    try:
        # Execute the query
        cur.execute(query, (iso,))
        # Fetch all results
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        
        # Close the connection
        cur.close()
        conn.close()
    except Exception as e:
        logger.error("Failed to execute query")
        logger.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error: could not execute query.'})
        }
    
    # Convert results to CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(columns)
    writer.writerows(rows)
    csv_content = output.getvalue()

    # Combine the message with the CSV content
    message = f"Message: Request worked successfully for ISO: {iso}\n\n"
    csv_with_message = message + csv_content
    
    # Return the CSV content as a file download response
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment;filename=output.csv'
        },
        'body': csv_content
    }
