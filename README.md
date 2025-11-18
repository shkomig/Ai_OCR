# 🎓 Interactive Homework Learning Platform

![Platform Logo](./frontend/public/Logo.png)

An AI-powered platform that transforms traditional homework into engaging, interactive learning experiences using OCR technology, Claude AI, and gamification.

## 🌟 Features

### 🔍 Smart OCR Processing
- **Camera-Based Upload**: Capture homework documents using smartphone camera
- **Google Cloud Vision Integration**: Advanced OCR for text extraction
- **Multi-Language Support**: Hebrew, English, and Mathematics
- **Automatic Subject Detection**: Intelligent categorization of content

### 🤖 AI-Powered Content Analysis
- **Claude AI Integration**: Deep content analysis and learning objective extraction
- **Topic Identification**: Automatically identifies key concepts and topics
- **Difficulty Assessment**: Evaluates complexity and suggests appropriate interventions
- **Personalized Recommendations**: Tailored learning paths based on content analysis

### 🎮 Interactive Gamification
- **Dynamic Game Generation**: Transform homework into engaging games
- **Adaptive Quizzes**: Auto-generated quizzes with multiple question types
- **Study Guides**: AI-created review materials and summaries
- **Progress Tracking**: Monitor performance and learning progress

### 📊 Analytics & Insights
- **Performance Dashboard**: Comprehensive view of learning metrics
- **Score Tracking**: Monitor quiz and game performance
- **Time Analytics**: Track study time across subjects
- **Subject Breakdown**: Visual representation of learning activities

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER (React/Vite)                    │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │  Camera Capture  │  │  Document Upload │  │ Game Display │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
└────────────────────────┬──────────────────────────────────────┘
                         │ REST API
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                            │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐          │
│  │   OCR        │ │   Content    │ │  Game/Quiz  │          │
│  │  Service     │ │  Analysis    │ │  Generation │          │
│  └──────────────┘ └──────────────┘ └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Google      │ │  Claude API  │ │  Database    │
│  Vision API  │ │  (Anthropic) │ │  (SQLite)    │
└──────────────┘ └──────────────┘ └──────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)
- Google Cloud Vision API credentials
- Anthropic Claude API key

### Installation

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd Ai_OCR
```

#### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys:
# - ANTHROPIC_API_KEY
# - GOOGLE_APPLICATION_CREDENTIALS
# - SECRET_KEY (generate a secure random key)

# Initialize database
python -c "from app.core.database import init_db; init_db()"

# Run the backend
python main.py
```

Backend will be available at `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

#### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

### Docker Deployment

```bash
# Make sure you have .env file with API keys
docker-compose up -d

# Access the application
# Frontend: http://localhost
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 📁 Project Structure

```
Ai_OCR/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints/      # API route handlers
│   │   ├── core/               # Core configurations
│   │   ├── models/             # Database models
│   │   ├── schemas/            # Pydantic schemas
│   │   └── services/           # Business logic
│   ├── tests/                  # Backend tests
│   ├── main.py                 # Application entry point
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile             # Backend Docker config
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   ├── services/           # API clients
│   │   └── utils/              # Utility functions
│   ├── public/                 # Static assets (logo, images)
│   ├── package.json            # NPM dependencies
│   └── Dockerfile             # Frontend Docker config
├── docs/                       # Documentation
├── homework-system-design.md   # System design document
├── docker-compose.yml          # Docker orchestration
└── README.md                   # This file
```

## 🔑 API Keys Configuration

### Google Cloud Vision API
1. Create a project in [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Cloud Vision API
3. Create a service account and download JSON key
4. Set `GOOGLE_APPLICATION_CREDENTIALS` to the path of JSON file

### Anthropic Claude API
1. Sign up at [Anthropic](https://www.anthropic.com/)
2. Generate an API key
3. Set `ANTHROPIC_API_KEY` in your .env file

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user

### Document Endpoints
- `POST /api/v1/documents/upload` - Upload homework document
- `GET /api/v1/documents/` - List user documents
- `GET /api/v1/documents/{id}` - Get document details
- `GET /api/v1/documents/{id}/status` - Check processing status
- `DELETE /api/v1/documents/{id}` - Delete document

### Content Generation Endpoints
- `POST /api/v1/content/{document_id}/games` - Generate game
- `POST /api/v1/content/{document_id}/quizzes` - Generate quiz
- `POST /api/v1/content/{document_id}/review-materials` - Generate study guide
- `GET /api/v1/content/{content_id}` - Get content details

### Progress Endpoints
- `POST /api/v1/progress/submit` - Submit quiz/game results
- `GET /api/v1/progress/user/{user_id}` - Get user progress
- `GET /api/v1/progress/user/{user_id}/dashboard` - Get dashboard data

## 🎯 Usage Guide

### 1. Upload Homework
1. Click "Upload" in navigation
2. Select subject (Mathematics, English, or Hebrew)
3. Drag & drop or select homework image
4. Click "Upload and Analyze"

### 2. Wait for Processing
- OCR extracts text from image
- Claude AI analyzes content
- System identifies topics and creates learning profile

### 3. Generate Learning Content
- **Games**: Interactive matching, puzzles, fill-in-the-blanks
- **Quizzes**: Multiple choice, true/false, short answer questions
- **Study Guides**: Summaries, examples, memory aids

### 4. Complete Activities
- Answer questions
- Get instant feedback
- Track your score and progress

### 5. Monitor Progress
- View dashboard for performance metrics
- Check subject breakdown
- Review recent activities

## 🔧 Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Building for Production
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm run build
```

## 📊 Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **Google Cloud Vision**: OCR and image analysis
- **Anthropic Claude**: AI content analysis and generation
- **Redis**: Caching and session management
- **Pydantic**: Data validation

### Frontend
- **React 18**: UI library
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **Lucide React**: Icon library

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Web server and reverse proxy

## 🌐 Supported Languages

- **English**: Full support for English language homework
- **Hebrew**: Native support including RTL text and Hebrew-specific content
- **Mathematics**: Symbol recognition and equation parsing

## 📝 License

This project is part of an educational platform development initiative.

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests.

## 📞 Support

For issues and questions:
- Check the [System Design Document](./homework-system-design.md)
- Review API documentation at `/docs` endpoint
- Open an issue on GitHub

## 🎓 Credits

Developed as a comprehensive AI-powered learning platform integrating:
- Google Cloud Vision for OCR
- Anthropic Claude for AI analysis and content generation
- Modern web technologies for seamless user experience

---

**Transform homework into adventure. Make learning fun! 🚀**
