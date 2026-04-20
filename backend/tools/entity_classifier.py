# Classifying which entity the user is referring to
from backend.agent.agents import Agent

class EntityClassifier:
    def __init__(self):
        self.agent = Agent()

    def classify_entity(self, user_prompt):
        entity_prompt = f"""
    Classify the user request into one of these entity types:

    1. family_subscription → family/group data
    2. individual → general person data
    3. medicare_individual → age >= 65, medicare

    User input: "{user_prompt}"

    Return ONLY type:
    family_subscription | individual | medicare_individual
"""
        response = self.agent.model.generate_content(entity_prompt)
        return response.text.strip()





