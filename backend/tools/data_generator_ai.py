# Data Generating using AI

from backend.agent.agents import Agent

agent = Agent()

class Data_Generator:
    def generate_data(self, entity_type, num_records):
        if entity_type == "family_subscription":
            prompt = f"""
Generate {num_records} rows of synthetic healthcare data for FAMILY subscriptions.

Output ONLY CSV format with header:
last_name,first_name,ssn,dob,gender,relationship,address,city,state,zip_code,medicare_member_id

STRICT RULES:

1. FAMILY GROUPING:
- Data must be generated in FAMILY groups (clusters).
- Each family must contain 2 to 6 members.
- Each group MUST have:
  - Exactly 1 'self'
  - Exactly 1 'spouse'
  - 0 to 3 'child'
  - 0 to 1 'newborn'

2. FAMILY CONSISTENCY:
- All members in a family MUST share:
  last_name, address, city, state, zip_code

3. SSN:
- Must be unique per individual
- Must be exactly 9-digit numeric string

4. DOB & AGE LOGIC:
- 'self' should be adult (age 25–60)
- 'spouse' similar age range
- 'child' must be younger than parents (age 1–25)
- 'newborn' must have DOB within last 30 days

5. GENDER:
- Must be one of: male, female, other

6. STATE & ZIP:
- Use valid US 2-letter state codes
- Zip must be 5-digit numeric

7. MEDICARE RULE:
- If age >= 65 → medicare_member_id MUST be generated
- Otherwise → leave blank

8. FORMAT:
- No explanations
- No markdown
- Start directly with header row
"""
        elif entity_type == "individual":
            prompt = f"""
Generate {num_records} rows of synthetic healthcare data for INDIVIDUAL records.

Output ONLY CSV format with header:
last_name,first_name,ssn,dob,gender,address,city,state,zip_code

STRICT RULES:

1. INDEPENDENT RECORDS:
- Each row is completely independent
- No grouping or shared data required

2. SSN:
- Must be unique
- Must be exactly 9-digit numeric string

3. DOB:
- Must be realistic (age between 0 and 90)

4. GENDER:
- Must be one of: male, female, other

5. ADDRESS:
- Use realistic US address, city, and state

6. STATE:
- Must be valid 2-letter US state code

7. ZIP:
- Must be 5-digit numeric

8. FORMAT:
- No explanations
- No markdown
- Start directly with header row
"""
        elif entity_type == "medicare_individual":
            prompt = f"""
Generate {num_records} rows of synthetic healthcare data for MEDICARE individuals.

Output ONLY CSV format with header:
last_name,first_name,ssn,dob,gender,address,city,state,zip_code,medicare_member_id

STRICT RULES:

1. AGE CONSTRAINT:
- All individuals MUST be age 65 or older

2. MEDICARE REQUIREMENT:
- medicare_member_id is MANDATORY for every row
- Must be realistic alphanumeric format

3. SSN:
- Must be unique
- Must be exactly 9-digit numeric string

4. DOB:
- Must align with age >= 65

5. GENDER:
- Must be one of: male, female, other

6. ADDRESS:
- Use realistic US address

7. STATE:
- Must be valid 2-letter US state code

8. ZIP:
- Must be 5-digit numeric

9. FORMAT:
- No explanations
- No markdown
- Start directly with header row
"""
        else:
            raise ValueError("Invalid entity type")

        response = agent.model.generate_content(prompt)
        return response.text.strip()