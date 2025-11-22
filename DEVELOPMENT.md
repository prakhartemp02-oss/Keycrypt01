# KeyCrypt Development Setup

This guide will help you set up a complete development environment for the KeyCrypt educational cryptography game.

## Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose
- [Git](https://git-scm.com/)
- [Node.js](https://nodejs.org/) 18+ (optional, for local frontend development)
- [Python](https://www.python.org/) 3.10+ (optional, for local backend development)

## Quick Start (Recommended)

The easiest way to get started is with Docker Compose:

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Keycrypt01
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration if needed
   ```

3. **Start the development environment**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Database: localhost:5432
   - Redis: localhost:6379

5. **Check the services are running**
   ```bash
   docker-compose ps
   ```

6. **View logs**
   ```bash
   docker-compose logs -f
   docker-compose logs -f frontend  # Frontend only
   docker-compose logs -f backend   # Backend only
   docker-compose logs -f postgres  # Database only
   ```

## Manual Development Setup

If you prefer to develop without Docker, here's how to set up each component individually.

### Backend Setup

1. **Create virtual environment**
   ```bash
   cd backend
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file in the backend directory
   DATABASE_URL=sqlite:///keycrypt.db
   SECRET_KEY=your-secret-key-here
   FLASK_ENV=development
   CORS_ORIGINS=http://localhost:3000
   ```

4. **Initialize the database**
   ```bash
   # For SQLite (default)
   flask db init
   flask db migrate
   flask db upgrade

   # Or run the init script manually if using PostgreSQL
   psql -d keycrypt -f database/init.sql
   ```

5. **Generate RSA keys**
   ```bash
   mkdir keys
   openssl genrsa -out keys/private.pem 2048
   openssl rsa -in keys/private.pem -pubout -out keys/public.pem
   ```

6. **Run the backend server**
   ```bash
   cd backend
   python run.py
   ```

The backend will be available at http://localhost:5000

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend  # or the root directory if package.json is there
   npm install
   ```

2. **Set up environment variables**
   ```bash
   # Create .env.local file
   NEXT_PUBLIC_API_URL=http://localhost:5000/api
   NEXT_PUBLIC_ENV=development
   ```

3. **Run the frontend server**
   ```bash
   npm run dev
   ```

The frontend will be available at http://localhost:3000

## Development Workflow

### Making Changes

- **Frontend changes**: The Next.js development server will automatically reload
- **Backend changes**: The Flask development server will automatically reload
- **Database changes**: Run migration scripts or update the init.sql file

### Database Management

#### Adding New Words to Dictionary

```sql
INSERT INTO word_dictionary (word, length, category, difficulty_score)
VALUES ('NEWWORD', 7, 'tech', 2);
```

#### Resetting Database

```bash
# Docker
docker-compose down -v
docker-compose up -d

# Manual development
rm keycrypt.db  # For SQLite
# Then restart the backend
```

#### Database Schema Changes

1. Update `database/init.sql`
2. Add migration files if using Flask-Migrate
3. Test changes

### Testing

#### Backend Tests

```bash
cd backend
python -m pytest tests/
```

#### Frontend Tests

```bash
cd frontend
npm test
```

#### Manual Testing Checklist

1. **Backend API**
   - [ ] Health check: `GET /health`
   - [ ] New game: `POST /api/new-game`
   - [ ] Submit guess: `POST /api/guess`
   - [ ] Get hints: `GET /api/hints`
   - [ ] Get game status: `GET /api/game/{id}`

2. **Frontend Navigation**
   - [ ] Landing page loads
   - [ ] Level selection works
   - [ ] Game starts when level selected
   - [ ] Virtual keyboard functions
   - [ ] Physical keyboard input works
   - [ ] Hints display correctly
   - [ ] Game over screens show

3. **Game Flow**
   - [ ] Complete game from start to finish
   - [ ] Test all 9 cipher levels
   - [ ] Verify no plaintext secrets in API responses
   - [ ] Check responsive design on mobile

### API Documentation

The API documentation is automatically generated and available at:

- Development: http://localhost:5000/docs
- Production: https://your-domain.com/docs

### Common Issues

#### Backend Won't Start

```bash
# Check for missing imports
python -c "from backend.app import create_app"

# Check configuration
python -c "from backend.app.config import Config; print(Config.DATABASE_URL)"
```

#### Frontend Can't Connect to Backend

1. Verify backend is running: `curl http://localhost:5000/health`
2. Check CORS configuration in `.env`
3. Verify `NEXT_PUBLIC_API_URL` in frontend

#### Database Issues

```bash
# Docker
docker-compose exec postgres psql -U keycrypt -d keycrypt -c "SELECT 1;"

# Manual
psql postgresql://keycrypt:password@localhost:5432/keycrypt -c "SELECT 1;"
```

## Production Deployment

### Environment Variables

For production, update your `.env` file with:

```bash
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@prod-host:5432/keycrypt
SECRET_KEY=super-secure-production-key
CORS_ORIGINS=https://yourdomain.com
MASTER_KEY=production-encryption-key
```

### Security Considerations

1. **Change default passwords and keys**
2. **Use HTTPS in production**
3. **Set up proper CORS origins**
4. **Enable rate limiting**
5. **Use environment variables for secrets**
6. **Regular security updates**

### Docker Production Deployment

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests and ensure everything works
5. Submit a pull request

### Code Style

- **Backend**: Follow PEP 8 Python style guide
- **Frontend**: Use ESLint and Prettier configuration
- **Commits**: Use conventional commit messages

## Getting Help

- **Issues**: Report bugs on GitHub Issues
- **Documentation**: Check the `/docs` folder
- **API Documentation**: Available at `/docs` endpoint
- **Examples**: See the `/examples` folder

## Development Tools

### Recommended IDE Extensions

- **Python**: Python Extension Pack
- **TypeScript/React**: ES7+ React/Redux/React-Native snippets
- **Docker**: Docker Extension
- **Database**: PostgreSQL Extension

### Monitoring and Debugging

- **Backend Logs**: `docker-compose logs -f backend`
- **Frontend Logs**: Browser DevTools Console
- **Database**: pgAdmin or DBeaver
- **API Testing**: Postman or Insomnia