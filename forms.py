from flask_wtf import FlaskForm
from wtforms.fields import EmailField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email


class LoginForm(FlaskForm):
    email = EmailField("Почта",
                       validators=[InputRequired("Email is required")],
                       render_kw={"style": "width: 100%;",
                                  "autocomplete": "off"})
    password = PasswordField("Пароль",
                             validators=[InputRequired()],
                             render_kw={"style": "width: 100%;",
                                        "autocomplete": "off"})
    remember = BooleanField("Запомнить меня", default=False)
    submit = SubmitField("Войти", render_kw={"style": "width: 30%;"})
