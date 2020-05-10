from flask import Flask, render_template, request
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
    """ route for playing selected song """
    song = Songs.query.get_or_404(id)
    return render_template("play.html", path=song.path, title=song.title, artist=song.artist, album=song.album )


# def make_playlist(path:str):
#     with open("winplaylist.m3u", "w") as f:
#         for path, dirs, folders in os.walk(path):
#             for file in folders:
#                 if file.endswith(".mp3"):
#                     print(os.path.join(path, file), file=f)


def fill_db(path:str):
    with open("winplaylist.m3u", "w") as f:
        for path, dirs, folder in os.walk(root):
            for file in folder:
                if file.endswith(".mp3"):
                    print(file)
                    artist, album, title = file.strip(".mp3").split(" -- ")
                    artist = " ".join(artist.split(" ")[1:])
                    song = Songs(title=title, album=album, artist=artist, path=os.path.join(root, file))
                    db.session.add(song)
                    db.session.commit()


if __name__=="__main__":
    Songs.query.delete()
    root = r"audio"
    # make_playlist(root)
    fill_db(root)
    app.run(debug=True, host="localhost")
   

