# AI Adaptive Diagnostic Engine

> An intelligent adaptive testing system that adjusts question difficulty in real-time based on student performance using Item Response Theory (IRT) and generates personalized study plans using AI.

## 🎯 Overview

This system implements an adaptive diagnostic engine that:
- Dynamically adjusts question difficulty based on student ability
- Uses IRT-based algorithms for ability estimation
- Generates personalized study plans using OpenAI's GPT models
- Tracks performance across different topics
- Provides detailed analytics and insights

## 🏗️ Architecture

```
User
  │
  │ HTTP/REST
  ▼
┌─────────────────────────────────┐
│      FastAPI Backend            │
│  ┌───────────────────────────┐  │
│  │   Adaptive Engine         │  │
│  │   (IRT Algorithm)         │  │
│  └───────────────────────────┘  │
│              │                   │
│              ▼                   │
│  ┌───────────────────────────┐  │
│  │   MongoDB Database        │  │
│  │   - Questions             │  │
│  │   - User Sessions         │  │
│  └───────────────────────────┘  │
│              │                   │
│              ▼                   │
│  ┌───────────────────────────┐  │
│  │   OpenAI LLM Service      │  │
│  │   (Study Plan Generator)  │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

## 🚀 Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **AI/ML**: OpenAI GPT-4o-mini
- **Algorithm**: Item Response Theory (IRT)

## ✨ Features

### Core Features
- ✅ **Adaptive Difficulty Selection** - Questions adjust to student ability level
- ✅ **IRT Ability Scoring** - Sophisticated ability estimation using IRT principles
- ✅ **Personalized Study Plans** - AI-generated recommendations based on performance
- ✅ **Topic Tracking** - Identifies weak areas for targeted improvement
- ✅ **Real-time Analytics** - Live performance metrics and statistics

### Algorithm Details

**Ability Update Formula:**
```python
expected = 1 / (1 + e^(difficulty - ability))
result = 1 if correct else 0
ability_new = ability_old + learning_rate * (result - expected)
```

**Difficulty Matching:**
- Questions are selected within ±0.15 of current ability
- Ability score ranges from 0.0 (beginner) to 1.0 (expert)
- Learning rate: 0.1 (balanced adaptation speed)

## 📋 Prerequisites

- Python 3.8+
- MongoDB installed and running
- OpenAI API key

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/adaptive-diagnostic-engine.git
cd adaptive-diagnostic-engine
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
# Copy the example env file
copy .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your_actual_api_key_here
```

### 4. Start MongoDB
```bash
# Make sure MongoDB is running on localhost:27017
# Or update the connection string in database.py
```

### 5. Seed the database
```bash
python seed_questions.py
```

### 6. Run the application
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### Start a new session
```http
POST /start-session
```
**Response:**
```json
{
  "session_id": "507f1f77bcf86cd799439011"
}
```

### Get next question
```http
GET /next-question/{session_id}
```
**Response:**
```json
{
  "_id": "q1",
  "question": "What is 12 * 8?",
  "options": ["96", "88", "108", "112"],
  "difficulty": 0.2,
  "topic": "Arithmetic"
}
```

### Submit answer
```http
POST /submit-answer
Content-Type: application/json

{
  "session_id": "507f1f77bcf86cd799439011",
  "question_id": "q1",
  "answer": "96"
}
```
**Response:**
```json
{
  "correct": true,
  "new_ability": 0.55,
  "correct_answer": "96",
  "topic": "Arithmetic"
}
```

### Generate study plan
```http
POST /generate-plan
Content-Type: application/json

{
  "session_id": "507f1f77bcf86cd799439011"
}
```
**Response:**
```json
{
  "study_plan": "1. Focus on Algebra fundamentals...\n2. Practice...",
  "ability_score": 0.55,
  "topics_missed": ["Algebra", "Calculus"],
  "questions_answered": 10,
  "accuracy": 70.0
}
```

### Get session details
```http
GET /session/{session_id}
```

## 📊 Database Schema

### Questions Collection
```javascript
{
  "_id": ObjectId,
  "question": String,
  "options": [String],
  "correct_answer": String,
  "difficulty": Float,  // 0.0 to 1.0
  "topic": String,
  "tags": [String]
}
```

### Sessions Collection
```javascript
{
  "_id": ObjectId,
  "ability_score": Float,  // 0.0 to 1.0
  "questions_answered": [{
    "question_id": String,
    "correct": Boolean,
    "difficulty": Float
  }],
  "topics_missed": [String]
}
```

## 🎓 How It Works

1. **Session Start**: Student begins with ability score of 0.5 (medium difficulty)

2. **Question Selection**: System selects question near current ability level
   - Easy: difficulty 0.1-0.3
   - Medium: difficulty 0.4-0.6
   - Hard: difficulty 0.7-0.9

3. **Answer Submission**: Student answers question

4. **Ability Update**: IRT algorithm updates ability based on:
   - Question difficulty
   - Answer correctness
   - Expected probability of success

5. **Adaptive Flow**: Next question difficulty matches new ability level

6. **Study Plan**: After test, AI analyzes weak topics and generates personalized recommendations

## 🎯 Sample Workflow

```python
# 1. Start session
session = POST /start-session
# → ability: 0.5

# 2. Get first question (medium difficulty ~0.5)
question = GET /next-question/{session_id}

# 3. Submit correct answer
result = POST /submit-answer
# → ability increases to 0.55

# 4. Get harder question (difficulty ~0.55)
question = GET /next-question/{session_id}

# 5. Submit wrong answer
result = POST /submit-answer
# → ability decreases to 0.50

# 6. Continue for 10-15 questions...

# 7. Generate study plan
plan = POST /generate-plan
```

## 🧪 Testing the API

### Using cURL:
```bash
# Start session
curl -X POST http://localhost:8000/start-session

# Get next question
curl http://localhost:8000/next-question/YOUR_SESSION_ID

# Submit answer
curl -X POST http://localhost:8000/submit-answer \
  -H "Content-Type: application/json" \
  -d '{"session_id":"YOUR_SESSION_ID","question_id":"QUESTION_ID","answer":"96"}'
```

### Using Python:
```python
import requests

# Start session
response = requests.post("http://localhost:8000/start-session")
session_id = response.json()["session_id"]

# Get question
question = requests.get(f"http://localhost:8000/next-question/{session_id}").json()

# Submit answer
result = requests.post("http://localhost:8000/submit-answer", json={
    "session_id": session_id,
    "question_id": question["_id"],
    "answer": "96"
})
```

## 🚀 Deployment

### Deploy to Render/Railway/Fly.io

1. Add `Procfile`:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. Set environment variables:
   - `OPENAI_API_KEY`
   - `MONGODB_URI` (use MongoDB Atlas for cloud database)

3. Deploy and share your live demo link!

## 📈 Future Enhancements

- [ ] Add difficulty heatmap visualization
- [ ] Implement ability graph over time
- [ ] Add question difficulty distribution charts
- [ ] Session history and progress tracking
- [ ] Multiple question topic categories
- [ ] Time tracking per question
- [ ] Export results to PDF
- [ ] User authentication

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Name](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- Built with FastAPI
- Uses OpenAI GPT-4o-mini for study plan generation
- Implements IRT (Item Response Theory) principles
- MongoDB for flexible data storage

---

⭐ **Star this repo if you find it helpful!**

📧 **Questions?** Open an issue or contact me directly.

🚀 **Live Demo**: [Add your deployed link here]
