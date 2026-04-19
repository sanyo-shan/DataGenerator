# Classifying which entity the user is referring to

from main import user_prompt
from agent.agents import model

def classify_entity(user_prompt):

    entity_prompt = f"""
    Classify the user request into one of these entity types:

    1. family_subscription → family/group data
    2. individual → general person data
    3. medicare_individual → age >= 65, medicare

    User input: "{user_prompt}"

    Return ONLY JSON:
    {
        "entity_type": "..."
    }
"""
    response = model.generate_content(entity_prompt)
    return response





