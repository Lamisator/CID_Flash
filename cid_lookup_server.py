#!/usr/bin/python3

import http.server
import socketserver
from urllib.parse import parse_qs
import pandas
import re
import sqlite3


PORT = 8000


class Serv(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(self.path[2:])
        number = params["num"][0]
        city = self.code_lookup(number)
        name = self.cid_lookup(number)
        self.wfile.write(name.encode())
        self.wfile.write("\n".encode())
        self.wfile.write(city.encode())


    def code_lookup(self, cid):
        if not "csv" in globals():
            self.csv = pandas.read_csv("codes.csv", sep=";", index_col=0).T.to_dict()


        cid = cid[1:]
        for i in range(1, len(cid)):
            code = cid[:i]
            if int(code) in self.csv.keys():
                return str(self.csv[int(code)]["city"])
        return "Unknown city"

    def cid_lookup(self, cid):
        if not "cur" in globals():
            self.db = sqlite3.connect("/var/lib/asterisk/astdb.sqlite3")
            self.cur = self.db.cursor()
        self.cur.execute("SELECT value FROM astdb WHERE key='/cidname/{}';".format(cid))

        cid_name = ""
        try:
             cid_name = self.cur.fetchall()[0][0]
        except:
             cid_name = "Unbekannt"

        return cid_name



with socketserver.TCPServer(("", PORT), Serv) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
