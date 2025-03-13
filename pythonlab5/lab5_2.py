import re

def match(text):
    pattern = r'ab{2,3}'
    return bool(re.match(pattern, text))

print(match("abb")) # True
print(match("abbb")) # True
print(match("ab")) # False
print(match("abbbb")) # True