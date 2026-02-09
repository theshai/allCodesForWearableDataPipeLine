import json
import os
import pg8000

conn = None

def get_conn():
    global conn
    if conn is None:
        conn = pg8000.connect(
            host=os.environ['DB_HOST'],
            port=int(os.environ['DB_PORT']),
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD']
        )
    return conn


def lambda_handler(event, context):
    connection = get_conn()
    
    try:
        # works for GET or POST
        if event.get("body"):
            data = json.loads(event["body"])
        else:
            data = event.get("queryStringParameters") or {}

        uid = data.get("uid")
        user = data.get("user")
        user="shai" # get shai user only for the test, in production will parse the json

        

        if not uid and not user:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Provide uid or user"})
            }

        with connection.cursor() as cur:

            if uid:
                cur.execute(
                    'SELECT uid, "user", value,flag, datetime FROM heartrate WHERE uid=%s ORDER BY datetime DESC;',
                    (uid,)
                )
            else:
                cur.execute(
                    'SELECT uid, "user", value,flag, datetime FROM heartrate WHERE "user"=%s ORDER BY datetime DESC;',
                    (user,)
                )

            rows = cur.fetchall()

        # convert to JSON friendly list
        results = [
            {
                "uid": r[0],
                "user": r[1],
                "value": float(r[2]),
                "flag":r[3],
                "datetime": str(r[4])
            }
            for r in rows
        ]

        return {
            "statusCode": 201,
            "headers": { # CORS issue bypass
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,x-api-key",
                "Access-Control-Allow-Methods": "POST,OPTIONS"
            },
            "body": json.dumps(results)
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }