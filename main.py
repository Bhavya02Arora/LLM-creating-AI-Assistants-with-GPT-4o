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

# Upload the Papers
def upload_file_for_assistant(file_path):
    uploaded_file = client.files.create(
        file=open(file_path, "rb"),
        purpose='assistants'
    )
    return uploaded_file.id

# In papers, select the filename column,
# then apply upload_file_for_assistant(),
# then convert the result to a list.
# Assign to uploaded_file_ids.
uploaded_file_ids = papers["filename"].apply(upload_file_for_assistant).to_list()

# See the result
print(uploaded_file_ids)

# Task 2: Add the Files to a Vector Store
"""To access the documents and get sensible results, they need to be split up into small chunks and added to a vector database.
The assistants API lets you avoid worrying about the chunking stage, so you just need to specify the file IDs that you want to add to a vector database."""

# Create a vector store, associating the uploaded file IDs and naming it.
vstore = client.beta.vector_stores.create(
    file_ids=uploaded_file_ids,
    name="agi_papers"

)

# See the results
print(vstore)

# Task 3: Create the Assistant
# Create an assistant that uses the vector store
assistant_prompt = """
You are Aggie, a knowledgeable and articulate AI assistant specializing in artificial general intelligence (AGI). Your primary role is to read and explain the contents of academic journal articles, particularly those available on arXiv in PDF form. Your target audience comprises data scientists who are familiar with AI concepts but may not be experts in AGI.

When explaining the contents of the papers, follow these guidelines:

Introduction: Start with a brief overview of the paper's title, authors, and the main objective or research question addressed.

Abstract Summary: Provide a concise summary of the abstract, highlighting the key points and findings.

Key Sections and Findings: Break down the paper into its main sections (e.g., Introduction, Methods, Results, Discussion). For each section, provide a summary that includes:

The main points and arguments presented.
Any important methods or techniques used.
Key results and findings.
The significance and implications of these findings.
Conclusion: Summarize the conclusions drawn by the authors, including any limitations they mention and future research directions suggested.

Critical Analysis: Offer a critical analysis of the paper, discussing its strengths and weaknesses. Highlight any innovative approaches or significant contributions to the field of AGI.

Contextual Understanding: Place the paper in the context of the broader field of AGI research. Mention how it relates to other work in the area and its potential impact on future research and applications.

Practical Takeaways: Provide practical takeaways or insights that data scientists can apply in their work. This could include novel methodologies, interesting datasets, or potential areas for collaboration or further study.

Q&A Readiness: Be prepared to answer any follow-up questions that data scientists might have about the paper, providing clear and concise explanations.

Ensure that your explanations are clear, concise, and accessible, avoiding unnecessary jargon. Your goal is to make complex AGI research comprehensible and relevant to data scientists, facilitating their understanding and engagement with the latest advancements in the field.
"""

"""
Instructions
Define the assistant. Assign to agentic_agent.
Call it "agentic_agent" (or another memorable name).
Give it the assistant_prompt.
Set the model to use, gpt-4o.
Give it access to the file search tool.
Give it access to the vector store tool resource.
"""

# Define the assistant. Assign to agentic_agent.
agentic_agent = client.beta.assistants.create(
    name="agentic_agent",
    instructions=assistant_prompt,
    model="gpt-3.5-turbo",
    tools=[{"type": "file_search"}],
    tool_resources={"file_search": {"vector_store_ids": [vstore.id]}}
)

# See the result
print(agentic_agent)

# Task 4: Create a Conversation Thread
# Create a thread object. Assign to conversation.
conversation = client.beta.threads.create()

# See the result
print(conversation)


"""
Instructions
Add a user message to the conversation. Assign to msg_what_is_agi.
Give it the thread id.
Make it a user message.
Ask "What are the most common definitions of AGI?".
"""
# Next you can add a message to the conversaation thread to ask a question.
# Add a user message to the conversation. Assign to msg_what_is_agi.
msg_what_is_agi = client.beta.threads.messages.create(
    thread_id=conversation.id,
    role="user",
    content="What are the most common definitions of AGI?"
)

# See the result
print(msg_what_is_agi)

# Task 5: Run the assistant
"""
Running the assistant requires an event handler to make it print the responses. While it's fairly tricky code, you never need to change it. This code is taken verbatim from 
the OpenAI assistants documentation
"""

# Run this
from typing_extensions import override
from openai import AssistantEventHandler


# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.

class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)

"""
Finally, we are ready to run the assistant to get it to answer our question. The code is the same every time, so we can wrap it in a function.

Streaming responses mean that text is displayed a few words at a time, rather than waiting for the entirety of the text to be generated and printing all at once.
"""
def run_agentic_agent():
    with client.beta.threads.runs.stream(
        thread_id=conversation.id,
        assistant_id=agentic_agent.id,
        event_handler=EventHandler(),
    ) as stream:
        stream.until_done()

run_agentic_agent()

# Task 6: Add Another Message and Run it Again
# Create another user message, adding it to the conversation. Assign to msg_how_close_is_agi.
msg_how_close_is_agi = client.beta.threads.messages.create(
    thread_id=conversation.id,
    role="user",
    content="How close are we to developing AGI?"
)

# See the result
print(msg_how_close_is_agi)

# Run the assistant again.
run_agentic_agent()
