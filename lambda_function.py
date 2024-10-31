import sys
import logging
import json
import os
import psycopg2
import csv
import io
import boto3
from psycopg2 import sql

# RDS and S3 settings
user_name = os.environ['USER_NAME']
password = os.environ['PASSWORD']
rds_proxy_host = os.environ['RDS_PROXY_HOST']
db_name = os.environ['DB_NAME']
s3_bucket_name = os.environ['S3_BUCKET_NAME']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Size threshold in bytes
SIZE_THRESHOLD = 4 * 1024 * 1024  

def lambda_handler(event, context):
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=rds_proxy_host,
            database=db_name,
            user=user_name,
            password=password,
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
    data = event.get('queryStringParameters', {}).get('data', None)
    
    if not iso:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Bad request: Missing or invalid ISO parameter.'})
        }
    if not data:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Bad request: Missing or invalid data parameter.'})
        }
    
    # Parse data parameter and build table names
    data_types = data.split(',')
    tables = [f"{iso}_{d}" if d != "geo" else iso for d in data_types]
    
    # Verify table existence and prepare SQL joins
    valid_tables = []
    for table in tables:
        try:
            cur.execute(
                sql.SQL("SELECT to_regclass(%s)"),
                (table,)
            )
            result = cur.fetchone()
            if result[0] is not None:
                valid_tables.append(table)
            else:
                logger.info(f"Table {table} does not exist, skipping.")
        except Exception as e:
            logger.error(f"Failed to check existence of table {table}")
            logger.error(e)
    
    if not valid_tables:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'No valid tables found for the specified parameters.'})
        }
    
    # Build the SQL JOIN query on geo_id for all valid tables
    base_table = valid_tables[0]
    joins = [
        sql.SQL("LEFT JOIN {} ON {}.geo_id = {}.geo_id").format(
            sql.Identifier(table),
            sql.Identifier(base_table),
            sql.Identifier(table)
        )
        for table in valid_tables[1:]
    ]
    
    query = sql.SQL("SELECT * FROM {} {}").format(
        sql.Identifier(base_table),
        sql.SQL(" ").join(joins)
    )
    
    try:
        # Execute the query
        cur.execute(query)
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
    
    # Check CSV size and decide response type
    if len(csv_content.encode('utf-8')) > SIZE_THRESHOLD:
        # Initialize S3 client and save to bucket
        s3 = boto3.client('s3')
        s3_key = f"exports/{iso}_output.csv"
        s3.put_object(Bucket=s3_bucket_name, Key=s3_key, Body=csv_content, ContentType='text/csv')
        
        # Generate presigned URL for S3 file
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': s3_bucket_name, 'Key': s3_key},
            ExpiresIn=3600
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'CSV saved to S3 due to size constraints', 'url': presigned_url})
        }
    
    # Return CSV content if size is below threshold
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment;filename=output.csv'
        },
        'body': csv_content
    }
