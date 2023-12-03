import streamlit as st
from openai import OpenAI

def chat_page():
    st.write(f'jobTitle: {st.session_state.jobTitle}')
    st.write(f'questionType: {st.session_state.questionType}')
    st.write(f'difficulty: {st.session_state.difficulty}')
    st.write(f'notes: {st.session_state.notes}')
    st.title("Mock Interview")
    client = OpenAI(api_key ="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")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = 'gpt-3.5-turbo'

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input('Hello'):
        st.session_state.messages.append({"role":"user" , "content":prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in client.chat.completions.create(
                model = st.session_state['openai_model'],
                messages = [
                    {"role": m['role'], "content":m['content']}
                    for m in  st.session_state.messages
                ],
                stream = True,
            ):
                full_response +=(response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response+ "| ")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant" , "content": full_response})

if __name__ == '__main__':
    chat_page()
