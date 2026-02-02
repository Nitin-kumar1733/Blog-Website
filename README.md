# Django Blog Website - Complete Guide

> **Your all-in-one guide to understanding, setting up, and running the blog website**

---

## 📖 Table of Contents

1. [About the Website](#about-the-website)
2. [Key Features](#key-features)
3. [Technology Stack](#technology-stack)
4. [Quick Start (3 Minutes)](#quick-start-3-minutes)
5. [Detailed Setup Instructions](#detailed-setup-instructions)
6. [Using AI Summarization](#using-ai-summarization)
7. [Common Commands](#common-commands)
8. [Troubleshooting](#troubleshooting)
9. [Project Structure](#project-structure)
10. [Development Guide](#development-guide)

---

## About the Website

A modern, production-ready blogging platform built with Django that provides a complete solution where anyone can share information and post articles about any topic. The website includes rich text editing, AI-powered summarization using OpenAI GPT-3.5, user profiles with image uploads, and a fully responsive Bootstrap UI.

### What Makes This Special?

- **Production-Ready**: Fully Dockerized with PostgreSQL, Nginx, and Gunicorn
- **AI-Powered**: Automatic blog post summarization using LangChain and OpenAI
- **Modern Stack**: Python 3.12, Django 6.0.1, Rich text editor (CKEditor)
- **Secure**: Environment-based configuration, HTTPS support, security headers
- **Easy Deployment**: One-command deployment with Docker Compose

---

## Key Features

✅ **AI-Powered Blog Summarization** (LangChain 1.2.7 + OpenAI GPT-3.5)
✅ **Rich Text Editor** (CKEditor with full formatting toolbar)
✅ **User Registration & Authentication**
✅ **Complete CRUD Operations** for blog posts
✅ **User Profiles** with image uploads
✅ **Smart Caching** (AI summaries cached for 24 hours)
✅ **Pagination** for blog listings
✅ **Password Reset** functionality
✅ **Responsive Design** with Bootstrap 4
✅ **Full Docker Containerization**
✅ **PostgreSQL 14** database
✅ **Nginx Reverse Proxy** with gzip compression
✅ **Static File Serving** with WhiteNoise

---

## Technology Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.12 | Programming language |
| **Django** | 6.0.1 | Web framework |
| **PostgreSQL** | 14 | Production database |
| **LangChain** | 1.2.7 | AI framework (LCEL API) |
| **OpenAI API** | GPT-3.5 | AI summarization model |
| **CKEditor** | 6.7.3 | Rich text editor |
| **Gunicorn** | 24.1.1 | Production WSGI server |
| **Nginx** | Latest | Web server & reverse proxy |
| **Docker** | Latest | Containerization |
| **Bootstrap** | 4 | Frontend framework |

---

## Quick Start (3 Minutes)

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key (get from https://platform.openai.com/api-keys)

### Setup Steps

```bash
# 1. Navigate to project directory
cd Blog-Website

# 2. Copy environment file
cp .env.example .env.production

# 3. Edit .env.production and add:
#    - Random SECRET_KEY (generate using command below)
#    - Your OpenAI API key
#    - Strong DB_PASSWORD
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Example .env.production:**
```env
DEBUG=False
SECRET_KEY=your-generated-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
USE_POSTGRES=True
DB_NAME=blogdb
DB_USER=bloguser
DB_PASSWORD=your-strong-password-here
DB_HOST=db
DB_PORT=5432
OPENAI_API_KEY=sk-your-openai-api-key-here
```

```bash
# 4. Start all services
docker-compose up -d

# 5. Create admin user
docker-compose exec web python manage.py createsuperuser

# 6. Access the website
#    Website: http://localhost
#    Admin:   http://localhost/admin
```

**That's it!** 🎉 Your production-ready blog is now running.

---

## Detailed Setup Instructions

### Option 1: Docker Production Setup (Recommended)

#### Step 1: Prepare Environment File

```bash
# Copy the example environment file
cp .env.example .env.production

# Generate a secure SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Edit .env.production with your favorite editor
nano .env.production
```

#### Step 2: Configure Environment Variables

Required settings in `.env.production`:

```env
# Security
DEBUG=False
SECRET_KEY=your-generated-secret-key-from-step-1

# Hosts
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database (PostgreSQL)
USE_POSTGRES=True
DB_NAME=blogdb
DB_USER=bloguser
DB_PASSWORD=secure-database-password-here
DB_HOST=db
DB_PORT=5432

# AI Summarization
OPENAI_API_KEY=sk-your-openai-api-key-here

# Email (Optional - for password reset)
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-specific-password
```

#### Step 3: Build and Start Services

```bash
# Build and start all containers
docker-compose up --build -d

# Check if all services are running
docker-compose ps

# View logs
docker-compose logs -f web
```

#### Step 4: Initialize Database and Create Admin

```bash
# Create database tables (migrations run automatically, but you can check)
docker-compose exec web python manage.py migrate

# Create a superuser account
docker-compose exec web python manage.py createsuperuser
# Follow the prompts to enter username, email, and password

# Collect static files (done automatically in entrypoint.sh)
docker-compose exec web python manage.py collectstatic --noinput
```

#### Step 5: Access Your Website

- **Main Website**: http://localhost
- **Admin Panel**: http://localhost/admin
- **Login with your superuser credentials**

### Option 2: Local Development (Without Docker)

#### Step 1: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

#### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Setup Environment

```bash
# Copy environment file
cp .env.example .env

# Edit .env file with your settings
nano .env
```

#### Step 4: Run Database Migrations

```bash
python manage.py migrate
```

#### Step 5: Create Superuser

```bash
python manage.py createsuperuser
```

#### Step 6: Run Development Server

```bash
python manage.py runserver
```

Access at: http://localhost:8000

---

## Using AI Summarization

### Setup AI Feature

#### 1. Get OpenAI API Key

1. Visit [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

#### 2. Add to Environment

Edit `.env.production`:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

#### 3. Restart Services

```bash
docker-compose down
docker-compose up -d
```

### How to Generate AI Summaries

#### Step 1: Login to Your Account
- Navigate to http://localhost/
- Click "Login" or "Register"
- Create/login to your account

#### Step 2: View a Blog Post
- Click on any blog post title from the home page
- Or create a new post by clicking "New Post"

#### Step 3: Generate Summary
- Scroll to the bottom of the blog post
- Click **"Generate AI Summary" 🪄** button
- Wait 3-5 seconds for OpenAI to process
- Summary appears in a blue alert box with robot icon 🤖

#### Step 4: Regenerate (Optional)
- The button changes to **"Regenerate Summary"**
- Click to create a new summary if the post was updated

### AI Summary Features

✅ **Smart & Concise**: Generates 2-3 sentence summaries
✅ **Fast**: Takes only 3-5 seconds
✅ **Cached**: Summaries stored for 24 hours (saves API costs)
✅ **Cost-Effective**: ~$0.0003 per summary
✅ **Timestamped**: Shows when summary was generated
✅ **Login Required**: Only authenticated users can generate

### Example

**Original Post (500 words):**
```
Django is a high-level Python web framework that encourages rapid 
development and clean, pragmatic design. Built by experienced developers, 
it takes care of much of the hassle of web development, so you can 
focus on writing your app without needing to reinvent the wheel...
[continues for 500 words]
```

**AI Summary:**
```
This blog post introduces Django as a powerful Python web framework 
that simplifies web development by handling common tasks automatically. 
It emphasizes Django's focus on rapid development and clean design 
principles for building modern web applications.
```

### Verify AI Setup

```bash
# Check LangChain is available
docker-compose exec web python manage.py shell -c "from blog.views import LANGCHAIN_AVAILABLE; print('LANGCHAIN_AVAILABLE:', LANGCHAIN_AVAILABLE)"

# Expected: LANGCHAIN_AVAILABLE: True

# Check API key is configured
docker-compose exec web python manage.py shell -c "import os; print('API Key configured:', 'Yes' if os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY') != 'your-openai-api-key-here' else 'No')"

# Expected: API Key configured: Yes
```

---

## Common Commands

### Docker Management

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build -d

# View logs
docker-compose logs -f web

# Check service status
docker-compose ps

# Execute commands in web container
docker-compose exec web python manage.py [command]
```

### Django Management

```bash
# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run migrations
docker-compose exec web python manage.py migrate

# Create new migrations
docker-compose exec web python manage.py makemigrations

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Open Django shell
docker-compose exec web python manage.py shell

# Run tests
docker-compose exec web python manage.py test

# Check for issues
docker-compose exec web python manage.py check
```

### Database Management

```bash
# Access PostgreSQL shell
docker-compose exec db psql -U bloguser -d blogdb

# Backup database
docker-compose exec db pg_dump -U bloguser blogdb > backup.sql

# Restore database
docker-compose exec -T db psql -U bloguser blogdb < backup.sql

# View database tables
docker-compose exec db psql -U bloguser -d blogdb -c "\dt"
```

### Container Management

```bash
# Enter container bash shell
docker-compose exec web bash

# View container resource usage
docker stats

# Remove all stopped containers
docker-compose down -v

# View container logs (specific service)
docker-compose logs -f db
docker-compose logs -f nginx
docker-compose logs -f web
```

---

## Troubleshooting

### AI Summarization Issues

#### Problem: No "Generate AI Summary" button visible
**Solution**: You need to be logged in! Click "Login" in the top right corner.

#### Problem: "AI summarization is not configured" error
**Solution**: 
1. Add `OPENAI_API_KEY` to `.env.production`
2. Restart services: `docker-compose restart web`

#### Problem: "AI summarization is not available" error
**Solution**: 
1. Rebuild container with LangChain packages:
   ```bash
   docker-compose down
   docker-compose up -d --build
   ```

#### Problem: OpenAI API error
**Solution**:
1. Verify your API key at https://platform.openai.com/api-keys
2. Check your account has credits at https://platform.openai.com/account/usage
3. Ensure API key is correctly set in `.env.production` (starts with `sk-`)

### Docker Issues

#### Problem: "Port already in use" error
**Solution**:
```bash
# Find process using port 80
sudo lsof -i :80  # macOS/Linux
netstat -ano | findstr :80  # Windows

# Kill the process or change port in docker-compose.yml
```

#### Problem: Container fails to start
**Solution**:
```bash
# View detailed logs
docker-compose logs web

# Check for environment variable issues
docker-compose exec web env | grep -E "(SECRET_KEY|DB_|OPENAI)"

# Rebuild from scratch
docker-compose down -v
docker-compose up --build -d
```

#### Problem: Database connection error
**Solution**:
```bash
# Check if database is running
docker-compose ps

# Restart database
docker-compose restart db

# Check database logs
docker-compose logs db
```

### Static Files Issues

#### Problem: CSS/JS not loading
**Solution**:
```bash
# Collect static files again
docker-compose exec web python manage.py collectstatic --noinput

# Restart nginx
docker-compose restart nginx
```

### Permission Issues

#### Problem: Permission denied errors
**Solution**:
```bash
# Fix ownership of media files
sudo chown -R $USER:$USER media/

# Fix ownership of database file (if using SQLite)
sudo chown -R $USER:$USER db.sqlite3
```

---

## Project Structure

```
Blog-Website/
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Docker image definition
├── docker-compose.yml            # Production Docker setup
├── docker-compose.dev.yml        # Development Docker setup
├── entrypoint.sh                  # Container startup script
├── .env.production               # Production environment variables
├── .env.example                   # Environment template
│
├── django_project/                # Main project configuration
│   ├── __init__.py
│   ├── settings.py               # Django settings (updated for production)
│   ├── urls.py                   # Root URL configuration
│   ├── wsgi.py                   # WSGI configuration
│   └── asgi.py                   # ASGI configuration
│
├── blog/                          # Blog application
│   ├── models.py                 # Post model with AI summary fields
│   ├── views.py                  # Blog views + AI summarization
│   ├── urls.py                   # URL routing
│   ├── admin.py                  # Admin configuration
│   ├── forms.py                  # Forms (if any)
│   ├── templates/blog/           # Blog templates
│   │   ├── base.html            # Base template
│   │   ├── home.html            # Home page
│   │   ├── post_detail.html     # Post detail with AI summary
│   │   ├── post_form.html       # Create/edit post
│   │   ├── post_confirm_delete.html
│   │   ├── user_posts.html      # User's posts
│   │   └── about.html           # About page
│   ├── static/blog/              # Blog static files
│   │   └── main.css             # Custom CSS
│   └── migrations/               # Database migrations
│
├── users/                         # User management application
│   ├── models.py                 # Profile model
│   ├── views.py                  # User views (register, login, profile)
│   ├── forms.py                  # User forms
│   ├── signals.py                # Auto-create profiles
│   ├── admin.py                  # Admin configuration
│   ├── templates/users/          # User templates
│   │   ├── register.html
│   │   ├── login.html
│   │   ├── logout.html
│   │   ├── profile.html
│   │   ├── password_reset.html
│   │   ├── password_reset_done.html
│   │   ├── password_reset_confirm.html
│   │   └── password_reset_complete.html
│   └── migrations/               # Database migrations
│
├── nginx/                         # Nginx configuration
│   └── nginx.conf                # Reverse proxy config
│
├── media/                         # User uploaded files
│   └── profile_pics/             # User profile images
│
├── staticfiles/                   # Collected static files (production)
├── logs/                          # Application logs
└── db.sqlite3                     # SQLite database (development only)
```

### Key Files Explained

- **manage.py**: Django's command-line utility for administrative tasks
- **requirements.txt**: All Python dependencies including Django, LangChain, OpenAI
- **Dockerfile**: Defines how to build the Docker image
- **docker-compose.yml**: Orchestrates PostgreSQL, Django, and Nginx containers
- **entrypoint.sh**: Runs migrations and starts Gunicorn automatically
- **settings.py**: Main Django configuration (security, database, static files)
- **models.py** (blog): Post model with `summary` and `summary_generated_at` fields
- **views.py** (blog): Contains `summarize_post` view with LangChain integration
- **nginx.conf**: Reverse proxy configuration for serving the application

---

## Development Guide

### Setting Up Development Environment

#### Using Docker (Recommended)

```bash
# Start development server with hot-reload
docker-compose -f docker-compose.dev.yml up

# The app will be available at http://localhost:8000
# Code changes will auto-reload
```

#### Local Python Environment

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment
cp .env.example .env
# Edit .env with your settings

# 4. Run migrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Run development server
python manage.py runserver
```

### Development Workflow

#### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

#### 2. Make Changes

Edit relevant files in `blog/` or `users/` apps.

#### 3. Test Changes

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test blog
python manage.py test users
```

#### 4. Run Migrations (if models changed)

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. Check for Issues

```bash
python manage.py check
```

### Adding New Features

#### Create a New Django App

```bash
docker-compose exec web python manage.py startapp newapp
```

#### Add to INSTALLED_APPS

Edit `django_project/settings.py`:

```python
INSTALLED_APPS = [
    # ...existing apps...
    'newapp.apps.NewappConfig',
]
```

#### Create Models

Edit `newapp/models.py` and create migrations:

```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Testing

```bash
# Run all tests
docker-compose exec web python manage.py test

# Run specific app tests
docker-compose exec web python manage.py test blog

# Run specific test case
docker-compose exec web python manage.py test blog.tests.PostModelTest

# Run with verbosity
docker-compose exec web python manage.py test --verbosity=2

# Run with coverage (install coverage first)
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report
```

### Best Practices

1. **Environment Variables**: Never hardcode secrets; use `.env` files
2. **Migrations**: Always create migrations for model changes
3. **Static Files**: Run `collectstatic` before deployment
4. **Security**: Keep `DEBUG=False` in production
5. **Database**: Use PostgreSQL in production, SQLite is fine for development
6. **Version Control**: Don't commit `.env`, `db.sqlite3`, or `media/` files
7. **Documentation**: Update this guide when adding major features

---

## Security Checklist

Before deploying to production:

- [ ] Set `DEBUG=False` in `.env.production`
- [ ] Generate strong `SECRET_KEY`
- [ ] Set strong database password
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Add OpenAI API key
- [ ] Enable HTTPS/SSL (use Let's Encrypt)
- [ ] Set up regular database backups
- [ ] Configure email settings for password reset
- [ ] Review and enable security headers in Nginx
- [ ] Set up monitoring and logging
- [ ] Regularly update dependencies

---

## Support & Resources

### Official Documentation
- **Django**: https://docs.djangoproject.com/
- **LangChain**: https://python.langchain.com/docs/
- **OpenAI**: https://platform.openai.com/docs/
- **Docker**: https://docs.docker.com/
- **PostgreSQL**: https://www.postgresql.org/docs/

### Getting Help
- Review this guide thoroughly
- Check the troubleshooting section
- View container logs: `docker-compose logs -f`
- Search Django/LangChain documentation
- Check OpenAI API status: https://status.openai.com/

### Useful Commands Reference

```bash
# Quick restart
docker-compose restart web

# Full rebuild
docker-compose down && docker-compose up -d --build

# View all logs
docker-compose logs -f

# Clean everything
docker-compose down -v && docker system prune -a

# Backup database
docker-compose exec db pg_dump -U bloguser blogdb > backup_$(date +%Y%m%d).sql
```

---

## Summary

You now have a fully functional, production-ready Django blog website with:
- ✅ AI-powered summarization
- ✅ Rich text editing
- ✅ User authentication and profiles
- ✅ Complete Docker containerization
- ✅ PostgreSQL database
- ✅ Nginx reverse proxy
- ✅ Security best practices

**To start the website:**
```bash
docker-compose up -d
```

**To access:**
- Website: http://localhost
- Admin: http://localhost/admin

**That's all you need!** 🚀

---

*Last Updated: February 2, 2026*
