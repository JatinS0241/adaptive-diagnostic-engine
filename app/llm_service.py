def generate_study_plan(topics, ability):
    """
    Generate a personalized, rule-based 3-step study plan.

    Args:
        topics: List of weak topics
        ability: Current ability score (0.0 to 1.0)

    Returns:
        String containing study plan recommendations
    """
    if ability < 0.35:
        level_guidance = "begin with fundamentals and untimed practice"
    elif ability < 0.65:
        level_guidance = "focus on mixed medium-difficulty sets and accuracy"
    else:
        level_guidance = "practice advanced, timed problem-solving"

    weak_topics = topics if topics else ["overall consistency"]
    primary_topic = weak_topics[0]
    secondary_topic = weak_topics[1] if len(weak_topics) > 1 else weak_topics[0]

    plan_lines = [
        f"1. Review core concepts in {primary_topic} for 30-45 minutes and solve 10 easy practice questions.",
        f"2. Do a focused practice block on {secondary_topic} ({level_guidance}) and analyze every mistake.",
        "3. Take one mixed mini-test (8-12 questions), track weak areas, and revise the top 2 mistakes before the next session.",
    ]

    return "\n".join(plan_lines)
