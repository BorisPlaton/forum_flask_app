from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash, Bcrypt
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from wtforms.fields import EmailField, PasswordField, SubmitField, BooleanField, StringField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///forum.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


class User(db.Model, UserMixin):
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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:   # Если пользователь уже в профиле, не разрешит зайти в меню авторизации
        return "<h1>U are already in the account</h1>"

    login_form = LoginForm()    # Форма для входа в аккаунт
    if login_form.validate_on_submit():
        # Смотрим есть ли такой пользователь и совпадают ли пароли
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and check_password_hash(user.password, login_form.password.data):
            login_user(user, login_form.remember.data)  # В случае успеха пользователь входит в аккаунт
        else:
            flash("Неверная почта или пароль", category="danger")
        return redirect(url_for('login'))   # Возвращает в меню авторизации если не удался вход
    return render_template("login.html", form=login_form)


@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:   # Если пользователь уже в профиле, не разрешит зайти в меню регистрации
        return "<h1>U are already in the account</h1>"
    registration_form = RegistrationForm()  # Форма регистрации
    if registration_form.validate_on_submit():
        # Проверяем нет ли уже созданного аккаунта с такой почтой
        if not User.query.filter_by(email=registration_form.email.data).first():
            hash_password = generate_password_hash(registration_form.password.data).decode("utf-8")
            user = User(email=registration_form.email.data,
                        password=hash_password,
                        username=registration_form.username.data)   # Создаем пользователя и хэшируем пароль
            db.session.add(user)
            db.session.commit()
            flash("Аккаунт создан", category="success")
        else:
            flash("Такая почта уже зарегистрирована", category="danger")
            return redirect(url_for("register"))
        return redirect(url_for('login'))
    return render_template("registration.html", form=registration_form)


if __name__ == "__main__":
    app.run(debug=True)
