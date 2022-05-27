from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
from rti import bcrypt, db
from rti.dashboard import dashboard
from rti.dashboard.forms import NewAdminForm, UpdateInformAdmin, removeFile, ForfaitForm, DureeForm
from rti.dashboard.utils import save_file, send_welcome_email, insertToDB, get_roles
from rti.models import User, load_profil, load_all_admin, load_user, load_all_profil, Profil, Forfait, Taux, Duree
from rti.dashboard.forms import GenerateForm
from rti.security.utils import save_piece_form


# ========================= USER =================================
@dashboard.route('/new/admin', methods=['GET', 'POST'])
@dashboard.route('/new/client', methods=['GET', 'POST'])
@login_required
def user_new():
    form = NewAdminForm()
    url = ""
    role = []
    profil = Profil()
    if str(request.url_rule) == "/new/admin":
        url = 'dashboard/admin/new.html'
        role = get_roles()
    elif str(request.url_rule) == "/new/client":
        profil = load_profil('CLIENT')
        url = 'dashboard/client/new.html'
        role = [(role.id, role.libelle) for role in Profil.query.filter_by(libelle="CLIENT")]

    form.profile.choices = role
    if form.validate_on_submit():
        if str(request.url_rule) == "/new/admin":
            profil = Profil.query.get(int(form.profile.data))

        passwordGenerated = datetime.now().strftime("%H%M%H%M%S")
        hashed_password = bcrypt.generate_password_hash(passwordGenerated).decode('utf-8')
        picture_file = save_piece_form(form.photo_piece.data)
        user = User()
        user.nom = form.nom.data
        user.prenom = form.prenom.data
        user.date_nais = form.date_nais.data
        user.password = hashed_password
        user.tel = form.tel.data
        user.email = form.email.data
        user.type_piece = form.type_piece.data
        user.num_piece = form.num_piece.data
        user.photo_piece = picture_file
        user.profil = profil
        if form.avatar.data:
            user.avatar = save_piece_form(form.avatar.data)
        insertToDB([user])
        send_welcome_email(user)
        print(passwordGenerated)
        if str(request.url_rule) == "/new/admin":
            flash('Nouvel administrateur ajouté avec succès. Un email lui a été envoyé pour qu\'il puisse se connecter',
                  'success')
            return redirect(url_for('dashboard.admin_list'))
        else:
            flash('Nouveau client ajouté avec succès !', 'success')
            return redirect(url_for('dashboard.client_list'))

    return render_template(url, form=form, user=current_user)


@dashboard.route('/profile/admin/<int:id>', methods=['GET', 'POST'])
@dashboard.route('/profile/admin', methods=['GET', 'POST'])
@login_required
def edit_user(id=None):
    user = User()
    url = ""
    if id:
        user = load_user(int(id))
        url = 'dashboard/client/edit.html'
    else:
        user = current_user
        url = 'dashboard/admin/edit.html'

    form = UpdateInformAdmin(obj=user)
    if form.validate_on_submit():
        user.nom = form.nom.data
        user.prenom = form.prenom.data
        user.email = form.email.data
        user.tel = form.tel.data
        user.num_piece = form.num_piece.data
        user.type_piece = form.type_piece.data

        if form.password.data != '':
            if form.password.data == form.confirm_password.data:
                user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            else:
                flash(
                    'La modification du mot de passe n\'a pas été pris en compte car les mots de passe ne correspondent pas.',
                    'danger')
        if form.avatar.data:
            user.avatar = save_piece_form(form.avatar.data)
        if form.photo_piece.data:
            user.photo_piece = save_piece_form(form.photo_piece.data)
        db.session.commit()
        flash('Données modifiées avec succès', 'success')
        return redirect(url_for('dashboard.edit_user'))
    return render_template(url, form=form, user=user)


@dashboard.route('/block/user/<int:id>', methods=['GET', 'POST'])
@login_required
def block_user(id):
    user = load_user(int(id))
    if current_user.profil.libelle == "ADMIN":
        print(current_user.profil.libelle)
        if user.blocked:
            user.blocked = False
            db.session.commit()
            flash('Le compte à été Débloqué', 'success')
            return redirect(url_for('dashboard.admin_list'))
        else:
            user.blocked = True
            print('false')
            db.session.commit()
            flash('Le compte à été bloqué', 'danger')
            return redirect(url_for('dashboard.admin_list', user=current_user))
    else:
        flash('L\'administrateur seul à se droit', 'danger')
    return render_template('dashboard/admin/index.html', user=current_user, admins=load_all_admin())


@dashboard.route('/delete/user/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    try:
        user = load_user(int(id))
        removeFile(user.photo_piece)
        removeFile(user.avatar)
        db.session.delete(user)
        db.session.commit()
        if user.profil.libelle == "ADMIN" or user.profil.libelle == "COMPTABLE":
            flash('Administrateur supprimé avec succès', 'success')
        else:
            flash('Client supprimé avec succès', 'success')
            return redirect(url_for('dashboard.client_list'))
    except:
        flash('Impossible de supprimer l\'admin', 'error')
        return redirect(url_for('dashboard.admin_list'))


# ========================= ADMIN AND ACCOUNTING =================================
@dashboard.route('/list/admin')
@login_required
def admin_list():
    return render_template('dashboard/admin/index.html', user=current_user, admins=load_all_admin())


# ========================= CLIENT =================================
@dashboard.route('/list/client')
@login_required
def client_list():
    clients = User.query.all()
    return render_template('dashboard/client/list.html', user=current_user, clients=clients)


# ========================= OTHERS =================================
@dashboard.route('/delete/other/<int:id>', methods=['GET', 'POST'])
@login_required
def other_delete(id):
    pass


# ========================= TAUX & DUREE =================================
@dashboard.route('/list/taux-duree/<int:id>')
@dashboard.route('/list/taux-duree')
@login_required
def taux_duree_list(id=None):
    duree = Duree.query.all()
    taux = Taux.query.all()
    form = GenerateForm()
    if form.validate_on_submit():
        print(form.data)
    return render_template('dashboard/tauxduree/list.html', formDuree=form, user=current_user, duree=duree, taux=taux)


@dashboard.route('/add/duree', methods=['GET', 'POST'])
@login_required
def addDuree():

    if request.method == "POST":
        if request.form.get('nombre'):
            nombre = request.form.get('nombre')
            duree = request.form.get('duree')
            libelle = nombre + ' ' + duree
            if Duree.query.filter_by(libelle=libelle).first():
                flash('Cette durée existe déjà, changer s\'il vous plaît !', category='danger')
            else:
                duree = Duree(libelle=libelle)
                insertToDB([duree])
    return redirect(url_for('dashboard.forfait_new'))


# ========================= FORFIAT =================================
@dashboard.route('/list/forfait')
@login_required
def forfait_list():
    forfaits = Forfait.query.all()
    return render_template('dashboard/forfait/list.html', user=current_user, forfaits=forfaits)


@dashboard.route('/new/forfait', methods=['GET', 'POST'])
@login_required
def forfait_new():
    form = ForfaitForm(request.form)
    formDuree = GenerateForm()
    countDuree = Duree.query.all()

    print(request.data)

    form.duree.min_entries = Duree.query.count()
    form.taux.min_entries = Duree.query.count()
    if not form.libelle.data:
        form.process()
    for dure in form.duree:
        dure.choices = [(role.id, role.libelle) for role in Duree.query.all()]
    if form.validate_on_submit():
        count = 0
        if Forfait.query.filter_by(libelle=form.libelle.data).first():
            flash(('Ce Forfait existe déjà, changer s\'il vous plaît !'), category='danger')
        else:
            forfait = Forfait(libelle=form.libelle.data, borne_inf=form.borne_inf.data, borne_sup=form.borne_sup.data)
            db.session.add(forfait)
            for cpt in form.duree.data:
                duree = Duree.query.get(int(cpt))
                taux = Taux(taux_interet=form.taux.data[count], forfait=forfait, duree=duree)
                db.session.add(taux)
                print(form.taux.data)
                count += 1
            db.session.commit()
            flash(('Forfait ajouté avec succes !'), category='success')
            return redirect('/list/forfait')
    return render_template('dashboard/forfait/new.html', formDuree=formDuree, duree=countDuree, form=form,
                           user=current_user)


@dashboard.route('/edit/<int:id>', methods=['GET', 'POST'])
def forfait_edit(id):
    print(id)
    # return render_template('dashboard/forfait/edit.html', user=current_user)
    return "{}".format(id)


@dashboard.route('/delete/<int:id>', methods=['GET', 'POST'])
def forfait_delete(id):
    return "{}".format(id)


# ========================= RETRAIT =================================
@dashboard.route('/admin/new/forfait')
def retrait_new():
    return render_template('dashboard/forfait/new.html', user=current_user)


@dashboard.route('/admin/list/forfait')
def retrait_list():
    return render_template('dashboard/forfait/list.html', user=current_user)


@dashboard.route('/admin/edit/forfait')
def retrait_edit():
    return render_template('dashboard/forfait/edit.html', user=current_user)


@dashboard.route('/admin/delete/forfait')
def retrait_delete():
    return render_template('dashboard/forfait/edit.html', user=current_user)
