from openai import OpenAI
import os
import time
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))

def show_json(obj):
    print(json.loads(obj.model_dump_json()))


# Upload the file
file = client.files.create(
    file=open(
        "data\\astro2.pdf",
        "rb",
    ),
    purpose="assistants",
)

assistant = client.beta.assistants.create(
  name="Data Reader",
  description="You are great at creating beautiful data summarizations. You analyze data present in .pdf files, understand, and come up with  a brief text summary.",
  model="gpt-4o",
  tools=[{"type": "code_interpreter"}],
  tool_resources={
    "code_interpreter": {
      "file_ids": [file.id]
    }
  }
)
READER_ASSISTANT_ID = assistant.id  # or a hard-coded ID like "asst-..."

show_json(assistant)

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")
    
def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(READER_ASSISTANT_ID, thread, user_input)
    return thread, run
    
# Pretty printing helper
def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()


# Waiting in a loop
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run    

thread, run = create_thread_and_run(
   """
      Give me the vedic horoscope for Ramesh based on
      date of birth: 18th June 1963, place of birth: Coimbatore, TamilNadu, India Time of birth: 4.04PM?
      
      Use standard procedure or the methods from the PDF uploaded.
   """
    )
run = wait_on_run(run, thread)
pretty_print(get_response(thread))
