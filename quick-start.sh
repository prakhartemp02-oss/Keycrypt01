#!/bin/bash

# KeyCrypt Quick Start Script
# Sets up the development environment and starts the application

set -e

echo "🔐 KeyCrypt - Educational Cryptography Game"
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Set up environment variables
if [ ! -f .env ]; then
    echo "📋 Creating environment file from template..."
    cp .env.example .env
    echo "✅ .env file created from .env.example"
    echo "💡 You can edit .env to customize your configuration"
else
    echo "✅ Environment file already exists"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p keys database logs

# Generate RSA keys if they don't exist
if [ ! -f keys/private.pem ]; then
    echo "🔑 Generating RSA keys..."
    openssl genrsa -out keys/private.pem 2048
    openssl rsa -in keys/private.pem -pubout -out keys/public.pem
    echo "✅ RSA keys generated"
else
    echo "✅ RSA keys already exist"
fi

# Stop any existing containers
echo "🛑 Stopping any existing containers..."
docker-compose down

# Build and start the containers
echo "🐳 Building and starting Docker containers..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo "🔍 Checking service health..."

# Check backend health
if curl -f http://localhost:5000/health &> /dev/null; then
    echo "✅ Backend API is healthy"
else
    echo "⚠️ Backend API is not responding yet (this is normal on first start)"
fi

# Check frontend is accessible
if curl -f http://localhost:3000 &> /dev/null; then
    echo "✅ Frontend is accessible"
else
    echo "⚠️ Frontend is starting up (this can take a minute on first start)"
fi

# Show service status
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "🎮 KeyCrypt is now running!"
echo ""
echo "📱 Frontend Application: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5000"
echo "💾 Database: localhost:5432"
echo "📦 Redis: localhost:6379"
echo ""
echo "🔍 Useful Commands:"
echo "  View logs:           docker-compose logs -f"
echo "  View backend logs:   docker-compose logs -f backend"
echo "  View frontend logs:  docker-compose logs -f frontend"
echo "  Stop services:       docker-compose down"
echo "  Restart services:    docker-compose restart"
echo ""
echo "📚 Development Guide: DEVELOPMENT.md"
echo "🐛 Report Issues:      https://github.com/your-repo/issues"
echo ""
echo "🎯 Quick Test:"
echo "  1. Open http://localhost:3000 in your browser"
echo "  2. Click 'Start Playing' → Select a level → Start a game"
echo "  3. Try guessing the encrypted word!"
echo ""
echo "✨ Happy Cryptography Learning! ✨"