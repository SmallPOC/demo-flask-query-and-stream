from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from time import time

app = Flask(__name__)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///playlist.db'
app.config["SQLALCHEMY_ECHO"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Songs(db.Model):
    """ data model for song """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    artist = db.Column(db.String)
    album = db.Column(db.String)
    path = db.Column(db.String)

    def __repr__(self):
        title = " ".join(self.title.split()[:-1])
        return f"{title} - {self.artist} - {self.album}"

db.create_all()


@app.route("/", methods=["GET", "POST"])
def search():
    """ route for seeing results of a search """
    if request.method == 'POST':
        query = request.form.get("artist")
        qry_result = Songs.query.filter_by(artist=query.title()).all()
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
    return render_template("play.html", path=song.path, title=" ".join(song.title.split()[:-1]), artist=song.artist, album=song.album )


if __name__=="__main__":
    app.run(debug=True, host="localhost")
   