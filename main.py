from backend.tools.schema_loader import schema
from backend.tools.entity_classifier import EntityClassifier
from backend.tools.data_generator_ai import Data_Generator
from backend.agent.agents import Agent
from backend.tools.excel_writer import ExcelWriter

class Main:
    
    def __init__(self):

        count = int(input("Enter the number of records:"))
        user_prompt = input("Enter the prompt: ")

        # Classify entity type
        classify_entity = EntityClassifier()
        entity_type = classify_entity.classify_entity(user_prompt)
        print("Entity Type: ", entity_type)

        # Generate synthetic healthcare records
        data_generator = Data_Generator()
        raw_data = data_generator.generate_data(entity_type, count)

        # Save to CSV
        excel_writer = ExcelWriter()
        excel_writer.save_to_excel(raw_data)


if __name__ == "__main__":
    main = Main()
    

    