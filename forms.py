from flask_wtf import FlaskForm
from wtforms import Form
from wtforms.fields import EmailField, PasswordField, SubmitField, BooleanField, StringField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    email = EmailField("Почта",
                       validators=[InputRequired("Необходимо ввести почту")],
                       render_kw={"style": "width: 100%;",
                                  "autocomplete": "off"})
    password = PasswordField("Пароль",
                             validators=[InputRequired("Необходимо ввести пароль")],
                             render_kw={"style": "width: 100%;",
                                        "autocomplete": "off"})
    remember = BooleanField("Запомнить меня", default=False)
    submit = SubmitField("Войти", render_kw={"style": "width: 30%;"})


class RegistrationForm(FlaskForm):
    email = EmailField("Почта",
                       validators=[InputRequired("Необходимо ввести почту")],
                       render_kw={"style": "width: 100%;",
                                  "autocomplete": "off"})
    password = PasswordField("Пароль",
                             validators=[InputRequired("Необходимо ввести пароль"),
                                         Length(min=1, max=30)],
                             render_kw={"style": "width: 100%;",
                                        "autocomplete": "off"})
    username = StringField("Ваше имя", validators=[InputRequired("Введите ваше имя"),
                                                   Length(min=1, max=30)],
                           render_kw={"style": "width: 100%;",
                                      "autocomplete": "off"})
    submit = SubmitField("Зарегистрироваться")
