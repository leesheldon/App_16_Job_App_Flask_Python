from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

db = SQLAlchemy(app)


class JobForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    occupation = db.Column(db.String(80))
    start_date = db.Column(db.Date)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        start_date = request.form["start_date"]
        date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        job_form = JobForm(first_name=first_name, last_name=last_name, email=email,
                           start_date=date_obj, occupation=occupation)
        db.session.add(job_form)
        db.session.commit()

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)




















