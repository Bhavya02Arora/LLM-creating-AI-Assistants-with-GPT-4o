"Took reference from: 'https://www.datacamp.com/code-along/creating-ai-assistants-with-gpt-4o'"

import os

# Pre-requisite: Install the OpenAI Python package
# pip install openai==1.33.0

# Import the os package
import os

# Check if the environment variable exists before accessing it
# openai_api_key = os.environ.get("OPENAI_API_KEY")
# if openai_api_key is None:
#     raise ValueError("OPENAI_API_KEY environment variable is not set")

# Import the openai package
import openai

# Import the pandas package with an alias
import pandas as pd


import openai

# Define an OpenAI client. Assign to client.
client = openai.OpenAI(api_key="your_openai_api_key_here")

