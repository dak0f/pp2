import re

def spaces(text):
    return re.sub(r'(?<!^)([A-Z])', r' \1', text)

print(spaces("HelloWorldPython"))  