from app.database import questions_collection

# Sample questions across different difficulty levels and topics
questions = [
    # Easy questions (difficulty 0.1-0.3)
    {
        "question": "What is 12 * 8?",
        "options": ["96", "88", "108", "112"],
        "correct_answer": "96",
        "difficulty": 0.2,
        "topic": "Arithmetic",
        "tags": ["multiplication", "basic"]
    },
    {
        "question": "What is 15 + 27?",
        "options": ["42", "41", "43", "40"],
        "correct_answer": "42",
        "difficulty": 0.1,
        "topic": "Arithmetic",
        "tags": ["addition", "basic"]
    },
    {
        "question": "What is the value of 5² ?",
        "options": ["10", "15", "25", "20"],
        "correct_answer": "25",
        "difficulty": 0.2,
        "topic": "Arithmetic",
        "tags": ["exponents", "basic"]
    },
    {
        "question": "What is 100 - 37?",
        "options": ["63", "73", "53", "67"],
        "correct_answer": "63",
        "difficulty": 0.15,
        "topic": "Arithmetic",
        "tags": ["subtraction", "basic"]
    },
    
    # Medium questions (difficulty 0.4-0.6)
    {
        "question": "Solve: 2x + 5 = 13",
        "options": ["3", "4", "5", "6"],
        "correct_answer": "4",
        "difficulty": 0.5,
        "topic": "Algebra",
        "tags": ["linear equations", "solving"]
    },
    {
        "question": "What is 15% of 200?",
        "options": ["30", "25", "35", "20"],
        "correct_answer": "30",
        "difficulty": 0.45,
        "topic": "Arithmetic",
        "tags": ["percentages", "calculation"]
    },
    {
        "question": "If 3x - 7 = 11, what is x?",
        "options": ["4", "5", "6", "7"],
        "correct_answer": "6",
        "difficulty": 0.5,
        "topic": "Algebra",
        "tags": ["linear equations"]
    },
    {
        "question": "What is the area of a rectangle with length 8 and width 5?",
        "options": ["40", "26", "13", "30"],
        "correct_answer": "40",
        "difficulty": 0.4,
        "topic": "Geometry",
        "tags": ["area", "rectangle"]
    },
    {
        "question": "Simplify: 3(x + 4)",
        "options": ["3x + 4", "3x + 12", "x + 12", "3x + 7"],
        "correct_answer": "3x + 12",
        "difficulty": 0.45,
        "topic": "Algebra",
        "tags": ["distributive property", "simplification"]
    },
    
    # Hard questions (difficulty 0.7-0.9)
    {
        "question": "What is the derivative of x²?",
        "options": ["2x", "x", "x²", "2"],
        "correct_answer": "2x",
        "difficulty": 0.7,
        "topic": "Calculus",
        "tags": ["derivative", "power rule"]
    },
    {
        "question": "Solve: x² - 5x + 6 = 0",
        "options": ["x = 2 or x = 3", "x = 1 or x = 6", "x = -2 or x = -3", "x = 2 or x = 4"],
        "correct_answer": "x = 2 or x = 3",
        "difficulty": 0.75,
        "topic": "Algebra",
        "tags": ["quadratic equations", "factoring"]
    },
    {
        "question": "What is the integral of 2x?",
        "options": ["x² + C", "2x² + C", "x²/2 + C", "2"],
        "correct_answer": "x² + C",
        "difficulty": 0.8,
        "topic": "Calculus",
        "tags": ["integration", "antiderivative"]
    },
    {
        "question": "In a right triangle, if one angle is 30°, what is the other acute angle?",
        "options": ["60°", "45°", "90°", "30°"],
        "correct_answer": "60°",
        "difficulty": 0.65,
        "topic": "Geometry",
        "tags": ["triangles", "angles"]
    },
    {
        "question": "What is log₂(32)?",
        "options": ["5", "4", "6", "3"],
        "correct_answer": "5",
        "difficulty": 0.7,
        "topic": "Algebra",
        "tags": ["logarithms", "exponents"]
    },
    {
        "question": "If f(x) = 3x² - 2x + 1, what is f(2)?",
        "options": ["9", "11", "13", "7"],
        "correct_answer": "9",
        "difficulty": 0.6,
        "topic": "Algebra",
        "tags": ["functions", "evaluation"]
    },
]

def seed_database():
    """
    Seed the database with sample questions.
    Clears existing questions first.
    """
    # Clear existing questions
    questions_collection.delete_many({})
    
    # Insert new questions
    result = questions_collection.insert_many(questions)
    
    print(f"✅ Successfully inserted {len(result.inserted_ids)} questions")
    print("\nQuestions by difficulty:")
    print(f"  Easy (0.1-0.3): {sum(1 for q in questions if q['difficulty'] <= 0.3)}")
    print(f"  Medium (0.4-0.6): {sum(1 for q in questions if 0.4 <= q['difficulty'] <= 0.6)}")
    print(f"  Hard (0.7-0.9): {sum(1 for q in questions if q['difficulty'] >= 0.7)}")
    print("\nQuestions by topic:")
    topics = {}
    for q in questions:
        topics[q['topic']] = topics.get(q['topic'], 0) + 1
    for topic, count in topics.items():
        print(f"  {topic}: {count}")

if __name__ == "__main__":
    seed_database()
