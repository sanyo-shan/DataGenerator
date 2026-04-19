import json
import random
import pandas as pd
from datetime import datetime, timedelta

# Load Schema
with open("schema.json", "r") as f:
    schema = json.load(f)

