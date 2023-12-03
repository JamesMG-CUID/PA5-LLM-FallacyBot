# Import from 3rd party libraries
import streamlit as st
import openai

# Initialize
st.cache_data.clear()
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""

openai.api_key = st.session_state.openai_api_key

if "text_error" not in st.session_state:
    st.session_state.text_error = None

if "text" not in st.session_state:
    st.session_state.text = None

if "n_requests" not in st.session_state:
    st.session_state.n_requests = 0



# Define functions
def analyze_text(text_input = "If we let Timmy skip school, then soon all the kids will be skipping school, and we can't have that."):
    if not text_input:
        st.session_state.text_error = "Please enter your text"
        return

    with text_spinner_placeholder:
        prompt = text_input
        st.session_state.n_requests += 1
        st.session_state.text = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.4,
            top_p=0.8,
            max_tokens=450,
            messages=[
                {"role": "system", "content": "You are a fallacy checker bot that outputs in formatted html (Feel free to use color for emphasis). Provide a list of (Fairly simple) explanations if you find fallacies in user input."},
                {"role": "user", "content": f"Provide a list of fallacies from this text and explain what the fallacies are/mean (If there are non the just say 'Fallacy-Free!'): {prompt}"},
            ]
        )

# Render Streamlit page
st.set_page_config(page_title="FallacyBot", page_icon="🤖")
explanation_text = """
<h3 style = 'text-align: center;color:green'> FallacyBot </h3> 
<h6 style='text-align: center'> Checking for <span style='color:red'>fallacies</span> in your text since 2023!</h6>
<p> For your convenience, a default example is provided. If you don't input any text, the bot will use the example text. </p>
    """
st.markdown(explanation_text, unsafe_allow_html=True)

text_spinner_placeholder = st.spinner()


with st.sidebar:
    api_key_form = st.form(key="api_key_form")
    openai_api_key = api_key_form.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    api_key_form_submitted = api_key_form.form_submit_button("Submit")

    if api_key_form_submitted:
        if True:                              #check_openai_api_key(openai_api_key):
            openai.api_key = st.session_state.openai_api_key
            st.success("Your OpenAI API key was saved successfully!")
        else:
            st.info("Your OpenAI API key is invalid, please check to see if it is correctly inputted or contact OpenAI")


text_input = st.text_area(label="Input your text here", placeholder="If we let Timmy skip school, then soon all the kids will be skipping school, and we can't have that.")
st.button("Submit", on_click=analyze_text(text_input))

text_spinner_placeholder = st.empty()

if st.session_state.text_error:
    st.error(st.session_state.text_error)

if st.session_state.text:
    st.markdown("""---""")
    output = st.session_state.text
    st.markdown(f"<h3 style='color: green;'>Here's what FallacyBot has to say:</h3><p style='color: white;'><br><p><i>\"{text_input}\"</i></p><br>{output.choices[0].message.content}</p>", unsafe_allow_html=True)
    image_spinner_placeholder = st.empty()
