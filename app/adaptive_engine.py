import math

def update_ability(ability, difficulty, correct):
    """
    Update ability score using IRT-inspired algorithm.
    
    Args:
        ability: Current ability score (0.0 to 1.0)
        difficulty: Question difficulty (0.0 to 1.0)
        correct: Boolean indicating if answer was correct
    
    Returns:
        Updated ability score (clamped between 0.0 and 1.0)
    """
    # Calculate expected probability of correct answer
    expected = 1 / (1 + math.exp(difficulty - ability))
    
    # Set result based on correctness
    result = 1 if correct else 0
    
    # Learning rate controls how much ability changes
    learning_rate = 0.1
    
    # Update ability based on difference between actual and expected
    ability = ability + learning_rate * (result - expected)
    
    # Clamp ability between 0 and 1
    ability = max(0.0, min(1.0, ability))
    
    return ability
