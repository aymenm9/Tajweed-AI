# Tajweed-AI
Tajweed-AI : mobile app , salam hack Hackathon

# Tjweed-AI Backend

Backend for Tjweed-AI, a Django DRF application to assist users in learning Quranic recitation and Tajweed with AI-generated content. Hosted on Render using Docker.

## Project Idea
A mobile app backend leveraging AI to provide personalized Tajweed lessons, quizzes, and recitation correction for Quran learners.

## Deployment
- **URL**: [https://my-django-app-latest-ht9a.onrender.com](https://my-django-app-latest-ht9a.onrender.com)
- **Hosting**: Render
- **Container**: Docker

## Tech Stack
- **Framework**: Django REST Framework (DRF)
- **Language**: Python
- **Database**: SQLite
- **AI**: Google Gemini API
- **Deployment**: Docker on Render

## API Endpoints

### Authentication
- **`/api/signup/`**  
  - `POST`: Register a new user.
- **`/api/token/`**  
  - `POST`: Generate access and refresh tokens.
- **`/api/refresh/token/`**  
  - `POST`: Refresh access token.

### Core Functionality
- **`/api/generate_quiz/{{topic}}/`**  
  - `GET`: Generate a quiz for a given topic.
- **`/api/quiz/`**  
  - `GET`: List quizzes.  
  - `POST`: Create quiz.  
  - `PUT`, `PATCH`, `DELETE`: Update or delete quiz.
- **`/api/chatbot/`**  
  - `POST`: Send message to chatbot.  
  - `GET`: Retrieve chat history.  
  - `DELETE`: Clear chat history.
- **`/api/goals/`**  
  - `POST`: Set user goals and generate lessons.  
  - `PUT`: Update goals.  
  - `GET`: Retrieve goals.
- **`/api/lessons/`**  
  - `GET`: List lessons.  
  - `PATCH`: Update lesson.  
  - `DELETE`: Delete all lessons.
- **`/api/get_verse/{{topic}}/`**  
  - `GET`: Fetch a verse related to a topic.
- **`/api/recitation_correction/`**  
  - `POST`: Submit audio file, topic, and verse for correction.

## Setup
1. Clone the repo: `git clone <repo-url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start server: `python manage.py runserver`

## Notes
- All AI features (quiz generation, chatbot, lesson creation, recitation correction) use the Google Gemini API.
- Docker configuration is included for deployment.