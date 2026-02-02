#!/bin/bash

# Django Blog - Quick Start Script
# This script helps you get started with the blog application

echo "================================"
echo "Django Blog - Quick Start"
echo "================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "⚠️  .env.production not found. Creating from template..."
    cp .env.example .env.production
    echo "✅ Created .env.production"
    echo ""
    echo "🔐 IMPORTANT: Please edit .env.production and update:"
    echo "   - SECRET_KEY (generate using: python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\")"
    echo "   - ALLOWED_HOSTS (your domain)"
    echo "   - DB_PASSWORD (strong password)"
    echo "   - EMAIL credentials (if using email features)"
    echo ""
    read -p "Press Enter after updating .env.production to continue..."
fi

echo "🚀 Starting deployment..."
echo ""

# Build and start services
echo "📦 Building Docker images..."
docker-compose up --build -d

if [ $? -ne 0 ]; then
    echo "❌ Failed to start services. Check the error messages above."
    exit 1
fi

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

echo ""
echo "🎉 Services are running!"
echo ""

# Check if superuser exists
echo "👤 Superuser setup:"
read -p "Do you want to create a superuser now? (y/n): " create_superuser

if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    docker-compose exec web python manage.py createsuperuser
fi

echo ""
echo "================================"
echo "✅ Setup Complete!"
echo "================================"
echo ""
echo "Your blog is now running at:"
echo "  🌐 Website: http://localhost"
echo "  🔧 Admin:   http://localhost/admin"
echo ""
echo "Useful commands:"
echo "  📋 View logs:        docker-compose logs -f"
echo "  🛑 Stop services:    docker-compose down"
echo "  🔄 Restart services: docker-compose restart"
echo "  📊 View status:      docker-compose ps"
echo ""
echo "For more information, see README.md and DEPLOYMENT.md"
echo ""
