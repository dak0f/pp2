import re

def find(text):
    pattern = r'[A-Z][a-z]+'
    return re.findall(pattern, text)

print(find("Hello World python"))  