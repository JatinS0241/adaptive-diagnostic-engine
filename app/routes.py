from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database import sessions_collection, questions_collection
from app.adaptive_engine import update_ability
from app.llm_service import generate_study_plan
from app.models import SubmitAnswerRequest, StudyPlanRequest

router = APIRouter()

@router.post("/start-session")
def start_session():
    """
    Start a new testing session with default ability score.
    
    Returns:
        session_id: Unique identifier for the session
    """
    session = {
        "ability_score": 0.5,
        "questions_answered": [],
        "topics_missed": []
    }
    
    result = sessions_collection.insert_one(session)
    
    return {"session_id": str(result.inserted_id)}


@router.get("/next-question/{session_id}")
def next_question(session_id: str):
    """
    Get the next question based on current ability level.
    
    Args:
        session_id: Session identifier
    
    Returns:
        Question object matching current ability level
    """
    try:
        session = sessions_collection.find_one({"_id": ObjectId(session_id)})
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        ability = session["ability_score"]
        answered_ids = [q["question_id"] for q in session["questions_answered"]]
        
        # Find question near ability level that hasn't been answered
        question = questions_collection.find_one({
            "_id": {"$nin": answered_ids},
            "difficulty": {
                "$gte": ability - 0.15,
                "$lte": ability + 0.15
            }
        })
        
        # If no question found in range, get any unanswered question
        if not question:
            question = questions_collection.find_one({
                "_id": {"$nin": answered_ids}
            })
        
        if not question:
            return {"message": "No more questions available", "complete": True}
        
        # Convert ObjectId to string for JSON serialization
        question["_id"] = str(question["_id"])
        
        return question
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/submit-answer")
def submit_answer(request: SubmitAnswerRequest):
    """
    Submit an answer and update ability score.
    
    Args:
        request: Contains session_id, question_id, and answer
    
    Returns:
        Correctness, new ability score, and correct answer
    """
    try:
        question = questions_collection.find_one({"_id": ObjectId(request.question_id)})
        
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        correct = request.answer == question["correct_answer"]
        
        session = sessions_collection.find_one({"_id": ObjectId(request.session_id)})
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        ability = session["ability_score"]
        
        # Update ability using IRT algorithm
        new_ability = update_ability(
            ability,
            question["difficulty"],
            correct
        )
        
        # Track topics missed
        topics_missed = session.get("topics_missed", [])
        if not correct and question["topic"] not in topics_missed:
            topics_missed.append(question["topic"])
        
        # Update session in database
        sessions_collection.update_one(
            {"_id": ObjectId(request.session_id)},
            {
                "$set": {
                    "ability_score": new_ability,
                    "topics_missed": topics_missed
                },
                "$push": {
                    "questions_answered": {
                        "question_id": request.question_id,
                        "correct": correct,
                        "difficulty": question["difficulty"]
                    }
                }
            }
        )
        
        return {
            "correct": correct,
            "new_ability": round(new_ability, 2),
            "correct_answer": question["correct_answer"],
            "topic": question["topic"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/generate-plan")
def generate_plan(request: StudyPlanRequest):
    """
    Generate personalized study plan based on performance.
    
    Args:
        request: Contains session_id
    
    Returns:
        Personalized study plan and session statistics
    """
    try:
        session = sessions_collection.find_one({"_id": ObjectId(request.session_id)})
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        ability = session["ability_score"]
        topics_missed = session.get("topics_missed", [])
        questions_answered = session.get("questions_answered", [])
        
        # Generate study plan using local rule-based logic
        study_plan = generate_study_plan(topics_missed, ability)
        
        # Calculate statistics
        correct_count = sum(1 for q in questions_answered if q["correct"])
        total_count = len(questions_answered)
        accuracy = (correct_count / total_count * 100) if total_count > 0 else 0
        
        return {
            "study_plan": study_plan,
            "ability_score": round(ability, 2),
            "topics_missed": topics_missed,
            "questions_answered": total_count,
            "accuracy": round(accuracy, 1)
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/session/{session_id}")
def get_session(session_id: str):
    """
    Get session details and statistics.
    
    Args:
        session_id: Session identifier
    
    Returns:
        Session data and performance statistics
    """
    try:
        session = sessions_collection.find_one({"_id": ObjectId(session_id)})
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session["_id"] = str(session["_id"])
        
        questions_answered = session.get("questions_answered", [])
        correct_count = sum(1 for q in questions_answered if q["correct"])
        total_count = len(questions_answered)
        
        session["statistics"] = {
            "total_questions": total_count,
            "correct_answers": correct_count,
            "accuracy": round((correct_count / total_count * 100) if total_count > 0 else 0, 1)
        }
        
        return session
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
