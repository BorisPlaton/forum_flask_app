from flask import Flask, render_template, url_for
from forms import LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"


@app.route("/login", methods=["POST", "GET"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        return f'<h1>Email: {login_form.email.data} Password: {login_form.password.data}</h1>'
    return render_template("login.html", form=login_form)


if __name__ == "__main__":
    app.run(debug=True)
