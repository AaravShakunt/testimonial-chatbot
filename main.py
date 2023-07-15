import streamlit as st
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
# from utils import getResponse
from streamlit_chat import message
from utils import getResponse

import pinecone 
from langchain.vectorstores import Pinecone


st.subheader("Chatbot with Langchain, ChatGPT, Pinecone, and Streamlit")


if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)


# container for chat history
response_container = st.container()

# Create a button to open the pop-up box
if st.button("Open Pop-up Box"):
    if 'show_popup' not in st.session_state:
        st.session_state.show_popup = True
    else:
        st.session_state.show_popup = not st.session_state.show_popup

# Display the pop-up box if the toggle is True
if st.session_state.get('show_popup', False):
    with st.form("popup_form"):
        st.subheader("Pop-up Box")
        mail = st.text_input("Mail")
        query = st.text_input("Query")
        submit_button = st.form_submit_button("Submit")
        if submit_button:
            # Process the submitted data
            # Add your logic here
            st.success(f"Submitted: Mail - {mail}, Query - {query}")
            st.session_state.show_popup = False  # Close the pop-up box after submitting
textcontainer = st.container()

with textcontainer:
    query = st.text_input("Query: ", key="input")
    if query:
        with st.spinner("typing..."):
            
            response = getResponse(query)
        st.session_state.requests.append(query)
        st.session_state.responses.append(response) 
with response_container:
    if st.session_state['responses']:

        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i],key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')


