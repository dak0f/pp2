import re

def camel_to_snake(camel_str):
    return re.sub(r'(?<!^)([A-Z])', r'_\1', camel_str).lower()


print(camel_to_snake("helloWorldPython"))  # "hello_world_python"