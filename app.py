from flask import Flask, render_template, url_for
from forms import LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
