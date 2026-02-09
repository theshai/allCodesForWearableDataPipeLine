import json
import lambda_function # testing python_insert_to_db_lambda


def test_flag():
    assert lambda_function.calculate_flag(90) == "HIGH" # testing python_insert_to_db_lambda
    assert lambda_function.calculate_flag(80) == "NORMAL" # testing python_insert_to_db_lambda
    
class FakeConnection:
    def cursor(self):
        class C:
            def execute(self, *args): pass
            def fetchone(self): return ["2026-01-01"]
            def __enter__(self): return self
            def __exit__(self, *args): pass
        return C()

    def commit(self): pass


def test_lambda_handler(monkeypatch): # testing python_insert_to_db_lambda
    monkeypatch.setattr(lambda_function, "get_conn", lambda: FakeConnection()) # testing python_insert_to_db_lambda

    event = {
        "body": json.dumps({
            "uid": 1,
            "user": "shai",
            "value": 150
        })
    }

    res = lambda_function.lambda_handler(event, None) # testing python_insert_to_db_lambda

    body = json.loads(res["body"])

    assert body["flag"] == "HIGH"