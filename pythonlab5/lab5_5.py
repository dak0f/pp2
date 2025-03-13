import re

def match(text):
    pattern = r'a.*b$'
    return bool(re.match(pattern, text))

print(match("a123b"))# True
print(match("acb"))# True
print(match("ab"))# True
print(match("abc")) # False