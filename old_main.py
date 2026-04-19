import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
from io import StringIO
from google.genai import types
from datetime import datetime

# 1. Load Configuration
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

class HealthcareDataAgent:
    def __init__(self, model_name="gemini-3-flash-preview"):
        self.model = genai.GenerativeModel(model_name)
        
    def generate_batch(self, num_records):
        """Generates a batch of synthetic healthcare data."""
        config = types.GenerateContentConfig(
            thinking_config = types.ThinkingConfig(thinking_level="low")
        )
        prompt = f"""
        Generate {num_records} rows of realistic synthetic healthcare data.
        Output ONLY a CSV format with the following headers:
        - Last Name: Realistic family name
        - First Name: Realistic individual name
        - SSN: Unique 9-digit string (formatted as #########)
        - DOB: Date of birth (YYYY-MM-DD)
        - Gender: Male, Female, or Non-binary
        - Relationship: Subscriber, Spouse, or Child
        - Address: Street address
        - City: City name
        - State: 2-letter state code
        - Zip Code: 5-digit zip code
        - Medicare Member ID: Alpha-numeric ID (Only for members 65+ or Medicare COB; otherwise leave blank)
    Rules:
        1. FAMILY GROUPING: Generate data in clusters of 3-5 rows per family. 
        - All members of a cluster MUST have the exact same Address, City, State, and Zip Code.
        - All members of a cluster should typically share the same Last Name.
        2. SSN Uniqueness: Every individual, including newborns and children, must have a unique 9-digit SSN.
        3. Logic Consistency: Ensure the Relationship and DOB are logically consistent (e.g., a "Child" should be younger than a "Subscriber").
        4. Formatting: Do not include any markdown formatting like csv or .
        5. No Filler: Do not include any introductory text, conversational filler, or explanations. Start immediately with the header row.
        """
        
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def save_to_csv(self, raw_data, timestamp):
        filename="C:\\Users\\268878\\Desktop\\LocalClaims2\\output\\synthetic_healthcare_data"+timestamp+".csv"
        """Cleans and saves the data to a CSV file."""
        try:
            # Using StringIO to treat the string response like a file
            df = pd.read_csv(StringIO(raw_data))
            df.to_csv(filename, index=False)
            print(f"Successfully saved {len(df)} records to {filename}")
        except Exception as e:
            print(f"Error parsing CSV: {e}\nRaw Output: {raw_data}")

class DataValidator:
    def __init__(self, df):
        self.df = df
        self.errors = []

    def validate(self):
        # Rule 1: Check SSN Uniqueness
        if self.df['SSN'].duplicated().any():
            self.errors.append("Error: Duplicate SSNs detected.")

        # Rule 2: Check Medicare ID Logic (Must be blank if age < 65)
        # Note: This requires calculating age from DOB
        today = pd.to_datetime('today')
        self.df['DOB'] = pd.to_datetime(self.df['DOB'])
        self.df['Age'] = (today - self.df['DOB']).dt.days // 365
        
        invalid_medicare = self.df[(self.df['Age'] < 65) & (self.df['Medicare Member ID'].notna())]
        if not invalid_medicare.empty:
            self.errors.append(f"Error: Medicare ID found for {len(invalid_medicare)} underage members.")

        return len(self.errors) == 0, self.errors



# 3. Execution
if __name__ == "__main__":
    agent = HealthcareDataAgent()
    
    def main_pipeline():
        
        # 1. Generate synthetic healthcare records
        print("Generating healthcare records...")
        raw_csv_output = agent.generate_batch(num_records=15)

        # Get current timestamp for unique filename
        current_time = datetime.now().timestamp()
        agent.save_to_csv(raw_csv_output, current_time)
        df = pd.read_csv(StringIO(raw_csv_output))

        # 2. Data Validate
        validator = DataValidator(df)
        is_valid, error_list = validator.validate()

        if not is_valid:
            print("Validator flagged issues: ", error_list)

