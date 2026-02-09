import requests
import random
import time
from datetime import datetime

URL = "https://q7r9c9x537.execute-api.us-east-2.amazonaws.com/basic1/writeData"

HEADERS = {
    "x-api-key": "ap9kUNqYEM5L6TuseuWhf4jbnz4t4a1N5VZuDJgZ",
    "Content-Type": "application/json"
}


def generate_payload():
    return {
        "uid": random.randint(1000, 9999),   # 4-digit uid
        "user": "shai",
        "value": random.randint(60, 180)     # random range
    }


def send_post():
    payload = generate_payload()
    timestamp = datetime.now().strftime("%H:%M:%S")

    try:
        response = requests.post(URL, headers=HEADERS, json=payload, timeout=10)
        print(f"[{timestamp}] Sent {payload} -> {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"[{timestamp}] ERROR: {e}")


def main():
    print("Starting sender (every 5 seconds). Press Ctrl+C to stop.\n")

    while True:
        send_post()
        time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")