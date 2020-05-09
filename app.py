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

    def __repr__(self):
        return f"{self.title} - {self.artist} - {self.album}"

db.create_all()

def get_query_result(query:str) -> list:
    q = Songs.query.filter_by(artist=query).all()
    # result = []
    # for i in q:
    #     title = " ".join(i.title.split()[:-1])
    #     print(title, type(title))
    #     ret = f"{i.artist}  -  {i.album}  -  {title} - {i.id} - {i.path}"
    #     result.append(ret)
    return result      


@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == 'POST':
        query = request.form.get("artist")
        qry_result = Songs.query.filter_by(artist=query.title()).all()
        # print(qry_result
        if qry_result:
            return render_template("search.html", data=qry_result)
        else:
            msg = f"sorry no result found for '{query}'"
            return render_template("search.html", msg=msg)
    return render_template("search.html")



@app.route("/play/<int:id>")
def play(id:int):
    song = Songs.query.get_or_404(id)
    return render_template("play.html", path=song.path)


# @app.route("/post/<int:post_id>")
# def post(post_id:int):
#     """ route for seeing a single post """
#     post = Post.query.get_or_404(post_id)
#     return render_template("post.html", title=post.title, post=post)


if __name__=="__main__":
    app.run(debug=True, host="localhost")
   