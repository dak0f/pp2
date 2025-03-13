import re

def find(text):
    pattern = r'[a-z]+_[a-z]+'
    return re.findall(pattern, text)


print(find("hello_world foo_bar baz")) 