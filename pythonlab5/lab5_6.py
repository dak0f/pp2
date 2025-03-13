import re

def replace(text):
    return re.sub(r'[ ,.]', ':', text)


print(replace("Hello, world. This is a test."))  