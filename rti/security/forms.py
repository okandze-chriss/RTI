from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField, DateField, EmailField, TelField)
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from wtforms.fields import FileField
from rti.models import User


# Formulaire d'authetification
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Se rappeler de moi')
    submit = SubmitField('Login')


# Formulaire de requete de  renitialisation de mot de passe
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Rénitialiser mon mot de passe')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Il n\'y a pas de compte relié à ce mail. Vous devez avoir un compte.')


# Formulaire de renitialisation de mot passe
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Rénitialiser mon mot de passe')


# Formulaire de l'utilisateur
class UserForm(FlaskForm):
    nom = StringField('Montant', validators=[DataRequired()])
    prenom = StringField('Montant', validators=[DataRequired()])
    date = DateField("date de naissance", validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    tel = TelField('Numero de téléphone', validators=[DataRequired()])
    type_piece = StringField("Type de piece d'identité", validators=[DataRequired()])
    numero_piece = StringField("numero de piece d'identité", validators=[DataRequired()])
    photo_piece = FileField("photo de piece d'identité", validators=[DataRequired()])
    avatar = FileField("Avatar")
    submit = SubmitField('Enregistrer')
