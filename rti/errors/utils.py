from flask import abort

from flask_login import current_user


def check_roles(roles=[]):
    if current_user.profil.libelle in roles:
        return None
    else:
        abort(403)
