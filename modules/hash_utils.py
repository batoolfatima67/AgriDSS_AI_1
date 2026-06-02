import hashlib
import json

def generate_input_hash(user_data):
    return hashlib.md5(
        json.dumps(user_data, sort_keys=True).encode()
    ).hexdigest()
