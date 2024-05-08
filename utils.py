import re

def is_a_special_char(char):
    special_chars_regex = re.compile(r'[^\w\s]')
   
    if special_chars_regex.search(char):
        return True

    return False