#!/usr/bin/python3

import http.server
import socketserver
from urllib.parse import parse_qs

PORT = 8000


class Serv(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("Test")
        params = parse_qs(self.path[2:])
        self.wfile.write("Sie suchten nach der Telefonnummer: {}".format(params["num"][0]).encode())

with socketserver.TCPServer(("", PORT), Serv) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
