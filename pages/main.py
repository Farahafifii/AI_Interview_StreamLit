import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
import time 

# Load environment variables from .env file
load_dotenv()


def getResponse(run_id):
    # Wait for the assistant to generate a response
    while True:
        run = st.session_state['client'].beta.threads.runs.retrieve(
            thread_id=st.session_state['thread'].id,
            run_id=run_id
        )
        if run.status == 'completed':
            break
        time.sleep(1)  # Wait for 1 second before checking again

    messages = st.session_state['client'].beta.threads.messages.list(
        thread_id=st.session_state['thread'].id
    )
    
    return messages.data[0].content[0].text.value



def assistant_init(jobTitle, lvl, questionType):
    client = OpenAI(api_key =os.getenv("OPENAI_API_KEY"))
    assistant = client.beta.assistants.retrieve(os.getenv("ASSISTANT_ID"))
    thread = client.beta.threads.create(
        messages=[
            {
            "role": "user",
            "content": "Hello",
            }
        ]
    )
    st.session_state["client"] = client
    st.session_state["assistant"] = assistant
    st.session_state["thread"] = thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions=f"""
            Your candidate is a {jobTitle} with a {lvl} experience level and prefered questions type is {questionType}, customize the interview accordingly. 
            Now great the user and start the interview by asking the user to introduce himself."""
    )
    
    return getResponse(run.id)
    


def sendUserMessage(user_message):
    st.session_state['client'].beta.threads.messages.create(
        thread_id=st.session_state['thread'].id,
        role="user",
        content=user_message
    )
    run = st.session_state['client'].beta.threads.runs.create(
        thread_id=st.session_state['thread'].id,
        assistant_id=st.session_state['assistant'].id,
    )

    return getResponse(run.id)



def chat_page():
    # st.write(f'jobTitle: {st.session_state.jobTitle}')
    # st.write(f'questionType: {st.session_state.questionType}')
    # st.write(f'difficulty: {st.session_state.difficulty}')
    # st.write(f'notes: {st.session_state.notes}')
    st.title("Mock Interview")
    #client = OpenAI(api_key =os.getenv("API_KEY"))

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "assistant" not in st.session_state:
        first_message = assistant_init(st.session_state.jobTitle, st.session_state.difficulty, st.session_state.questionType)
        st.session_state.messages.append({"role": "assistant" , "content": first_message})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input('Hello'):
        st.session_state.messages.append({"role":"user" , "content":prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        response = sendUserMessage(prompt)
        with st.chat_message("assistant"): st.markdown(response)   
        st.session_state.messages.append({"role": "assistant" , "content": response})

if __name__ == '__main__':
    chat_page()
