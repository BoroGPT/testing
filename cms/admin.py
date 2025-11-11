"""
Admin interface for the CMS using Flask-Admin
"""
from flask import redirect, url_for, request, flash
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user
from cms.models import db, User, Content, ContentType, Media, Category, Tag
from wtforms import PasswordField
from werkzeug.security import generate_password_hash


class SecureModelView(ModelView):
    """Base model view with authentication"""

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login', next=request.url))


class SecureAdminIndexView(AdminIndexView):
    """Admin index view with authentication"""

    @expose('/')
    def index(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('.login'))
        return super(SecureAdminIndexView, self).index()

    @expose('/login', methods=['GET', 'POST'])
    def login(self):
        if current_user.is_authenticated:
            return redirect(url_for('.index'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('.index'))

            flash('Invalid username or password', 'error')

        return self.render('admin/login.html')

    @expose('/logout')
    def logout(self):
        logout_user()
        return redirect(url_for('.login'))


class UserAdmin(SecureModelView):
    """User admin view"""
    column_list = ['id', 'username', 'email', 'is_admin', 'created_at']
    column_searchable_list = ['username', 'email']
    column_filters = ['is_admin', 'created_at']
    form_excluded_columns = ['password_hash', 'contents', 'media']

    form_extra_fields = {
        'password': PasswordField('Password')
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password_hash = generate_password_hash(form.password.data)


class ContentTypeAdmin(SecureModelView):
    """Content type admin view"""
    column_list = ['id', 'name', 'slug', 'description', 'created_at']
    column_searchable_list = ['name', 'slug']
    form_columns = ['name', 'slug', 'description', 'schema']


class ContentAdmin(SecureModelView):
    """Content admin view"""
    column_list = ['id', 'title', 'content_type', 'status', 'author', 'created_at', 'updated_at']
    column_searchable_list = ['title', 'slug']
    column_filters = ['status', 'content_type', 'created_at']
    form_columns = ['title', 'slug', 'content_type', 'data', 'status', 'author']

    def on_model_change(self, form, model, is_created):
        from datetime import datetime
        if is_created:
            model.created_at = datetime.utcnow()
        model.updated_at = datetime.utcnow()

        if model.status == 'published' and not model.published_at:
            model.published_at = datetime.utcnow()


class MediaAdmin(SecureModelView):
    """Media admin view"""
    column_list = ['id', 'filename', 'original_filename', 'mime_type', 'file_size', 'uploaded_by', 'created_at']
    column_searchable_list = ['filename', 'original_filename']
    column_filters = ['mime_type', 'created_at']
    form_columns = ['filename', 'original_filename', 'mime_type', 'file_size', 'path', 'alt_text', 'uploaded_by']


class CategoryAdmin(SecureModelView):
    """Category admin view"""
    column_list = ['id', 'name', 'slug', 'parent', 'created_at']
    column_searchable_list = ['name', 'slug']
    form_columns = ['name', 'slug', 'description', 'parent']


class TagAdmin(SecureModelView):
    """Tag admin view"""
    column_list = ['id', 'name', 'slug', 'created_at']
    column_searchable_list = ['name', 'slug']
    form_columns = ['name', 'slug']


def init_admin(app):
    """Initialize Flask-Admin"""
    admin = Admin(
        app,
        name='CMS Admin',
        template_mode='bootstrap4',
        index_view=SecureAdminIndexView(url='/admin')
    )

    # Add model views
    admin.add_view(UserAdmin(User, db.session, name='Users'))
    admin.add_view(ContentTypeAdmin(ContentType, db.session, name='Content Types'))
    admin.add_view(ContentAdmin(Content, db.session, name='Content'))
    admin.add_view(MediaAdmin(Media, db.session, name='Media'))
    admin.add_view(CategoryAdmin(Category, db.session, name='Categories'))
    admin.add_view(TagAdmin(Tag, db.session, name='Tags'))

    return admin
