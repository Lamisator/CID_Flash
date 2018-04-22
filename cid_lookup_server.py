#!/usr/bin/python3

import http.server
import socketserver
from urllib.parse import parse_qs
import pandas
import re
import sqlite


PORT = 8000


class Serv(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(self.path[2:])
        number = params["num"][0]
        self.wfile.write("Sie suchten nach der Telefonnummer: {}".format(number).encode())
        city = self.code_lookup(int(number))
        print(city)
        
        self.wfile.write(city.encode())


    def code_lookup(self, code):
        if not "csv" in globals():
            self.csv = pandas.read_csv("codes.csv", sep=";", index_col=0).T.to_dict()

        if code in self.csv.keys():
            return str(self.csv[code]["city"])
        else:
            return "Unknown city"

    def cid_lookup(self, did):
        if not "db" in globals():
            self.db = sqlite3.connect("/var/lib/asterisk/astdb.sqlite3")
        db.execute("SELECT * FROM astdb;")




with socketserver.TCPServer(("", PORT), Serv) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
