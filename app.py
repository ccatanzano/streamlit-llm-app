#https://github.com/ccatanzano/streamlit-llm-app
#py -m pip freeze > requirements.txt
#py -m streamlit run app.py
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="LLM Chat App", page_icon="🤖")
st.title("🤖 LLM Chat App with Expert Role + Memory")

st.markdown("""
### How to use
1. Define the **expert role** (e.g. *Senior Software Engineer*, *English Teacher*, *Startup Mentor*)
2. Ask your questions
3. Enjoy a **multi-turn conversation**
""")

# Expert role input
expert_role = st.text_input(
    "Define the expert role for the AI:",
    value="Senior Software Engineer"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    else:
        with st.chat_message("assistant"):
            st.write(msg.content)

# User chat input
user_input = st.chat_input("Ask something...")

def ask_llm(user_prompt: str, expert_role: str):
    system_prompt = f"You are a {expert_role}. Answer clearly, accurately, and helpfully."

    chat = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3
    )

    messages = [SystemMessage(content=system_prompt)]
    messages.extend(st.session_state.messages)
    messages.append(HumanMessage(content=user_prompt))

    response = chat.invoke(messages)
    return response.content

if user_input:
    st.session_state.messages.append(HumanMessage(content=user_input))

    with st.spinner("Thinking..."):
        answer = ask_llm(user_input, expert_role)

    st.session_state.messages.append(AIMessage(content=answer))

    with st.chat_message("assistant"):
        st.write(answer)
