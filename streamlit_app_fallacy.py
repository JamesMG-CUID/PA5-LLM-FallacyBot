# Import from 3rd party libraries
import streamlit as st
import openai

# Initialize
openai_api_key = None

# Define functions
def analyze_text(text_input: str):
    if not text_input:
        st.session_state.text_error = "Please enter your text"
        return

    with text_spinner_placeholder:
        with st.spinner("Please wait while your text is analyzed..."):
            prompt = text_input
            st.session_state.n_requests += 1
            st.session_state.text = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=0.4,
                top_p=0.8,
                max_tokens=450,
                messages=[
                    {"role": "system", "content": "You are a fallacy checker bot that outputs in formatted html. Provide a list of (Fairly simple) explanations if you find fallacies in user input."},
                    {"role": "user", "content": f"Check this text for fallacies and explain what the fallacies are/mean: {prompt}"},
                ]
            )

# Render Streamlit page
st.set_page_config(page_title="FallacyBot", page_icon="🤖")
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
        if True:  # check_openai_api_key(openai_api_key):
            openai.api_key = openai_api_key
            st.success("Your OpenAI API key was saved successfully!")
        else:
            st.info("Your OpenAI API key is invalid, please check to see if it is correctly inputted or contact OpenAI")

text_input_form = st.form(key="text_input_form")
text_input = text_input_form.text_area(label="Input your text here", placeholder="Ex. If we let Tommy skip school, then soon all the kids will be skipping school, and we can't have that.")
text_input_form_submitted = text_input_form.form_submit_button("Submit")

if not text_input:
    text_input = "If we let Tommy skip school, then soon all the kids will be skipping school, and we can't have that."
else:
    analyze_text(text_input)

text_spinner_placeholder = st.empty()

if st.session_state.text_error:
    st.error(st.session_state.text_error)

if st.session_state.text:
    st.markdown("""---""")
    output = st.session_state.text
    st.markdown(f"<h3 style='color: #3498db;'>Here's what FallacyBot has to say:</h3><p style='color: #2ecc71;'>\t{output.choices[0].message.content}</p>", unsafe_allow_html=True)
    image_spinner_placeholder = st.empty()
