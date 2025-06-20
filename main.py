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


# Task 1: Upload the Papers
# So that GPT knows about the latest AGI research, we will provide it with some arxiv papers. There are 10 recent papers on AGI stored in the papers directory of this workbook.
#
# Click File -> Show workbook files to see a file browser.
# The papers were found by searching arxiv for "AGI", then eyballing recent papers for content on definitions of AGI or progress towards AGI.
#
# The table below shows the filenames and the titles of the papers.

papers = pd.DataFrame({
    "filename": [
        "2405.10313v1.pdf",
        "2401.03428v1.pdf",
        "2401.09395v2.pdf",
        "2401.13142v3.pdf",
        "2403.02164v2.pdf",
        "2403.12107v1.pdf",
        "2404.10731v1.pdf",
        "2312.11562v5.pdf",
        "2311.02462v2.pdf",
        "2310.15274v1.pdf"
    ],
    "title": [
        "How Far Are We From AGI?",
        "EXPLORING LARGE LANGUAGE MODEL BASED INTELLIGENT AGENTS: DEFINITIONS, METHODS, AND PROSPECTS",
        "CAUGHT IN THE QUICKSAND OF REASONING, FAR FROM AGI SUMMIT: Evaluating LLMs’ Mathematical and Coding Competency through Ontology-guided Interventions",
        "Unsocial Intelligence: an Investigation of the Assumptions of AGI Discourse",
        "Cognition is All You Need The Next Layer of AI Above Large Language Models",
        "Scenarios for the Transition to AGI",
        "What is Meant by AGI? On the Definition of Artificial General Intelligence",
        "A Survey of Reasoning with Foundation Models",
        "Levels of AGI: Operationalizing Progress on the Path to AGI",
        "Systematic AI Approach for AGI: Addressing Alignment, Energy, and AGI Grand Challenges"
    ]
})
papers["filename"] = "papers/" + papers["filename"]
print(papers)