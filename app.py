from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash, Bcrypt
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import Form
from wtforms.fields import EmailField, PasswordField, SubmitField, BooleanField, StringField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"user {self.username}"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"title {self.title} id {self.id} date {self.date_post}"


class LoginForm(FlaskForm):
    email = StringField("Почта",
                        validators=[InputRequired("Необходимо ввести почту"), Email("Нужно ввести почту")],
                        render_kw={"style": "width: 100%;",
                                   "autocomplete": "off"})
    password = PasswordField("Пароль",
                             validators=[InputRequired("Необходимо ввести пароль")],
                             render_kw={"style": "width: 100%;",
                                        "autocomplete": "off"})
    remember = BooleanField("Запомнить меня", default=False)
    submit = SubmitField("Войти", render_kw={"style": "width: 30%;"})


class RegistrationForm(FlaskForm):
    email = StringField("Почта",
                        validators=[InputRequired("Введите почту"), Email("Нужно ввести почту")],
                        render_kw={"style": "width: 100%;",
                                   "autocomplete": "off"})
    password = PasswordField("Пароль",
                             validators=[InputRequired("Введите пароль"),
                                         Length(min=1, max=30)],
                             render_kw={"style": "width: 100%;",
                                        "autocomplete": "off"})
    confirm_password = PasswordField("Повторите пароль",
                                     validators=[InputRequired("Повторите пароль"),
                                                 EqualTo("password", message="Пароли должны совпадать")])
    username = StringField("Ваше имя", validators=[InputRequired("Введите ваше имя"),
                                                   Length(min=1, max=30)],
                           render_kw={"style": "width: 100%;",
                                      "autocomplete": "off"})
    submit = SubmitField("Зарегистрироваться")

    def validation_email(self, email):
        """Проверяет уникальность почты"""
        email_presence = User.query.filter_by(email=email.data).first()
        if email_presence:  # Запрос должен быть пустым, в ином случае почта уже зарегистрирована
            raise ValidationError("Такая почта уже зарегистрирована")


@app.route("/login", methods=["POST", "GET"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        pass
    return render_template("login.html", form=login_form)


@app.route("/register", methods=["POST", "GET"])
def register():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        hash_password = generate_password_hash(registration_form.password.data).decode("utf-8")
        user = User(email=registration_form.email.data,
                    password=hash_password,
                    username=registration_form.username.data)
        db.session.add(user)
        db.session.commit()
        flash("Аккаунт создан", category="success")
        return redirect(url_for('login'))
    return render_template("registration.html", form=registration_form)


if __name__ == "__main__":
    app.run(debug=True)
