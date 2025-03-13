import re

def split(text):
    return re.findall(r'[A-Z][^A-Z]*', text)

print(split("HelloWorldPython"))  