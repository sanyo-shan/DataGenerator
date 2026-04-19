from tools.schema_loader import schema
from tools.entity_classifier import classify_entity

if __name__=="__main__":
    
    count = int(input("Enter the number of records:"))
    user_prompt = input("Enter the prompt: ")

    def main_pipeline():
        response = classify_entity(user_prompt)
        


    