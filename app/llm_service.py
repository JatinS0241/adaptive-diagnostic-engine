from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_study_plan(topics, ability):
    """
    Generate personalized study plan using LLM.
    
    Args:
        topics: List of weak topics
        ability: Current ability score (0.0 to 1.0)
    
    Returns:
        String containing study plan recommendations
    """
    prompt = f"""
Student ability score: {ability:.2f} (on a scale of 0.0 to 1.0)

Weak topics identified: {', '.join(topics) if topics else 'None - performing well overall'}

Based on this assessment, create a personalized 3-step study plan that:
1. Addresses the weak topics identified
2. Matches the student's current ability level
3. Provides actionable, specific steps

Format the response as a clear, numbered study plan.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating study plan: {str(e)}"
