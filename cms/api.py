"""
RESTful API endpoints for the CMS
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from cms.models import db, Content, ContentType, Media, Category, Tag
from datetime import datetime
from werkzeug.utils import secure_filename
import os

api_bp = Blueprint('api', __name__)


# Content Type endpoints
@api_bp.route('/content-types', methods=['GET'])
def get_content_types():
    """Get all content types"""
    content_types = ContentType.query.all()
    return jsonify([{
        'id': ct.id,
        'name': ct.name,
        'slug': ct.slug,
        'description': ct.description,
        'schema': ct.schema
    } for ct in content_types])


@api_bp.route('/content-types/<int:id>', methods=['GET'])
def get_content_type(id):
    """Get a specific content type"""
    content_type = ContentType.query.get_or_404(id)
    return jsonify({
        'id': content_type.id,
        'name': content_type.name,
        'slug': content_type.slug,
        'description': content_type.description,
        'schema': content_type.schema
    })


@api_bp.route('/content-types', methods=['POST'])
@login_required
def create_content_type():
    """Create a new content type"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json()
    content_type = ContentType(
        name=data['name'],
        slug=data['slug'],
        description=data.get('description'),
        schema=data.get('schema', {})
    )
    db.session.add(content_type)
    db.session.commit()

    return jsonify({
        'id': content_type.id,
        'name': content_type.name,
        'slug': content_type.slug,
        'message': 'Content type created successfully'
    }), 201


# Content endpoints
@api_bp.route('/content', methods=['GET'])
def get_contents():
    """Get all content with filtering and pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    content_type = request.args.get('type')
    status = request.args.get('status', 'published')
    search = request.args.get('search')

    query = Content.query

    if content_type:
        ct = ContentType.query.filter_by(slug=content_type).first()
        if ct:
            query = query.filter_by(content_type_id=ct.id)

    if status:
        query = query.filter_by(status=status)

    if search:
        query = query.filter(Content.title.ilike(f'%{search}%'))

    query = query.order_by(Content.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'items': [{
            'id': item.id,
            'title': item.title,
            'slug': item.slug,
            'content_type': item.content_type.name,
            'data': item.data,
            'status': item.status,
            'author': item.author.username if item.author else None,
            'created_at': item.created_at.isoformat(),
            'updated_at': item.updated_at.isoformat(),
            'published_at': item.published_at.isoformat() if item.published_at else None
        } for item in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@api_bp.route('/content/<int:id>', methods=['GET'])
def get_content(id):
    """Get a specific content item"""
    content = Content.query.get_or_404(id)
    return jsonify({
        'id': content.id,
        'title': content.title,
        'slug': content.slug,
        'content_type': content.content_type.name,
        'content_type_slug': content.content_type.slug,
        'data': content.data,
        'status': content.status,
        'author': content.author.username if content.author else None,
        'created_at': content.created_at.isoformat(),
        'updated_at': content.updated_at.isoformat(),
        'published_at': content.published_at.isoformat() if content.published_at else None
    })


@api_bp.route('/content/by-slug/<slug>', methods=['GET'])
def get_content_by_slug(slug):
    """Get content by slug"""
    content = Content.query.filter_by(slug=slug).first_or_404()
    return jsonify({
        'id': content.id,
        'title': content.title,
        'slug': content.slug,
        'content_type': content.content_type.name,
        'content_type_slug': content.content_type.slug,
        'data': content.data,
        'status': content.status,
        'author': content.author.username if content.author else None,
        'created_at': content.created_at.isoformat(),
        'updated_at': content.updated_at.isoformat(),
        'published_at': content.published_at.isoformat() if content.published_at else None
    })


@api_bp.route('/content', methods=['POST'])
@login_required
def create_content():
    """Create new content"""
    data = request.get_json()

    # Get content type
    content_type = ContentType.query.filter_by(slug=data['content_type']).first()
    if not content_type:
        return jsonify({'error': 'Invalid content type'}), 400

    content = Content(
        title=data['title'],
        slug=data.get('slug', data['title'].lower().replace(' ', '-')),
        content_type_id=content_type.id,
        data=data.get('data', {}),
        status=data.get('status', 'draft'),
        author_id=current_user.id
    )

    if data.get('status') == 'published' and not content.published_at:
        content.published_at = datetime.utcnow()

    db.session.add(content)
    db.session.commit()

    return jsonify({
        'id': content.id,
        'title': content.title,
        'slug': content.slug,
        'message': 'Content created successfully'
    }), 201


@api_bp.route('/content/<int:id>', methods=['PUT'])
@login_required
def update_content(id):
    """Update existing content"""
    content = Content.query.get_or_404(id)

    # Check permission
    if not current_user.is_admin and content.author_id != current_user.id:
        return jsonify({'error': 'Permission denied'}), 403

    data = request.get_json()

    if 'title' in data:
        content.title = data['title']
    if 'slug' in data:
        content.slug = data['slug']
    if 'data' in data:
        content.data = data['data']
    if 'status' in data:
        content.status = data['status']
        if data['status'] == 'published' and not content.published_at:
            content.published_at = datetime.utcnow()

    content.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        'id': content.id,
        'title': content.title,
        'message': 'Content updated successfully'
    })


@api_bp.route('/content/<int:id>', methods=['DELETE'])
@login_required
def delete_content(id):
    """Delete content"""
    content = Content.query.get_or_404(id)

    # Check permission
    if not current_user.is_admin and content.author_id != current_user.id:
        return jsonify({'error': 'Permission denied'}), 403

    db.session.delete(content)
    db.session.commit()

    return jsonify({'message': 'Content deleted successfully'})


# Media endpoints
@api_bp.route('/media', methods=['GET'])
def get_media():
    """Get all media files"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    pagination = Media.query.order_by(Media.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'items': [{
            'id': item.id,
            'filename': item.filename,
            'original_filename': item.original_filename,
            'mime_type': item.mime_type,
            'file_size': item.file_size,
            'path': item.path,
            'alt_text': item.alt_text,
            'uploaded_by': item.uploaded_by.username if item.uploaded_by else None,
            'created_at': item.created_at.isoformat()
        } for item in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@api_bp.route('/media/upload', methods=['POST'])
@login_required
def upload_media():
    """Upload a media file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file:
        filename = secure_filename(file.filename)
        # Add timestamp to avoid conflicts
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"

        from flask import current_app
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Get file size
        file_size = os.path.getsize(filepath)

        media = Media(
            filename=filename,
            original_filename=file.filename,
            mime_type=file.content_type,
            file_size=file_size,
            path=filepath,
            alt_text=request.form.get('alt_text'),
            uploaded_by_id=current_user.id
        )
        db.session.add(media)
        db.session.commit()

        return jsonify({
            'id': media.id,
            'filename': media.filename,
            'path': media.path,
            'message': 'File uploaded successfully'
        }), 201


# Category endpoints
@api_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    categories = Category.query.all()
    return jsonify([{
        'id': cat.id,
        'name': cat.name,
        'slug': cat.slug,
        'description': cat.description,
        'parent_id': cat.parent_id
    } for cat in categories])


@api_bp.route('/categories', methods=['POST'])
@login_required
def create_category():
    """Create a new category"""
    data = request.get_json()
    category = Category(
        name=data['name'],
        slug=data.get('slug', data['name'].lower().replace(' ', '-')),
        description=data.get('description'),
        parent_id=data.get('parent_id')
    )
    db.session.add(category)
    db.session.commit()

    return jsonify({
        'id': category.id,
        'name': category.name,
        'slug': category.slug,
        'message': 'Category created successfully'
    }), 201


# Tag endpoints
@api_bp.route('/tags', methods=['GET'])
def get_tags():
    """Get all tags"""
    tags = Tag.query.all()
    return jsonify([{
        'id': tag.id,
        'name': tag.name,
        'slug': tag.slug
    } for tag in tags])


@api_bp.route('/tags', methods=['POST'])
@login_required
def create_tag():
    """Create a new tag"""
    data = request.get_json()
    tag = Tag(
        name=data['name'],
        slug=data.get('slug', data['name'].lower().replace(' ', '-'))
    )
    db.session.add(tag)
    db.session.commit()

    return jsonify({
        'id': tag.id,
        'name': tag.name,
        'slug': tag.slug,
        'message': 'Tag created successfully'
    }), 201


# Search endpoint
@api_bp.route('/search', methods=['GET'])
def search():
    """Search across all content"""
    query = request.args.get('q', '')
    content_type = request.args.get('type')

    if not query:
        return jsonify({'error': 'Search query required'}), 400

    search_query = Content.query.filter(
        Content.title.ilike(f'%{query}%') |
        Content.data.cast(db.String).ilike(f'%{query}%')
    )

    if content_type:
        ct = ContentType.query.filter_by(slug=content_type).first()
        if ct:
            search_query = search_query.filter_by(content_type_id=ct.id)

    results = search_query.filter_by(status='published').all()

    return jsonify({
        'query': query,
        'count': len(results),
        'results': [{
            'id': item.id,
            'title': item.title,
            'slug': item.slug,
            'content_type': item.content_type.name,
            'excerpt': str(item.data)[:200] if item.data else ''
        } for item in results]
    })
