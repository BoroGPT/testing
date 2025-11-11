"""
Main Flask application for the CMS
"""
import os
from flask import Flask, render_template, jsonify
from flask_login import LoginManager
from cms.models import db, User
from cms.config import config
from cms.api import api_bp
from cms.admin import init_admin


def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')

    # Initialize admin interface
    init_admin(app)

    # Create database tables
    with app.app_context():
        db.create_all()
        initialize_default_data()

    # Root route
    @app.route('/')
    def index():
        return render_template('index.html')

    # Health check
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'version': '1.0.0'})

    return app


def initialize_default_data():
    """Initialize default content types and admin user"""
    from cms.models import ContentType, User
    from datetime import datetime
    import json

    # Create default admin user if none exists
    if User.query.count() == 0:
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)

    # Create default content types if none exist
    if ContentType.query.count() == 0:
        # Page content type
        page_type = ContentType(
            name='Page',
            slug='page',
            description='Static pages',
            schema={
                'fields': [
                    {'name': 'body', 'type': 'text', 'required': True},
                    {'name': 'meta_description', 'type': 'string'},
                    {'name': 'meta_keywords', 'type': 'string'}
                ]
            }
        )

        # Blog post content type
        post_type = ContentType(
            name='Post',
            slug='post',
            description='Blog posts',
            schema={
                'fields': [
                    {'name': 'body', 'type': 'text', 'required': True},
                    {'name': 'excerpt', 'type': 'text'},
                    {'name': 'featured_image', 'type': 'string'}
                ]
            }
        )

        # Card content type (for Magic the Gathering cards)
        card_type = ContentType(
            name='Card',
            slug='card',
            description='Magic the Gathering cards',
            schema={
                'fields': [
                    {'name': 'type', 'type': 'string', 'required': True},
                    {'name': 'mana_cost', 'type': 'string', 'required': True},
                    {'name': 'text', 'type': 'text', 'required': True},
                    {'name': 'set', 'type': 'string'},
                    {'name': 'rarity', 'type': 'string'}
                ]
            }
        )

        db.session.add(page_type)
        db.session.add(post_type)
        db.session.add(card_type)

    db.session.commit()

    # Import existing card data
    import_card_data()


def import_card_data():
    """Import existing card data from codex/cards.json"""
    from cms.models import Content, ContentType
    import json
    from pathlib import Path
    from datetime import datetime

    # Check if cards have already been imported
    card_type = ContentType.query.filter_by(slug='card').first()
    if not card_type:
        return

    if Content.query.filter_by(content_type_id=card_type.id).count() > 0:
        return  # Already imported

    cards_file = Path(__file__).parent.parent / 'codex' / 'cards.json'
    if not cards_file.exists():
        return

    try:
        with open(cards_file, 'r') as f:
            cards = json.load(f)

        for card in cards:
            content = Content(
                title=card['name'],
                slug=card['name'].lower().replace(' ', '-'),
                content_type_id=card_type.id,
                data={
                    'type': card['type'],
                    'mana_cost': card['mana_cost'],
                    'text': card['text'],
                    'set': card['set'],
                    'rarity': card['rarity']
                },
                status='published',
                published_at=datetime.utcnow()
            )
            db.session.add(content)

        db.session.commit()
        print(f"Imported {len(cards)} cards into CMS")
    except Exception as e:
        print(f"Error importing cards: {e}")


if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    app.run(debug=True, host='0.0.0.0', port=5000)
