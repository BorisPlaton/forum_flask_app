from flask import Flask, render_template, url_for, flash
from forms import LoginForm, RegistrationForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
#
# db = SQLAlchemy(app)
#
#
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.Text, unique=True, nullable=False)
#     password = db.Column(db.String(30), nullable=False)
#     username = db.Column(db.String(30), nullable=False)
#
#     def __repr__(self):
#         return f"user {self.username}"


@app.route("/login", methods=["POST", "GET"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        return f'<h1>Email: {login_form.email.data} Password: {login_form.password.data}</h1>'
    return render_template("login.html", form=login_form)


@app.route("/register", methods=["POST", "GET"])
def register():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        return f'<h1>Email: {registration_form.email.data} Password: {registration_form.password.data} Username {registration_form.username.data}</h1>'
    return render_template("registration.html", form=registration_form)


if __name__ == "__main__":
    app.run(debug=True)
