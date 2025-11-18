# Setup Guide

## Prerequisites

### Required
- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn package manager

### Optional
- Docker & Docker Compose (for containerized deployment)
- Redis (for caching)
- PostgreSQL (alternative to SQLite for production)

## API Keys Setup

### 1. Anthropic Claude API

1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add to `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-...
   ```

### 2. Google Cloud Vision API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Cloud Vision API
4. Create a service account:
   - Go to IAM & Admin > Service Accounts
   - Create service account with Vision API User role
   - Create and download JSON key
5. Add to `.env`:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
   GOOGLE_CLOUD_PROJECT_ID=your-project-id
   ```

## Backend Setup

### 1. Create Virtual Environment
```bash
cd backend
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env file with your API keys and settings
```

### 4. Initialize Database
```bash
python -c "from app.core.database import init_db; init_db()"
```

### 5. Run Backend Server
```bash
# Development mode (with auto-reload)
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

## Frontend Setup

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Environment
```bash
# Create .env file (optional - defaults are provided)
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env
```

### 3. Run Development Server
```bash
npm run dev
```

The frontend will be available at:
- App: http://localhost:3000

### 4. Build for Production
```bash
npm run build
# Built files will be in dist/ directory
```

## Docker Setup

### 1. Configure Environment Variables
Create a `.env` file in the root directory with your API keys:
```bash
ANTHROPIC_API_KEY=your-key-here
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

### 2. Build and Run Containers
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- Frontend: http://localhost
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Database Options

### SQLite (Default - Development)
No additional setup required. Database file is created automatically.

### PostgreSQL (Production)
1. Install PostgreSQL
2. Create database:
   ```sql
   CREATE DATABASE homework_platform;
   ```
3. Update `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/homework_platform
   ```

## Redis Setup (Optional)

### Local Installation
```bash
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# Windows
# Download from: https://github.com/microsoftarchive/redis/releases
```

### Using Docker
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

## Troubleshooting

### Backend Issues

**Import errors:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**Database errors:**
```bash
# Reinitialize database
rm homework_platform.db
python -c "from app.core.database import init_db; init_db()"
```

**OCR not working:**
- Verify Google Cloud credentials are correct
- Check if Cloud Vision API is enabled
- Ensure service account has proper permissions

### Frontend Issues

**Module not found:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**API connection errors:**
- Verify backend is running on port 8000
- Check CORS settings in backend `.env`
- Ensure VITE_API_URL is correct

### Docker Issues

**Port conflicts:**
```bash
# Change ports in docker-compose.yml
# Or stop conflicting services
```

**Permission errors:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

## First User Setup

1. Start both backend and frontend
2. Navigate to http://localhost:3000
3. Click "Sign up"
4. Fill in registration form:
   - Username
   - Email
   - Password (minimum 6 characters)
   - Grade level
   - Native language
   - Subjects (optional)
5. Click "Create Account"
6. Log in with your credentials

## Testing the System

### 1. Upload Test Document
1. Log in to the platform
2. Click "Upload" in navigation
3. Select a subject
4. Upload a homework image
5. Wait for processing to complete

### 2. Generate Content
1. Go to "My Documents"
2. Click on uploaded document
3. Generate game, quiz, or review material
4. Complete the generated content

### 3. View Dashboard
1. Click "Dashboard" in navigation
2. Review your learning statistics

## Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment instructions.

## Support

If you encounter issues:
1. Check this setup guide
2. Review error logs
3. Consult the [README.md](../README.md)
4. Open an issue on GitHub
