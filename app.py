from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request
from time import time


app = Flask(__name__)
db = SQLAlchemy(app)
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///playlist.db'
app.config["SQLALCHEMY_ECHO"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class MemberDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    added = db.Column(db.DateTime)

class Songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    artist = db.Column(db.String)
    album = db.Column(db.String)
    path = db.Column(db.String)

db.create_all()

def get_query_result(query:str) -> list:
    q = Songs.query.filter_by(artist=query).all()
    result = []
    for i in q:
        ret = f"{i.artist} - {i.album} - {i.title}"
        result.append(ret)
    return result
        


@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == 'POST':
        query = request.form.get("search")
        qry_result = get_query_result(query)
        print(qry_result)
        return render_template("search.html", data=qry_result)
    return render_template("search.html")


if __name__=="__main__":
    app.run(debug=True, host="localhost")
   