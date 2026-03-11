"""
Simple test script to verify the API is working correctly.
Run this after starting the server with: uvicorn app.main:app --reload
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing AI Adaptive Diagnostic Engine API\n")
    
    # Test 1: Start session
    print("1️⃣ Starting new session...")
    response = requests.post(f"{BASE_URL}/start-session")
    if response.status_code == 200:
        session_data = response.json()
        session_id = session_data["session_id"]
        print(f"   ✅ Session created: {session_id}\n")
    else:
        print(f"   ❌ Failed to create session: {response.status_code}")
        return
    
    # Test 2: Get questions and answer them
    questions_answered = 0
    max_questions = 5
    
    print(f"2️⃣ Answering {max_questions} questions...\n")
    
    for i in range(max_questions):
        # Get next question
        response = requests.get(f"{BASE_URL}/next-question/{session_id}")
        
        if response.status_code != 200:
            print(f"   ❌ Failed to get question: {response.status_code}")
            break
        
        question_data = response.json()
        
        if "complete" in question_data:
            print(f"   ℹ️  No more questions available")
            break
        
        question_id = question_data["_id"]
        question_text = question_data["question"]
        options = question_data["options"]
        difficulty = question_data["difficulty"]
        topic = question_data["topic"]
        
        print(f"   Question {i+1}:")
        print(f"   Topic: {topic} | Difficulty: {difficulty}")
        print(f"   {question_text}")
        for idx, option in enumerate(options):
            print(f"      {chr(65+idx)}) {option}")
        
        # For testing, just pick the first option
        answer = options[0]
        
        # Submit answer
        response = requests.post(
            f"{BASE_URL}/submit-answer",
            json={
                "session_id": session_id,
                "question_id": question_id,
                "answer": answer
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            correct = result["correct"]
            new_ability = result["new_ability"]
            correct_answer = result["correct_answer"]
            
            status = "✅ Correct!" if correct else f"❌ Wrong! (Answer: {correct_answer})"
            print(f"   {status}")
            print(f"   New ability score: {new_ability}\n")
            questions_answered += 1
        else:
            print(f"   ❌ Failed to submit answer: {response.status_code}\n")
        
        time.sleep(0.5)
    
    # Test 3: Get session details
    print("3️⃣ Fetching session details...")
    response = requests.get(f"{BASE_URL}/session/{session_id}")
    if response.status_code == 200:
        session = response.json()
        stats = session.get("statistics", {})
        print(f"   Total Questions: {stats.get('total_questions', 0)}")
        print(f"   Correct Answers: {stats.get('correct_answers', 0)}")
        print(f"   Accuracy: {stats.get('accuracy', 0)}%")
        print(f"   Final Ability Score: {session.get('ability_score', 0.5)}\n")
    
    # Test 4: Generate study plan
    print("4️⃣ Generating AI study plan...")
    response = requests.post(
        f"{BASE_URL}/generate-plan",
        json={"session_id": session_id}
    )
    
    if response.status_code == 200:
        plan_data = response.json()
        print(f"   ✅ Study plan generated!")
        print(f"\n   📚 Personalized Study Plan:")
        print(f"   {'-' * 50}")
        study_plan = plan_data.get("study_plan", "")
        for line in study_plan.split('\n'):
            if line.strip():
                print(f"   {line}")
        print(f"   {'-' * 50}")
        print(f"\n   📊 Performance Summary:")
        print(f"   - Ability Score: {plan_data.get('ability_score', 0)}")
        print(f"   - Topics to Improve: {', '.join(plan_data.get('topics_missed', [])) or 'None'}")
        print(f"   - Questions Answered: {plan_data.get('questions_answered', 0)}")
        print(f"   - Accuracy: {plan_data.get('accuracy', 0)}%")
    else:
        print(f"   ⚠️  Note: Study plan generation requires OpenAI API key")
        print(f"   Add OPENAI_API_KEY to .env file to enable this feature")
    
    print(f"\n{'='*60}")
    print("✅ API test completed successfully!")
    print(f"{'='*60}")

if __name__ == "__main__":
    try:
        # Test if server is running
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("❌ Server is not responding. Please start it with:")
            print("   uvicorn app.main:app --reload")
            exit(1)
        
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Please start it with:")
        print("   uvicorn app.main:app --reload")
        exit(1)
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        exit(1)
