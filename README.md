# 📝 Modern Note-Taking Web Application

A full-featured, secure note-taking web application built with Flask, featuring user authentication, rich note management, search functionality, and a modern responsive UI.

## ✨ Features

### 🔐 Security & Authentication
- **Secure User Authentication** with Flask-Login
- **CSRF Protection** to prevent cross-site request forgery
- **Password Hashing** using Werkzeug's secure hash functions
- **Input Validation** with WTForms
- **Environment-based Configuration** for secure secret management

### 📝 Note Management
- **Rich Note Creation** with titles, content, categories, and tags
- **Advanced Search** with full-text search across titles and content
- **Category Organization** (General, Work, Personal, Ideas, Learning, Projects)
- **Tag System** for flexible note organization
- **Favorites** to mark important notes
- **CRUD Operations** - Create, Read, Update, Delete notes
- **Responsive Design** that works on desktop and mobile

### 🎨 Modern UI/UX
- **Bootstrap 4** for responsive design
- **Card-based Layout** for clean note presentation
- **Modal Forms** for seamless note creation
- **Real-time Search** and filtering
- **Statistics Dashboard** showing note counts and favorites
- **Professional Styling** with hover effects and smooth transitions

### 🚀 Technical Features
- **RESTful API** endpoints for future mobile app integration
- **Database Migrations** support
- **Error Handling** with proper logging
- **Form Validation** with user-friendly error messages
- **AJAX Operations** for smooth user experience

## 🛠️ Tech Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 4
- **Database**: SQLite (easily configurable for PostgreSQL)
- **Security**: CSRF protection, password hashing, input validation
- **Deployment**: Ready for Docker containerization

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Note-Storing-Flask-Web-App
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create a .env file in the root directory
   echo "SECRET_KEY=your-super-secret-key-here" > .env
   echo "DATABASE_URL=sqlite:///database.db" >> .env
   echo "FLASK_ENV=development" >> .env
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
Note-Storing-Flask-Web-App/
├── main.py                 # Application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── website/
│   ├── __init__.py       # Flask app factory
│   ├── models.py         # Database models
│   ├── views.py          # Route handlers
│   ├── auth.py           # Authentication routes
│   ├── forms.py          # WTForms definitions
│   ├── static/
│   │   └── index.js      # JavaScript functionality
│   └── templates/
│       ├── base.html     # Base template
│       ├── home.html     # Main notes page
│       ├── login.html    # Login page
│       ├── sign_up.html  # Registration page
│       ├── edit_note.html # Note editing
│       └── note_detail.html # Note viewing
└── instance/
    └── database.db       # SQLite database
```

## 🔧 Configuration

The application uses environment variables for configuration. Create a `.env` file with:

```env
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///database.db
FLASK_ENV=development
FLASK_DEBUG=True
```

## 🎯 API Endpoints

### Authentication
- `GET /login` - Login page
- `POST /login` - User login
- `GET /signup` - Registration page
- `POST /signup` - User registration
- `GET /logout` - User logout

### Notes
- `GET /` - Main notes page with search/filter
- `POST /` - Create new note
- `GET /note/<id>` - View specific note
- `GET /note/<id>/edit` - Edit note form
- `POST /note/<id>/edit` - Update note
- `POST /delete-note` - Delete note (AJAX)
- `POST /toggle-favorite/<id>` - Toggle favorite status
- `GET /api/notes` - Get all notes as JSON

## 🔒 Security Features

- **CSRF Protection**: All forms are protected against CSRF attacks
- **Password Security**: Passwords are hashed using PBKDF2 with SHA-256
- **Input Validation**: All user inputs are validated and sanitized
- **SQL Injection Prevention**: Using SQLAlchemy ORM prevents SQL injection
- **XSS Protection**: Template auto-escaping prevents XSS attacks

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "main.py"]
```

### Environment Variables for Production
```env
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:password@localhost/notes_db
FLASK_ENV=production
FLASK_DEBUG=False
```

## 🧪 Testing

Run the application and test the following features:
1. User registration and login
2. Creating, editing, and deleting notes
3. Search and filtering functionality
4. Favorites system
5. Responsive design on different screen sizes

## 🎨 Customization

### Adding New Categories
Edit `website/forms.py` and add new options to the category choices.

### Styling
Modify the CSS in the template files or create separate CSS files in the `static` directory.

### Database
The application is configured for SQLite by default but can easily be switched to PostgreSQL or MySQL by changing the `DATABASE_URL` in the configuration.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🎯 Future Enhancements

- [ ] Rich text editor integration
- [ ] File attachment support
- [ ] Real-time collaboration
- [ ] Mobile app development
- [ ] Advanced search with filters
- [ ] Note sharing capabilities
- [ ] Export to PDF/Markdown
- [ ] Dark mode theme
- [ ] API rate limiting
- [ ] User profile management

---

**Built with ❤️ using Flask and modern web technologies**
