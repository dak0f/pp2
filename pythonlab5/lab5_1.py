import re

def match(text):
    pattern = r'ab*'
    return bool(re.match(pattern, text))

print(match("ac")) # True
print(match("abc"))  # True
print(match("bbbab"))  # False