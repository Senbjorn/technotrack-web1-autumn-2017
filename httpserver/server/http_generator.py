# -*- coding: utf-8 -*-
import os
import time
from http_form import *
from http_parser import *

get_patterns = {"/": "main", "/test/": "test", "/media/": "info", "/media/.*": "content", "code": "code"}
methods = {"GET", "POST", "HEAD", "PUT", "CONNECT", "OPTIONS", "PATCH", "TRACE", "DELETE"}
implemented = {"GET"}


def read_file(path):
    file = open(path, 'r')
    line = file.read()
    file.close()
    return line


def read_pattern(name):
    return read_file(name + "_pattern.html")


def read_content(name):
    return read_file("..\\files\\" + name)


def generate_code_http(request, code):
    now = time.strftime('%c')
    response = HttpResponse()
    body = read_pattern(get_patterns["code"]).format(code, http_cc[code])
    length = len(body)
    response.set_code(code)
    response.add_header("Server", "MyHttp")
    response.add_header("Date", now)
    response.add_header("Content-Language", "en-US")
    response.add_header("Content-Type", "text/html")
    response.add_header("Content-Length", length)
    response.set_body(body)
    return response


def generate_main_http(request):
    now = time.strftime('%c')
    headers = request.http_headers
    param = request.http_param
    response = HttpResponse()
    print("get:", param)
    body = read_pattern(get_patterns[param]).format(headers["User-Agent"])
    length = len(body)
    response.set_code(200)
    response.add_header("Server", "MyHttp")
    response.add_header("Date", now)
    response.add_header("Content-Language", "en-US")
    response.add_header("Content-Type", "text/html")
    response.add_header("Content-Length", length)
    response.set_body(body)
    return response


def generate_content_http(request):
    now = time.strftime('%c')
    param = request.http_param
    response = HttpResponse()
    path = re.match('^/media/(.*)$', param).group(1)
    if not os.access("..\\files\\" + path, os.R_OK):
        return generate_code_http(request, 404)
    print("get:", path)
    body = read_pattern(get_patterns["/media/.*"])
    body = (body[0: body.find('<title>')] +
            body[body.find('<title>'): body.find('</title>')].format(path) +
            body[body.find('</title>'): body.find('<body>')] +
            body[body.find('<body>'):].format(read_content(path)))
    length = len(body)
    response.set_code(200)
    response.add_header("Server", "MyHttp")
    response.add_header("Date", now)
    response.add_header("Content-Language", "en-US")
    response.add_header("Content-Type", "text/html")
    response.add_header("Content-Length", length)
    response.set_body(body)
    return response


def generate_info_http(request):
    now = time.strftime('%c')
    param = request.http_param
    response = HttpResponse()
    print("get:", param)
    body = read_pattern(get_patterns[param])
    print(body)
    files = os.listdir(path='..\\Files')
    files = [files[i] for i in range(len(files)) if os.access("..\\Files\\" + files[i], os.R_OK)]
    list_files = ''
    for i in range(len(files)):
        list_files += "<li><span>{}</span></li>".format(files[i])
    print(list_files)
    body = body[0: body.find('<body>')] + body[body.find('<body>'):].format(list_files)
    length = len(body)
    response.set_code(200)
    response.add_header("Server", "MyHttp")
    response.add_header("Date", now)
    response.add_header("Content-Language", "en-US")
    response.add_header("Content-Type", "text/html")
    response.add_header("Content-Length", length)
    response.set_body(body)
    return response


def generate_test_http(request):
    now = time.strftime('%c')
    param = request.http_param
    response = HttpResponse()
    print("get:", param)
    body = read_pattern(get_patterns["/test/"])
    body = body = body[0: body.find('<body>')] + body[body.find('<body>'):].format(str(request))
    length = len(body)
    response.set_code(200)
    response.add_header("Server", "MyHttp")
    response.add_header("Date", now)
    response.add_header("Content-Language", "en-US")
    response.add_header("Content-Type", "text/html")
    response.add_header("Content-Length", length)
    response.set_body(body)
    return response


def generate_get(request):
    param = request.http_param
    if re.match('^/$', param):
        return generate_main_http(request)
    if re.match('^/media/$', param):
        return generate_info_http(request)
    if re.match('^/media/.*$', param):
        return generate_content_http(request)
    if re.match('^/test/$', param):
        return generate_test_http(request)
    return generate_code_http(request, 400)


def generate_http_response(r_request):
    request = parse_request(r_request)
    if request is None:
        return generate_code_http(request, 400)
    if request.http_method == "GET":
        return generate_get(request)
    if request.http_method in methods and request.http_method not in implemented:
        return generate_code_http(request, 501)
    return generate_code_http(request, 400)
