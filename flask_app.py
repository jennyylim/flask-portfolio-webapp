from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True

# --------------------------------------------------------------------
#  DATABASE CONFIG  (Replace YOURPASSWORD with your MySQL password)
# --------------------------------------------------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+mysqlconnector://JennyALim:jenny12345@JennyALim.mysql.pythonanywhere-services.com/JennyALim$mydatabase"
)
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


#  DATABASE
class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096), nullable=False)


#  ROUTES
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        all_comments = Comment.query.all()
        return render_template("main_page.html", comments=all_comments)

    # POST: add new comment
    new_comment = Comment(content=request.form["contents"])
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for("index"))


#  DELETE COMMENT
@app.route("/delete/<int:comment_id>", methods=["POST"])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
