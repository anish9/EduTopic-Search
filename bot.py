import streamlit as st
from openai import OpenAI

print(st.__version__)
client = OpenAI(api_key=None)



st.set_page_config(page_title="MBRDI-pdf-bot", page_icon="🤖")
#######

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Doto:wght@100..900&family=Funnel+Display:wght@300..800&display=swap" rel="stylesheet">
<style>
.title {
    font-family: 'Funnel Display', sans-serif;
    font-size: 2.5rem;
    font-weight: bold;
    background: linear-gradient(to right, #19ff71, #70ffd4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: left;
    margin-bottom: 30px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)



#######

col1,col2 = st.columns([1,10])
with col1:
    st.image('images.png', width=190)
with col2:
    # Custom title with styled markdown
    st.markdown('<div class="title">MBRDI - DocAssistant</div>', unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []



# st.session_state.messages.append(("Hello","Hey, How are you doing?"))
# st.session_state.messages.append(("I am good","can you write a blog post on like my friend... ?"))

for user_type,converse in st.session_state.messages:
    with st.chat_message(user_type):
        st.markdown(converse)

print(st.session_state)

if prompt := st.chat_input("What would you like to discuss?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    

    st.session_state.messages.append(('user',prompt))

    print(st.session_state.messages)
    with st.chat_message("assistant"):
        response = client.chat.completions.create(model="gpt-4o",
                                                  messages=[{"role":user_type,"content":converse} for user_type,converse in st.session_state.messages],
                                                  temperature=0.6,
                                                  max_tokens=250,
                                                )
        response_text = response.choices[0].message.content
        st.markdown(response_text)

    st.session_state.messages.append(("system",response_text))
