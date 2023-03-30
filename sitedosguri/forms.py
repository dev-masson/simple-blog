from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from sitedosguri.models import User
from flask_login import current_user

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    remember = BooleanField('Lembrar Dados de Acesso')
    loginSubmit = SubmitField('Fazer Login')




class FormRegister(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirm_password = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('password')])
    registerSubmit = SubmitField('Criar Conta')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Nome de usuário já existente. Por favor, escolha outro.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Endereço de email já cadastrado. Por favor, escolha outro ou faça login.')


class FormEditProfile(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    picture = FileField('Atualizar Foto de Perfil' ,validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    editProfilesubmit = SubmitField('Atualizar')

    curso_excel = BooleanField('Excel')
    curso_word = BooleanField('Word')
    curso_powerpoint = BooleanField('PowerPoint')
    curso_access = BooleanField('Access')
    curso_vba = BooleanField('VBA')
    curso_sql = BooleanField('SQL')


    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Nome de usuário já existente. Por favor, escolha outro.')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Endereço de email já cadastrado. Por favor, escolha outro.')
            

class FormCriarPost(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(2, 140)])
    conteudo = TextAreaField('Conteúdo', validators=[DataRequired()])
    submitPost = SubmitField('Criar Post')