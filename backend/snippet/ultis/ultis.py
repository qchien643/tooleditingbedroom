# snippet/utils.py
import os
import json

def get_data_path(filename):
    # Lùi lên 3 cấp thư mục
    base_dir = os.path.dirname(
                   os.path.dirname(
                       os.path.dirname(
                           os.path.abspath(__file__)
                       )
                   )
               )
    return os.path.join(base_dir, 'data', filename)

def load_json(filename):
    with open(get_data_path(filename), 'r') as f:
        return json.load(f)