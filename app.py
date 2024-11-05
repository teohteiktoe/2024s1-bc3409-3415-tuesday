from flask import Flask,render_template,request
import google.generativeai as genai
import os
from textblob import TextBlob
import sqlite3
import datetime

api = os.getenv("MAKERSUITE_API_TOKEN") 
genai.configure(api_key=api)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/main",methods=["GET","POST"])
def main():
    q = request.form.get("q")
    currentDateTime = datetime.datetime.now()
    currentDateTime
    conn = sqlite3.connect('userlog.db')
    c = conn.cursor()
    c.execute('INSERT INTO user (name,timestamp) VALUES(?,?)',(q,currentDateTime))
    conn.commit()
    c.close()
    conn.close()
    return(render_template("main.html"))

@app.route("/userlog",methods=["GET","POST"])
def userlog():
    conn = sqlite3.connect('userlog.db')
    c = conn.cursor()
    c.execute('select * From user')
    r=""
    for row in c:
        print(row)
        r = r + str(row)
    c.close()
    conn.close()
    return(render_template("userlog.html",r=r))

@app.route("/financial_QA",methods=["GET","POST"])
def financial_QA():
    return(render_template("financial_QA.html"))

@app.route("/makersuite",methods=["GET","POST"])
def makersuite():
    q = request.form.get("q")
    r = model.generate_content(q)
    return(render_template("makersuite.html",r=r.text))

@app.route("/SA",methods=["GET","POST"])
def SA():
    return(render_template("SA.html"))

@app.route("/SAR",methods=["GET","POST"])
def SAR():
    q = request.form.get("q")
    r = TextBlob(q).sentiment
    return(render_template("SAR.html",r=r))

@app.route("/TM",methods=["GET","POST"])
def TM():
    return(render_template("TM.html"))

if __name__ == "__main__":
    app.run()
