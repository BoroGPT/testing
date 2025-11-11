# Content Management System (CMS)

A flexible, full-featured Content Management System built with Flask and SQLAlchemy. This project includes a RESTful API, admin interface, and support for custom content types.

## Features

- **Flexible Content Types**: Define custom content structures with JSON schemas
- **RESTful API**: Complete CRUD operations for all content
- **Admin Interface**: User-friendly web interface for content management
- **User Management**: Authentication and authorization system
- **Media Management**: Upload and organize images and documents
- **Search & Filter**: Powerful search across all content
- **Categories & Tags**: Organize content hierarchically
- **SQLite Database**: Lightweight, serverless database

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python -m cms.app
```

The CMS will be available at:
- **Home**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin
- **API**: http://localhost:5000/api/content

### 3. Default Credentials

- Username: `admin`
- Password: `admin123`

**Important**: Change the default password after first login!

## API Documentation

### Content Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/content` | Get all content (with pagination) |
| GET | `/api/content/<id>` | Get specific content by ID |
| GET | `/api/content/by-slug/<slug>` | Get content by slug |
| POST | `/api/content` | Create new content (auth required) |
| PUT | `/api/content/<id>` | Update content (auth required) |
| DELETE | `/api/content/<id>` | Delete content (auth required) |

### Other Endpoints

- `GET /api/content-types` - List all content types
- `GET /api/categories` - List all categories
- `GET /api/tags` - List all tags
- `GET /api/media` - List all media files
- `POST /api/media/upload` - Upload media (auth required)
- `GET /api/search?q=query` - Search content

### Example API Usage

```bash
# Get all content
curl http://localhost:5000/api/content

# Get specific content by ID
curl http://localhost:5000/api/content/1

# Search content
curl http://localhost:5000/api/search?q=magic

# Filter by content type
curl http://localhost:5000/api/content?type=card&status=published
```

## Content Types

The CMS comes with three predefined content types:

### 1. Page
Static pages with:
- Body (text)
- Meta description
- Meta keywords

### 2. Post
Blog posts with:
- Body (text)
- Excerpt
- Featured image

### 3. Card
Magic the Gathering cards with:
- Type
- Mana cost
- Card text
- Set
- Rarity

You can create additional content types through the admin interface.

## Project Structure

```
.
├── cms/
│   ├── __init__.py         # Package initialization
│   ├── app.py              # Main Flask application
│   ├── models.py           # Database models
│   ├── api.py              # RESTful API endpoints
│   ├── admin.py            # Admin interface
│   ├── config.py           # Configuration settings
│   └── templates/          # HTML templates
│       ├── base.html
│       ├── index.html
│       └── admin/
│           └── login.html
├── codex/
│   ├── codex.py            # Original CLI tool
│   └── cards.json          # Card data (imported into CMS)
├── uploads/                # Media upload directory
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Configuration

Create a `.env` file for custom configuration:

```bash
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///cms.db
```

See `.env.example` for reference.

## Development

### Database Migrations

The database is automatically created on first run. To reset the database:

```bash
rm cms.db
python -m cms.app
```

### Adding Custom Content Types

1. Go to Admin Panel → Content Types
2. Click "Create"
3. Define your schema in JSON format:

```json
{
  "fields": [
    {"name": "field_name", "type": "string", "required": true},
    {"name": "description", "type": "text"}
  ]
}
```

## Original Magic the Gathering Codex

This repository originally contained a CLI tool for Magic the Gathering cards. The original tool is still available:

```bash
python codex/codex.py list
python codex/codex.py search Lotus
```

The card data has been automatically imported into the CMS and can be managed through the admin interface.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
