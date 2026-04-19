from dotenv import load_dotenv
import google.generativeai as genai
import os
from google.genai import types

# 1. Load Configuration
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def __init__(self, model_name="gemini-3-flash-preview"):
    self.model = genai.GenerativeModel(model_name)
    config = types.GenerateContentConfig(
            thinking_config = types.ThinkingConfig(thinking_level="low")
        )
    
