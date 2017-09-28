# -*- coding: utf-8 -*-
version = "HTTP/1.1"
http_cc = {200: "ОК",
           400: "BAD REQUEST",
           404: "NOT FOUND",
           501: "NOT IMPLEMENTED"}  # codes with comments

class HttpForm:
    def __init__(self, body=None):
        self.http_version = version
        self.http_body = body  # body of http request
        self.http_headers = dict()  # all headers and their values
        self.http_headers_order = []  # expresses the order of headers in which they are passed into request

    def start_line(self):
        pass

    def add_header(self, key, value): # adds a header to request and writes it into the http_headers_order list
        self.http_headers[key] = value
        self.http_headers_order.append(key)

    def add_headers(self, keys, values):
        self.http_headers = {keys[i]: values[i] for i in range(len(keys))}
        self.http_headers_order = keys

    def set_body(self, body):
        self.http_body = body

    def __str__(self):
        http_form = self.start_line()
        print(http_form)
        for key in self.http_headers_order:
            http_form += "{}: {}\r\n".format(key, self.http_headers[key])
        http_form += "\r\n"
        if self.http_body is not None:
            http_form += self.http_body + "\r\n\r\n"
        return http_form


class HttpRequest(HttpForm): # this class describes simple http request and allows to convert it into string
    def __init__(self, method=None, param=None, body=None):
        super().__init__(body)
        self.http_method = method # method of request
        self.http_param = param # parameter of the method

    def start_line(self):
        line = ''
        if self.http_method is None:
            line += version + "\r\n"
        elif self.http_param is None:
            line += "{0} {1}\r\n".format(self.http_method, self.http_version)
        else:
            line += "{0} {1} {2}\r\n".format(self.http_method, self.http_param, self.http_version)
        return line

    def set_method(self, method, param):
        self.http_method = method
        self.http_param = param


class HttpResponse(HttpForm):
    def __init__(self, code=None, body=None):
        super().__init__(body)
        self.http_code = code

    def start_line(self):
        return (self.http_version + " " +
                str(self.http_code) + " " +
                http_cc[self.http_code] + " " +
                "\r\n")

    def set_code(self, code):
        self.http_code = code