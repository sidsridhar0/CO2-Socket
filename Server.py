
import csv
import json
import os
import socket
import sqlite3
from collections import defaultdict

STATES = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida",
          "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
          "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
          "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
          "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
          "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]


class Year():
    def __init__(self, year, avg):
        self.year = year
        self.avg = avg

    def getYear(self):
        return self.year

    def getAvg(self):
        return self.avg

    def setYear(self, y):
        self.year = y

    def setAvg(self, a):
        self.avg = a

    def __str__(self):
        return str(self.avg)


class ExtractCSV():
    def __init__(self, name):
        self.name = name

    def readCSV(self):
        with open(self.name) as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            count = 0
            sdict = defaultdict(list)
            for r in csvReader:
                # print(r)
                if 3 < count < 56:
                    sdict[r[0]] = r[1:52]
                count += 1
        #for bn, v in sdict.items():
            #print(bn, v)
        return sdict


class Database:
    def __init__(self, name):
        self.tn = "data"
        self.n = name
        self.conn = sqlite3.connect(name)
        self.c = self.conn.cursor()
        try:
            self.c.execute("CREATE TABLE " + self.tn + "(states blob)")
            self.conn.commit()
            print(name + " connected")
        except:
            print("table already exists")

    def closeConn(self):
        try:
            self.conn.commit()
            self.conn.close()
            print("successful closeConn()")
        except:
            print("FAILED closeConn()")

    def deleteDB(self):
        try:
            os.remove(self.n)
            print("successful deleteDB()")
        except sqlite3.Error as e:
            print("FAILED deleteDB()", e)

    def addColumn(self, d):
        try:
            temp = f"ALTER TABLE {self.tn} ADD COLUMN {d} BLOB"
            # print(temp)
            self.c.execute(temp)
            self.conn.commit()
            # print("successful addColumn()")
        except sqlite3.Error as e:
            print("FAILED addColumn()", e)

    def getFromDB(self, x):
        # tuple of (col, value)
        try:
            # if True:
            r = self.c.execute(f"SELECT * FROM {self.tn} WHERE states = '{x}'").fetchall()
            print("successful getFromDB()")

            return r
        except sqlite3.Error as e:
            print("FAILED getFromDB()", e)

    def removeFromDB(self, x):
        try:
            with self.conn:
                self.c.execute("DELETE from " + self.tn + " WHERE " + x[0] + " = :val", {'val': x[1]})
            print("successful removeFromDB()")
        except sqlite3.Error as e:
            print("FAILED removeFromDB()", e)

    def getNumCols(self):
        try:
            self.c.execute("SELECT * FROM " + self.tn)
            cols = len(self.c.description)
            # print("successful getNumCols()")
            return cols
        except sqlite3.Error as e:
            print("FAILED getNumCols()")

    def addToDB(self, d):
        try:
            cols = self.getNumCols()
            s = "INSERT INTO " + self.tn + " VALUES (" + ("?, ") * (cols - 1) + "?)"
            dt = (d[0:cols])
            with self.conn:
                self.c.execute(s, dt)
            # print("successful addToDB()")
        except sqlite3.Error as e:
            print("FAILED addToDb()", e)
            # print(d)

    def updateDB(self, d):
        try:
            # if(True):

            self.c.execute("SELECT * from " + self.tn)
            col_names = [i[0] for i in self.c.description]

            cols = self.getNumCols()
            s = "UPDATE " + self.tn + " SET " + d[0] + " = ? WHERE " + d[1] + " = ?"
            # print(s)
            # print(d)
            with self.conn:
                self.c.execute(s, d[2:])

            print("successful updateDB()")
        except sqlite3.Error as e:
            print("FAILED updateDB()", e)

    def query_builder(self, command, data=None):
        try:
            # if True:
            if command == "update":
                self.updateDB(data)
            elif command == "remove":
                self.removeFromDB(data)
            elif command == "get":
                return self.getFromDB(data)
            elif command == "add":
                self.addToDB(data)
            elif command == "close":
                self.closeConn()
            elif command == "deleteDB":
                self.deleteDB()
            elif command == "addColumn":
                self.addColumn(data)
            elif command == "numColumns":
                return self.getNumCols()
            else:
                print("FAILED query_builder()")
        except sqlite3.Error as e:
            print("FAILED query_builder()", e)


def setupDB():
    c = ExtractCSV("USAStatesCO2.csv")
    data = c.readCSV()
    # print(data)

    # cd = CreateData()
    # d = cd.mergeDicts(hdata, sdata)

    db = Database('lab2.db')

    # db.query_builder("addColumn", "states")
    for i in range(1970, 2021):
        db.query_builder("addColumn", "col_" + str(i))
        # print(i - 1970)

    #print(db.query_builder('numColumns'))

    for k, v in data.items():
        # print(bn, v)
        temp = [k]
        temp.extend(v)
        # print(len(temp), temp)
        db.query_builder("add", temp)

    # for i in range(50):
    # print(db.query_builder("get", "California"))

    '''
    db.query_builder('update', ("co2", "year", 400, 1959))
    db.query_builder('remove', ("year", 1960))
    print(db.query_builder('get', ("year", 1959)))
    db.query_builder("addColumn", "test")
    print(db.query_builder('numColumns'))

    for i in range(1959, 2020):
        print(db.query_builder('get', ("year", i)))
    '''
    return db


def server_program(portnumber, db):
    host = socket.gethostname()
    port = portnumber
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("from connected user: " + str(data))
        d = db.query_builder("get", data)
        print(d)
        conn.send(json.dumps(d).encode())

    db.query_builder("close")
    db.query_builder("deleteDB")
    conn.close()


if __name__ == "__main__":
    db = setupDB()
    server_program(5000, db)
