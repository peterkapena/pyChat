# import json
# from typing import List
# from dataclasses import dataclass

# @dataclass
# class client:
#     addr: str
#     port: int

# class JSON(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, client):
#             return obj.__dict__
#         return super().default(obj)

# clients = [client("192.168.0.1", 8000), client("192.168.0.2", 8000), client("192.168.0.3", 8000)]

# json_string = json.dumps(clients, cls=JSON)

# print(json_string)
