import re
from http_form import *


def parse_request(request):
    try:
        request = str(request)[2:-1]
        regexp_m = re.compile(r"^(.+?) (.+?) (HTTP/.+?)\\r\\n")
        regexp_k = re.compile(r"\\n(.+?):.+?\\r")
        regexp_v = re.compile(r"\\n.+?: (.+?)\\r")
        key, value = regexp_k.findall(request), regexp_v.findall(request)
        method, param, version = regexp_m.search(request).groups()
        h_request = HttpRequest(method, param)
        h_request.add_headers(key, value)
        return h_request
    except (AttributeError, TypeError):
        print('I do not like it! ', request)
        return None
