""" This is a simple demo showing how to query an audio file from a database and stream it online. It is one file app for simple demonstration of the concept (querying and streaming the chosen file) """ 

from flask import Flask, Response, render_template, request
from flask_sqlalchemy import SQLAlchemy
from time import time
import os

app = Flask(__name__)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///app.db'
app.config["SQLALCHEMY_ECHO"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Songs(db.Model):
    """ data model for song """
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String)
    title = db.Column(db.String)
    album = db.Column(db.String)
    path = db.Column(db.String)

    def __repr__(self):
        return f"{self.title} - {self.artist} - {self.album}"

db.create_all()


@app.route("/", methods=["GET", "POST"])
def search():
    """ route for seeing results of a search """
    if request.method == 'POST':
        query = request.form.get("artist")
        qry_result = Songs.query.filter_by(artist=query).all()
        print(qry_result)
        if qry_result:
            return render_template("search.html", data=qry_result)
        else:
            msg = f"sorry no result found for '{query}'"
            return render_template("search.html", msg=msg)
    return render_template("search.html")


@app.route("/play/<int:id>")
def play(id:int):
    """ route for playing a song selected from database """
    song = Songs.query.get_or_404(id)
    def gen():
        with open(song.path, "rb") as f:
            data = f.read(1024)
            while data:
                yield data
                data = f.read(1024)
    return Response(gen(), mimetype="audio/mp3")


def fill_db(root:str):
    """ function that fills the database with song audio files info """
    for path, dirs, folder in os.walk(root):
        for file in folder:
            if file.endswith(".mp3"):
                print(file)
                artist, album, title = file.strip(".mp3").split(" -- ")
                artist = " ".join(artist.split(" ")[1:])
                song = Songs(title=title, album=album, artist=artist, path=os.path.join(root, file))
                db.session.add(song)
                db.session.commit()


def main():
    Songs.query.delete() # deleting DB each time it runs.. just for debug puropose to work with clean..
    root = r"audio"
    fill_db(root)
    app.run(debug=True, host="localhost")
   

if __name__=="__main__":
    main()
   

