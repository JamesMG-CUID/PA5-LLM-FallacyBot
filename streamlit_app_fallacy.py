# Import from 3rd party libraries
import streamlit as st
import openai

#Init
openai_api_key = None
api_key_form_submitted = False
#openai.api_key = ""


# Define functions

def analyse_text(text_input: str, strictness: str):
    if not text_input:
        st.session_state.text_error = "Please enter your text"
        return

    with text_spinner_placeholder:
        with st.spinner("Please wait while your text is analysed..."):
            prompt = text_input
            st.session_state.n_requests += 1
            st.session_state.text = (
                openai.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.4,
                top_p = 0.8,
                max_tokens = 450,
                messages=[
                    {"role": "system", "content": f"You are a grammar checker bot that outputs in formatted html. Check the following text for grammar mistakes in the context of {strictness} Correct the errors and provide a list of (Fairly simple) explanations."},
                    {"role": "user", "content": f"Please fix this, highlighting any changes in green and, more importantly, showing the original with mistakes in red: {prompt}"},
                    ]
                )
            )



# Render Streamlit page
st.set_page_config(page_title="GrammarBuddy", page_icon="🤖")
st.session_state.text_error = None
st.session_state.text = None


text_spinner_placeholder = st.spinner()

if "n_requests" not in st.session_state:
    st.session_state.n_requests = 0

with st.sidebar:
    api_key_form = st.form(key="api_key_form")
    openai_api_key = api_key_form.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    api_key_form_submitted = api_key_form.form_submit_button("Submit")

    if api_key_form_submitted:
        if True:                              #check_openai_api_key(openai_api_key):
            openai.api_key = openai_api_key
            st.success("Your OpenAI API key was saved successfully!")
        else:
            st.info("Your OpenAI API key is invalid, please check to see if it is correctly inputted or contact OpenAI")



text_input_form = st.form(key = "text_input_form")
text_input = text_input_form.text_area(label="Input your text here", placeholder="Mary hadn't a little lamb.")
strictness = text_input_form.text_area(label="How strict should the checker be?", placeholder="(e.g. academic (default), slang, business)", height=50)
text_input_form_submitted = text_input_form.form_submit_button("Submit")


if not strictness:
    strictness = "academic"
if not text_input:
    st.info("Please add some text to continue.")
else:     
    analyse_text(text_input, strictness)
    
    

text_spinner_placeholder = st.empty()

if st.session_state.text_error:
    st.error(st.session_state.text_error)

if st.session_state.text:
    st.markdown("""---""")
    output = st.session_state.text
    st.markdown(f"<h3>Here's what your GrammarBuddy has to say: </h3><p>\t{output.choices[0].message.content}</p>", unsafe_allow_html=True)


    # st.write(f":red[{text_input}]")
    # st.text_area(label="Corrected", value=f"{output.choices[0].message.content}", height=400)
    image_spinner_placeholder = st.empty()
    
    
