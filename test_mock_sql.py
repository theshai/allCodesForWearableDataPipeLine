import json
from lambda_function import lambda_handler

with open("server_feed.json") as f:
    event = json.load(f)

print(lambda_handler(event, None))