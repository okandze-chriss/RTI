from datetime import datetime, date
from flask import current_app, session
from sqlalchemy.sql import expression
from sqlalchemy import func, text, extract
from rti import db, loginManager
from flask_login import UserMixin, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from random import *
from sqlalchemy import or_
from time import gmtime, strftime


# ***************  USER TABLE *******************
class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    date_nais = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), nullable=False)  # AutoGenerate
    tel = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())  # Default value
    blocked = db.Column(db.Boolean, nullable=False, default=False)  # Default value
    type_piece = db.Column(db.String(100), nullable=False)
    num_piece = db.Column(db.String(100), nullable=False)
    photo_piece = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(150), default='profil.png', nullable=True)  # Default value
    profil_id = db.Column(db.Integer, db.ForeignKey('Profil.id'), nullable=False)

    retraits = db.relationship('Retrait', backref='user', lazy=True)
    investissement = db.relationship('Investissement', backref='user', lazy=True)
    logs = db.relationship('Logs', backref='user', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


# ***************  PROFILE TABLE *******************
class Profil(db.Model):
    __tablename__ = 'Profil'
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(50), nullable=False, unique=True, default="CLIENT")
    users = db.relationship('User', backref='profil', lazy=True)


# ***************  RETRAIT TABLE *******************
class Retrait(db.Model):
    __tablename__ = 'Retrait'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    montant = db.Column(db.Float, nullable=False)
    justificatif = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)


# ***************  INVESTMENT TABLE *******************
class Investissement(db.Model):
    __tablename__ = 'Investissement'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    montant = db.Column(db.Float, nullable=False)
    actif = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    forfait_id = db.Column(db.Integer, db.ForeignKey('Forfait.id'), nullable=False)


# ***************  LOGS TABLE *******************
class Logs(db.Model):
    __tablename__ = 'Logs'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    titre = db.Column(db.String(100), nullable=False)
    texte = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)


# ***************  FORFAIT TABLE *******************
class Forfait(db.Model):
    __tablename__ = 'Forfait'
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(50), nullable=False)
    borne_inf = db.Column(db.Float, nullable=False)
    borne_sup = db.Column(db.Float, nullable=False)
    investissements = db.relationship('Investissement', backref='forfait', lazy=True)
    taux = db.relationship('Taux', backref='forfait', lazy=True)


# ***************  TAUX TABLE *******************
class Taux(db.Model):
    __tablename__ = 'Taux'
    id = db.Column(db.Integer, primary_key=True)
    taux_interet = db.Column(db.Float, nullable=False)
    forfait_id = db.Column(db.Integer, db.ForeignKey('Forfait.id'), nullable=False)
    duree_id = db.Column(db.Integer, db.ForeignKey('Duree.id'), nullable=False)


# ***************  DUREE TABLE *******************
class Duree(db.Model):
    __tablename__ = 'Duree'
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(50), nullable=False)
    taux = db.relationship('Taux', backref='duree', lazy=True)


# ***************  GET USER BY ID *******************
@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# *****************  FILTER BY LIBELLE *****************
def load_profil(profil_libelle):
    profil = Profil.query.filter_by(libelle=profil_libelle).first()
    if profil:
        return profil
    else:
        profil = Profil(libelle=profil_libelle)

        db.session.add(profil)
        db.session.commit()
        return Profil.query.filter_by(libelle=profil_libelle).first()


# *****************  GET ALL USER *****************
def load_all_admin():
    return User.query.all()


# *****************  GET ALL PROFILE *****************
def load_all_profil():
    return Profil.query.all()

# def erase_db():
#     sql = text('SET FOREIGN_KEY_CHECKS = 0')
#     result = db.engine.execute(sql)
#     sql = text('TRUNCATE TABLE `participer`')
#     result = db.engine.execute(sql)
#     sql = text('TRUNCATE TABLE `proposition`')
#     result = db.engine.execute(sql)
#     sql = text('TRUNCATE TABLE `journeetravaux`')
#     result = db.engine.execute(sql)
#     sql = text('TRUNCATE TABLE `chalet`')
#     result = db.engine.execute(sql)
#     sql = text('TRUNCATE TABLE `membre`')
#     result = db.engine.execute(sql)
#     sql = text('SET FOREIGN_KEY_CHECKS = 1')
#     result = db.engine.execute(sql)
