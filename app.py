from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["SECRET_KEY"] = "myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "lhanco@gmail.com"
app.config["MAIL_PASSWORD"] = os.getenv("Python_App_Send_Email")

db = SQLAlchemy(app)

mail = Mail(app)


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
        try:
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

            message_body = f"Thank you for your submission, {first_name}. \n" \
                           f"Here are your data: \n{first_name}\n{last_name}\n{start_date}\n" \
                           f"Thank you!"
            mail_message = Message(subject="New job form submission",
                                   sender=app.config["MAIL_USERNAME"],
                                   recipients=[email],
                                   body=message_body)
            mail.send(mail_message)

            flash(f"{first_name}, your form was submitted successfully!", category="success")
        except Exception as error:
            flash(f"{first_name}, your form was submitted failed!", category="danger")
            flash(f"{str(error)}", category="danger")

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
