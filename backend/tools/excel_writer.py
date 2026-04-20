from datetime import datetime
import pandas as pd
from io import StringIO

class ExcelWriter:
    def __init__(self):
        timestamp = datetime.now().timestamp()
        self.filename = "C:\\Users\\Sanyo\\Desktop\\AI Engineer\\Projects\\UST Projects\\DataGenerator\\output\\synthetic_healthcare_data"+str(timestamp)+".csv"

    def save_to_excel(self, raw_data):
        try:
            # Using StringIO to treat the string response like a file
            df = pd.read_csv(StringIO(raw_data))
            df.to_csv(self.filename, index=False)
            print(f"Successfully saved {len(df)} records to {self.filename}")
        except Exception as e:
            print(f"Error parsing CSV: {e}\nRaw Output: {raw_data}")