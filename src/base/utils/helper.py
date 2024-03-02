import re

def is_valid_password(password):
    password_pattern = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')
    return bool(password_pattern.match(password))

def is_valid_username(input_string):
    pattern = re.compile(r'^[a-zA-Z0-9_.]{1,32}$')
    return bool(pattern.match(input_string))