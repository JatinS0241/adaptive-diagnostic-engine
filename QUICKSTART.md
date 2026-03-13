# 🚀 Quick Start Guide

## Get Up and Running in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Up Environment
```bash
# Copy the example environment file
copy .env.example .env
```

### Step 3: Start MongoDB
Make sure MongoDB is running on `localhost:27017`

**Windows:**
```bash
# Start MongoDB service
net start MongoDB
```

**Mac/Linux:**
```bash
mongod
```

### Step 4: Seed the Database
```bash
python seed_questions.py
```

You should see:
```
✅ Successfully inserted 15 questions
```

### Step 5: Start the Server
```bash
uvicorn app.main:app --reload
```

Server will start at: `http://localhost:8000`

### Step 6: Test the API
Open a new terminal and run:
```bash
python test_api.py
```

Or visit the interactive docs: `http://localhost:8000/docs`

---

## 📝 Manual Testing

### Using the Interactive Docs (Recommended)

1. Go to `http://localhost:8000/docs`
2. Click on "POST /start-session" → Try it out → Execute
3. Copy the `session_id` from the response
4. Click on "GET /next-question/{session_id}" → Try it out → Paste session_id → Execute
5. Copy the question `_id` and choose an answer
6. Click on "POST /submit-answer" → Try it out → Fill in the form → Execute
7. Repeat steps 4-6 for multiple questions
8. Click on "POST /generate-plan" → Try it out → Enter session_id → Execute

### Using cURL

```bash
# 1. Start session
curl -X POST http://localhost:8000/start-session

# 2. Get next question (replace SESSION_ID)
curl http://localhost:8000/next-question/SESSION_ID

# 3. Submit answer (replace SESSION_ID and QUESTION_ID)
curl -X POST http://localhost:8000/submit-answer \
  -H "Content-Type: application/json" \
  -d "{\"session_id\":\"SESSION_ID\",\"question_id\":\"QUESTION_ID\",\"answer\":\"96\"}"

# 4. Generate study plan
curl -X POST http://localhost:8000/generate-plan \
  -H "Content-Type: application/json" \
  -d "{\"session_id\":\"SESSION_ID\"}"
```

---

## 🎯 What You Get

✅ **15 sample questions** across different difficulty levels
✅ **Adaptive algorithm** that adjusts difficulty based on performance
✅ **REST API** with 5 endpoints
✅ **IRT-based scoring** for accurate ability estimation
✅ **AI study plans** (requires OpenAI API key)
✅ **Complete documentation** with examples

---

## 📊 Understanding the Results

### Ability Score
- **0.0 - 0.3**: Beginner level
- **0.4 - 0.6**: Intermediate level
- **0.7 - 1.0**: Advanced level

### How It Adapts
1. Start at ability 0.5 (medium)
2. Answer correctly → ability increases → get harder question
3. Answer incorrectly → ability decreases → get easier question
4. Questions are matched within ±0.15 of your ability

---

## 🐛 Troubleshooting

### "Cannot connect to MongoDB"
- Make sure MongoDB is running: `mongod` or `net start MongoDB`
- Check if running on port 27017

### "Module not found"
- Install dependencies: `pip install -r requirements.txt`

### "Session not found"
- The session_id might be incorrect
- Make sure you're using the ID returned from `/start-session`

### "Study plan generation failed"
- This feature requires an OpenAI API key
- Add your key to the `.env` file
- You can still test all other features without it

---

## 🎓 Next Steps

1. **Add more questions**: Edit `seed_questions.py`
2. **Deploy online**: Use Render, Railway, or Fly.io
3. **Build a frontend**: Create a React/Vue app that calls these APIs
4. **Enhance the algorithm**: Implement full IRT with discrimination parameter
5. **Add analytics**: Track performance over time

---

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Python Driver](https://pymongo.readthedocs.io/)
- [OpenAI API](https://platform.openai.com/docs/)
- [Item Response Theory](https://en.wikipedia.org/wiki/Item_response_theory)

---

**Need help?** Check the main [README.md](README.md) or open an issue!
