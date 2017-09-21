import re
class NotMatchedException(Exception):
    def __init__(self, pattern, source):
        self.pattern = pattern
        self.source = source
    def __str__(self):
        return f'Pattern "{self.pattern}" is not matched in source "{self.source}"'

def search_from_source(pattern, source):
    m = re.search(pattern,source)
    if not m:
        raise NotMatchedException(pattern, source)
    return m

pattern = r'L\w{5}\b'
source = "Lux is a great person"
search_from_source(pattern, source)
