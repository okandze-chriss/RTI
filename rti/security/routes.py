import datetime

from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required

from rti import bcrypt, db
from rti.dashboard.utils import send_welcome_email
from rti.models import User, load_profil
from rti.security import security
from rti.security.forms import LoginForm, RequestResetForm, ResetPasswordForm
from rti.security.utils import send_reset_email


@security.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('security.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if form.email.data == 'jordyokandze77@gmail.com' and user is None:
            hashed_password = bcrypt.generate_password_hash("passer").decode('utf-8')
            user = User(
                nom="OKANDZE",
                prenom="Chriss Jordy",
                date_nais=datetime.date(1998, 9, 21),
                email='jordyokandze77@gmail.com',
                password=hashed_password,
                tel="781150585",
                type_piece="Passeport",
                num_piece="AB40049",
                photo_piece="chriss.png",
                profil=load_profil('ADMIN')
            )
            db.session.add(user)
            db.session.commit()
            send_welcome_email(user)
            load_profil('CLIENT')
            load_profil('COMPTABLE')
            user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.profil.libelle == 'CLIENT':
                flash('Les clients n\'ont pas access à la plateforme.', 'danger')
            elif user.blocked:
                flash('Cet utilisateur à été bloqué .', 'danger')
            else:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash('Bienvenue {} !!'.format(user.nom), 'success')
                return redirect(next_page) if next_page else redirect(url_for('security.home'))
        else:
            flash('Echec de connexion. Veuillez véifier votre email et votre mot de passe', 'danger')
        pass
    return render_template('authentification/login.html', form=form)


@security.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('security.login'))


@security.route('/dashboard')
@login_required
def home():
    return render_template('dashboard/index.html', user=current_user)

#
# @security.route('/sign-up')
# def new2():
#     return render_template('authentification/sign-up.html')


@security.route('/forgot/password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('security.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('Un email a été envoyé avec les instructions pour la rénitialisation.', 'info')
        return redirect(url_for('security.login'))
    return render_template('authentification/forgotpwd.html', form=form)


@security.route("/reset/password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('security.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('security.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Votre mot de passe a été mis à jour! Connectez vous !', 'success')
        return redirect(url_for('security.login'))
        # flash('Your password has been updated! You are now able to log in', 'success')
    return render_template('authentification/forgot_password.html', form=form, userglobal=current_user)
