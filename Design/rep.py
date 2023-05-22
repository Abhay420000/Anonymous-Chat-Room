req = """
{“name”: “”, “room_code”: "RyixQ1",“action”: “join room”}
"""
s = req.replace("”",'"')
s = s.replace("“",'"')

print(s)