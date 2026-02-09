import json
import os
import pg8000

conn = None


# -------------------------
# DB CONNECTION.ver1
# -------------------------
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


# -------------------------
# BUSINESS LOGIC (PURE)
# -------------------------
def calculate_flag(value: float) -> str:
    return "HIGH" if value > 120 else "NORMAL"


# -------------------------
# DATABASE LAYER
# -------------------------
def insert_heartrate(connection, uid, user, value, flag):
    with connection.cursor() as cur:
        cur.execute(
            """INSERT INTO heartrate (uid, "user", value, flag)
               VALUES (%s, %s, %s, %s)
               RETURNING datetime;""",
            (uid, user, value, flag)
        )
        connection.commit()
        return cur.fetchone()[0]


# -------------------------
# HANDLER
# -------------------------
def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        uid = int(body["uid"])
        user = body["user"]
        value = float(body["value"])

        flag = calculate_flag(value)

        connection = get_conn()
        inserted_time = insert_heartrate(connection, uid, user, value, flag)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Heart rate saved",
                "datetime": str(inserted_time),
                "flag": flag
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)})
        }