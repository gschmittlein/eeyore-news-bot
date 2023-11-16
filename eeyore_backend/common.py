import json

def format_response(result):
    try:
        result = json.loads(json.dumps(result))
    except Exception as err:
        return {"state": "FAILED", "response_code": 521, "error_msg": f"failed json serialization: {str(err)}"}
    
    return {"state": "DONE", "response_code": 200, "result": result}