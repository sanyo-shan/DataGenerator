from main import count
from schema_loader import schema
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

# We'll come back later to this part
def generate_data(entity_type, count):
    entity_schema = schema["entities"][entity_type]
    fields = entity_schema["fields"]

    used_ssns = set()

    def generate_ssn():
        while True:
            ssn = "".join([str(random.randint(0, 9)) for _ in range(9)])
            if ssn not in used_ssns:
                used_ssns.add(ssn)
                return ssn

    def generate_dob(min_age=0, max_age=90):
        today = datetime.today()
        start = today - timedelta(days=max_age * 365)
        end = today - timedelta(days=min_age * 365)
        return fake.date_between(start_date=start, end_date=end)

    data = []

    for _ in range(count):
        row = {}

        for field in fields:
            name = field["name"]
            ftype = field["type"]

            if name == "first_name":
                row[name] = fake.first_name()

            elif name == "last_name":
                row[name] = fake.last_name()

            elif name == "ssn":
                row[name] = generate_ssn()

            elif name == "dob":
                row[name] = generate_dob()

            elif ftype == "enum":
                row[name] = random.choice(field["values"])

            elif name == "address":
                row[name] = fake.street_address()

            elif name == "city":
                row[name] = fake.city()

            elif name == "state":
                row[name] = fake.state_abbr()

            elif name == "zip_code":
                row[name] = fake.zipcode()[:5]

            elif name == "medicare_member_id":
                row[name] = None  # set later if needed

            else:
                row[name] = None

        data.append(row)

    
    entity_schema = schema["entities"][entity_type]
    fields = entity_schema["fields"]

    used_ssns = set()


    def generate_ssn():
        while True:
            ssn = "".join([str(random.randint(0, 9)) for _ in range(9)])
            if ssn not in used_ssns:
                used_ssns.add(ssn)
                return ssn


    def generate_dob(min_age=0, max_age=90):
        today = datetime.today()
        start = today - timedelta(days=max_age * 365)
        end = today - timedelta(days=min_age * 365)
        return fake.date_between(start_date=start, end_date=end)


    def generate_row(shared=None):
        row = {}

        for field in fields:
            name = field["name"]
            ftype = field["type"]

            # Shared fields (family)
            if shared and name in shared:
                row[name] = shared[name]
                continue

            if name == "first_name":
                row[name] = fake.first_name()

            elif name == "last_name":
                row[name] = fake.last_name()

            elif name == "ssn":
                row[name] = generate_ssn()

            elif name == "dob":
                row[name] = generate_dob()

            elif ftype == "enum":
                row[name] = random.choice(field["values"])

            elif name == "address":
                row[name] = fake.street_address()

            elif name == "city":
                row[name] = fake.city()

            elif name == "state":
                row[name] = fake.state_abbr()

            elif name == "zip_code":
                row[name] = fake.zipcode()[:5]

            elif name == "medicare_member_id":
                row[name] = None  # set later if needed

            else:
                row[name] = None

        return row


    data = []

    # 🔵 INDIVIDUAL / MEDICARE
    if entity_type in ["individual", "medicare_individual"]:
        for _ in range(count):
            row = generate_row()

            # Medicare rule
            if entity_type == "medicare_individual":
                row["dob"] = generate_dob(min_age=65, max_age=90)
                row["medicare_member_id"] = "MED" + str(random.randint(100000, 999999))

            data.append(row)

    # 🟢 FAMILY
    elif entity_type == "family_subscription":
        generated = 0

        while generated < count:
            family_size = random.randint(2, 6)

            # Shared values
            shared = {
                "last_name": fake.last_name(),
                "address": fake.street_address(),
                "city": fake.city(),
                "state": fake.state_abbr(),
                "zip_code": fake.zipcode()[:5]
            }

            roles = ["self", "spouse"]
            roles += ["child"] * random.randint(0, 3)
            if random.choice([True, False]):
                roles.append("newborn")

            for role in roles:
                if generated >= count:
                    break

                row = generate_row(shared)

                row["relationship"] = role

                # Newborn rule
                if role == "newborn":
                    row["dob"] = datetime.today() - timedelta(days=random.randint(0, 30))

                # Medicare rule
                age = (datetime.today() - row["dob"]).days // 365
                if age >= 65:
                    row["medicare_member_id"] = "MED" + str(random.randint(100000, 999999))

                data.append(row)
                generated += 1

    # ✅ OUTPUT
    print(data)


