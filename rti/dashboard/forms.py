import os
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FileField, \
    DateField, TelField, SelectField, IntegerField, FieldList, DateTimeField
from wtforms.validators import DataRequired, Email, ValidationError, NumberRange
from rti.models import User

typePiece = [('Passeport', 'Passeport'),
             ('Visa', 'Visa'),
             ("carte d'identité nationale", "carte d'identité nationale"),
             ('carte de residence permanante', "carte de residence permanante")
             ]


class NewAdminForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prenom', validators=[DataRequired()])
    date_nais = DateField("Date de naissance", format="%Y-%m-%d", validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    # password = PasswordField('Mot de passe', validators=[DataRequired()])
    tel = TelField('Numero de téléphone', validators=[DataRequired()])
    type_piece = SelectField("Type de piece d'identité", validators=[DataRequired()], choices=typePiece)
    profile = SelectField("Rôle à jouer", validators=[DataRequired()], choices=[])
    num_piece = StringField("Numero de piece d'identité", validators=[DataRequired()])
    photo_piece = FileField("Photo de piece d'identité", validators=[DataRequired(), FileAllowed(['jpg', 'jpeg','png'], message="Elle doit être de forma :[jpg/jpeg/png]")])
    avatar = FileField("Avatar", validators=[FileAllowed(['jpg', 'jpeg', 'png'], message="Elle doit être de forma :[jpg/jpeg/png]")])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Il y a déja un compte relié à ce mail')


class UpdateInformAdmin(FlaskForm):
    nom = StringField('nom', validators=[DataRequired()])
    prenom = StringField('prenom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    date_nais = DateField("Date de naissance", format="%Y-%m-%d", validators=[DataRequired()])
    tel = TelField('Numero de téléphone', validators=[DataRequired()])
    type_piece = SelectField("Type de piece d'identité", validators=[DataRequired()], choices=typePiece)
    num_piece = StringField("Numero de piece d'identité", validators=[DataRequired()])
    photo_piece = FileField("Photo de piece d'identité", validators=[FileAllowed(['jpg', 'jpeg', 'heic', 'png'], message="Elle doit être de forma :[jpg/jpeg/png]")])
    avatar = FileField('Modifier la piece', validators=[FileAllowed(['jpg', 'jpeg', 'heic', 'png'])])
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Enregistrer')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Cet email est déja enregistré. Veuillez en choisir un autre')


# Formulaire de Duree
class DureeForm(FlaskForm):
    libelle = SelectField('Duree', choices=[], validators=[DataRequired()])


# Formulaire de Taux
class TauxForm(FlaskForm):
    montant = IntegerField('Taux', validators=[DataRequired()])


# Formulaire de retrait
class ForfaitForm(FlaskForm):
    libelle = StringField('Libelle', validators=[DataRequired()])
    borne_inf = IntegerField('Montant inferieur', validators=[DataRequired(), NumberRange(min=10000)])
    borne_sup = IntegerField('Montant Supperieur', validators=[DataRequired(), NumberRange(min=10000)])
    taux = FieldList(IntegerField('Taux', validators=[DataRequired(), NumberRange(min=1, max=100)]), min_entries=1)
    duree = FieldList(SelectField('Duree', choices=[], validators=[DataRequired()]), min_entries=1)
    submit = SubmitField('Valider')

# Formulaire d'investissement
class InvestmentForm(FlaskForm):
    montant = IntegerField('Montant', validators=[DataRequired()])
    actif = IntegerField('Actif', validators=[DataRequired()])
    date = DateTimeField("date d'investissement", validators=[DataRequired()])
    forfait = SelectField('Choisir', validators=[DataRequired()])
    submit = SubmitField('Valider')


# Formulaire de retrait
class WithdrawalForm(FlaskForm):
    montant = IntegerField('Montant', validators=[DataRequired()])
    justificatif = StringField('justificatif', validators=[DataRequired()])
    date = DateField("date d'investissement", validators=[DataRequired()])
    submit = SubmitField('Valider')


# pour forfait et duré
class GenerateForm(FlaskForm):
    nombre = IntegerField("Nombre", validators=[DataRequired(), NumberRange(min=1, max=10)])
    duree = SelectField("Duree", choices=[('MOIS', 'MOIS'), ('AN', 'AN')], validators=[DataRequired()])


def removeFile(filename):
    if os.path.exists('rti/static/img/avatar/'+ filename):
        return os.remove('rti/static/img/avatar/'+ filename)
    else:
        return "Impossible de supprimer le fichier car il n'existe pas"