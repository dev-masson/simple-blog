from flask import render_template, url_for, flash, redirect, request
from sitedosguri import client, database, bcrypt
from sitedosguri.forms import FormLogin, FormRegister, FormEditProfile, FormCriarPost
from sitedosguri.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import secrets
import os


@client.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('index.html', posts=posts)


@client.route('/contato')
def contato():
    return render_template('contato.html')


@client.route('/usuarios')
@login_required
def usuarios():
    user_list = User.query.all()
    return render_template('usuarios.html', user_list=user_list)


@client.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()

    if form_login.validate_on_submit() and 'loginSubmit' in request.form:

        user = User.query.filter_by(email=form_login.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_login.password.data):
            login_user(user, remember=form_login.remember.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            return redirect(url_for('home'))
        else:
            flash('Login ou senha incorretos', 'danger')

    form_register = FormRegister()

    if form_register.validate_on_submit() and 'registerSubmit' in request.form:
        password_hash = bcrypt.generate_password_hash(form_register.password.data).decode('utf-8')
        user = User(username=form_register.username.data, email=form_register.email.data, password=password_hash)
        database.session.add(user)
        database.session.commit()
        flash(f'Conta criada para o e-mail: {form_register.email.data}', 'success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_register=form_register)


@client.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'Logout feito com sucesso', 'success')
    return redirect(url_for('home'))


@client.route('/perfil')
@login_required
def perfil():
    profile_photo = url_for('static', filename=f"profile_photos/{current_user.image_file}")
    return render_template('perfil.html', profile_photo=profile_photo)


def save_picture(image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(image.filename)
    picture_fn = _ + random_hex + f_ext
    picture_path = os.path.join(client.root_path, 'static/profile_photos', picture_fn)
    output_size = (200, 200)
    i = Image.open(image)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def save_courses(form_courses):
    list_courses = []
    for course in form_courses:
        if 'curso_' in course.name:
            if course.data:
                list_courses.append(course.label.text)
    return ';'.join(list_courses)


@client.route('/perfil/editar', methods=['GET'])
@login_required
def edit_profile():
    error = request.args.get('error')

    if error:
        flash('Erro ao atualizar perfil', 'danger')

    form_edit_profile = FormEditProfile()
    form_edit_profile.username.data = current_user.username
    form_edit_profile.email.data = current_user.email
    if 'Excel' in current_user.cursos:
        form_edit_profile.curso_excel.data = True
    if 'Word' in current_user.cursos:
        form_edit_profile.curso_word.data = True
    if 'PowerPoint' in current_user.cursos:
        form_edit_profile.curso_powerpoint.data = True
    if 'Access' in current_user.cursos:
        form_edit_profile.curso_access.data = True
    if 'VBA' in current_user.cursos:
        form_edit_profile.curso_vba.data = True
    if 'SQL' in current_user.cursos:
        form_edit_profile.curso_sql.data = True
    profile_photo = url_for('static', filename=f'profile_photos/{current_user.image_file}')
    return render_template('editprofile.html', formEditProfile=form_edit_profile, profile_photo=profile_photo)


@client.route('/perfil/editar', methods=['POST'])
@login_required
def edit_profile_post():
    form_edit_profile = FormEditProfile()

    if form_edit_profile.validate_on_submit():
        # Atualiza nome e email do usuário
        user = database.session.query(User).filter(User.id == current_user.id).first()
        user.username = form_edit_profile.username.data
        user.email = form_edit_profile.email.data

        # Salva foto do perfil, se houver
        if form_edit_profile.picture.data:
            new_photo = save_picture(form_edit_profile.picture.data)
            current_user.image_file = new_photo
        
        # Salva lista de cursos
        user.cursos = save_courses(form_edit_profile)
        database.session.commit()
        flash('Perfil atualizado com Sucesso', 'success')
    profile_photo = url_for('static', filename='profile_photos/{}'.format(current_user.image_file))
    return render_template('perfil.html', formEditProfile=form_edit_profile, profile_photo=profile_photo)


@client.route('/post/criar', methods=['GET'])
@login_required
def criar_post():
    form = FormCriarPost()
    error = request.args.get('error')

    if error:
        flash('Erro ao atualizar perfil', 'danger')
    return render_template('criarpost.html', form=form)


@client.route('/post/criar', methods=['POST'])
@login_required
def criar_post_post():
    form = FormCriarPost()

    if form.validate_on_submit():
        post = Post(title=form.titulo.data, content=form.conteudo.data, author=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso', 'success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


@client.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get(post_id)
    
    if current_user == post.author:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.title
            form.conteudo.data = post.content
        elif form.validate_on_submit():
            post.title = form.titulo.data
            post.content = form.conteudo.data
            database.session.commit()
            flash('Post atualizado com sucesso', 'success')
            return redirect(url_for('home'))
    else:
        form = None

    return render_template('post.html', post=post, form=form)