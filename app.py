import flask
from flask import request, jsonify, make_response
import random
import socket
import json
import mariadb
import os
import sys

app = flask.Flask(__name__)
app.config["DEBUG"] = True




@app.route('/', methods=['GET'])
def home():
    response = make_response("qotd")
    response.mimetype = "text/plain"
    return prepareResponse(response)

@app.route('/version', methods=['GET'])
def version():
    response = make_response("v1")
    response.mimetype = "text/plain"
    return prepareResponse(response)

@app.route('/writtenin', methods=['GET'])
def writtenin():
    response = make_response("Python 3.8")
    response.mimetype = "text/plain"
    return prepareResponse(response)

@app.route('/quotes', methods=['GET'])
def getQuotes():
    return prepareResponse(jsonify(replaceHostname(quotes)))

@app.route('/quotes/<int:id>', methods=['GET'])
def getQuoteById(id):
    return prepareResponse(jsonify(replaceHostname(quotes[id])))

@app.route('/quotes/random', methods=['GET'])
def getRandom():
    try:
        conn = mariadb.connect(
        user="root",
        password="admin",
        host=os.environ.get('DB_SERVICE_NAME'),
        database="quotesdb",
        port=3306)
        db_cursor = conn.cursor(dictionary=True)
        db_cursor.execute("SELECT '-hostname-' as hostname, id, quotation, author FROM quotes ORDER BY author, id") 
        quotes = mycursor.fetchall()
        conn.close()
        n = random.randint(0,(mycursor.rowcount)-1)
        
        return prepareResponse(jsonify(replaceHostname(quotes[n])))

    except mariadb.Error as e:
        print("Error connecting to db")
        sys.exit(1)



    return prepareResponse(jsonify(replaceHostname(quotes[n])))

def prepareResponse(response):
    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def replaceHostname(jsondoc):
    q = json.dumps(jsondoc)
    q = q.replace('{hostname}', socket.gethostname())
    return json.loads(q)

if __name__ == '__main__':
    app.run(host="localhost", port=10000)