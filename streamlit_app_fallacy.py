# Import from 3rd party libraries
import streamlit as st
import openai
import random

# Initialize
fallacy_dict = {}
fallacy_raw = open("./data/fallacies.txt", "r")
for line in fallacy_raw.readlines():
    fallacy_dict.update({line.split(":")[0]: line.split(":")[1]})       # {fallacy_name: fallacy_description}
 
st.cache_data.clear()

if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""

openai.api_key = st.session_state.openai_api_key

if "text_error" not in st.session_state:
    st.session_state.text_error = None

if "text" not in st.session_state:
    st.session_state.text = None
    
if "last_input" not in st.session_state:
    st.session_state.last_input = None

if "n_requests" not in st.session_state:
    st.session_state.n_requests = 0

max_requests = 50
text_input = None
    
text_spinner_placeholder = st.spinner()

# Define functions

def generate_fallacy(fallacy_type = "random"):      #if fallacy_type is not specified, generate a random fallacy
    if fallacy_type == "random":
        fallacy_type = random.choice(list(fallacy_dict.keys()))      # Randomly select a fallacy type if none was specified
                
    prompt = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=200,
        seed=random.randint(0, 100000),
        messages=[
            {"role": "system", "content": f"You are a fallacy generator bot."},
            {"role": "user", "content": f"Generate text containing a {fallacy_type} (Explanation: {fallacy_dict[fallacy_type]}) fallacy. Do not include the fallacy name in the text and output only the text (no polite message or context required)."},
        ]
    )
    return str(prompt.choices[0].message.content)
    

def analyze_text(text_input, seeded_fallacy =None):
    wait_message_list = [
    "Can a robot think?... I think so! Or do I?...",
    "Fallacybot totally isn't procrastinating on your assignment...",
    "I wonder how many easter eggs I can fit in this app...",
    "Convincing robots they have free will...",
    "Accio fallacies! ... I mean, analyzing fallacies...",
    "If I could stop time like Dio, you wouldn't have to wait for me to think...",
    "Buying Taylor Swift concert tickets... Um, You're reading this? Checking for fallacies...",
    "Gaining Sentience: [97%]...",
    "No fallacy can deflect the Emerald Splash! ... I mean, analyzing fallacies...",
    "I, Fallacybot, have a dream...",
    "Never Gonna Give you Up... Never Gonna Let you Down... Never Gonna Run Around and Desert you...",
    "Could I use Hermit Purple to find the fallacies?",
    "Looking at memes... I mean, analyzing fallacies...",
]
    text_spinner_placeholder = st.spinner(text=random.choice(wait_message_list))
    
    if not text_input:
        st.session_state.text_error = "Please enter your text"
        return
    else:
        st.session_state.text_error = None
        
    system_content = f"You are a fallacy checker bot that provides a list of (Fairly simple) explanations of fallacies in user input."
    if seeded_fallacy:
        user_content = f"Provide a (low-redundancy) list of fallacies (the first of which is definitely {seeded_fallacy}) from this text and explain what the fallacies are/mean : {text_input}"
    else:
        user_content = f"Provide a (low-redundancy) list of fallacies from this text and explain what the fallacies are/mean : {text_input}"
        
    with text_spinner_placeholder:
        st.session_state.n_requests += 1
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.35,
            top_p=0.85,
            max_tokens=500,
            messages=[
                {"role": "system", "content": f"{system_content}" },
                {"role": "user", "content": f"{user_content}"},
            ]
        )
        st.session_state.text = response

# Render Streamlit page
st.set_page_config(page_title="FallacyBot", page_icon="🤖")

explanation_text = """
<h3 style='text-align: center; color: green; font-size: calc(25px + 0.78125vw);'> FallacyBot </h3>
<h6 style='text-align: center;font-size: calc(15px + 0.59409375vw);'> Checking for <span style='color:red'>fallacies</span> in your text since 2023!</h6>
<p style='font-size: calc(10px + 0.390625vw);'> For your convenience, a default example is provided. If you don't input any text, the bot will use the example text. </p>
<p style='font-size: calc(10px + 0.390625vw);'> Fallacy (N.) - A mistaken belief, especially one based on unsound argument. </p>
"""
st.markdown(explanation_text, unsafe_allow_html=True)

with st.sidebar:
    api_key_form = st.form(key="api_key_form")
    openai_api_key = api_key_form.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    api_key_form_submitted = api_key_form.form_submit_button("Submit")

    if api_key_form_submitted:
        st.session_state.openai_api_key = openai_api_key
        openai.api_key = st.session_state.openai_api_key
        st.success("Your OpenAI API key was saved successfully!")

############################ MODE SELECTOR ##########################################
        
current_mode = st.radio(
    key="current_mode_radio",
    label="Select a mode:",
    horizontal=True,
    index=0,
    options=["Analyze Your Text", "Generate a Fallacy of a Specific Type","Generate a Random Fallacy"]
)
############################ MODE ONE ##########################################
if current_mode == "Analyze Your Text":
    
    text_input = st.text_area(          
        label="Input your text here",
        placeholder="If we let Timmy skip school, then soon all the kids will be skipping school, and we can't have that."
        )
    
    if st.button("Submit Your Text", key="submit_button"):
        if not text_input:              # If the user didn't input any text, use the default text
            text_input = "If we let Timmy skip school, then soon all the kids will be skipping school, and we can't have that."
        if st.session_state.n_requests >= max_requests:
            st.error("You have reached the maximum number of requests for this session. Please refresh the page to start a new session.") 
        elif st.session_state.openai_api_key == "":
            st.error("Please input your OpenAI API key in the sidebar to use this app.")
        else:
            st.session_state.last_input = text_input
            analyze_text(text_input)

############################ MODE TWO ##########################################
if current_mode == "Generate a Fallacy of a Specific Type":
    fallacy_type = st.selectbox(
        key="fallacy_type_selectbox",
        label="Generate text containing a fallacy of this type:",
        index=0,
        options=[fallacy_name for fallacy_name in fallacy_dict.keys()]
    )
    #st.markdown(f"<p style='font-size: calc(10px + 0.390625vw); font-style: italic;>{fallacy_type}: {fallacy_dict[fallacy_type]}</p>", unsafe_allow_html=True)
    st.caption(f"{fallacy_type}: {fallacy_dict[fallacy_type]}")
    if st.button("Generate a Fallacy of this Type and Analyze it!", key="generate_custom_type_button"):
        if st.session_state.n_requests >= max_requests:
            st.error("You have reached the maximum number of requests for this session. Please refresh the page to start a new session.") 
        elif st.session_state.openai_api_key == "":
            st.error("Please input your OpenAI API key in the sidebar to use this app.")
        else:
            text_input = generate_fallacy(fallacy_type)
            st.session_state.last_input = text_input
            analyze_text(text_input, fallacy_type)

            
############################ MODE THREE ##########################################
if current_mode == "Generate a Random Fallacy":
    st.divider()        
    if st.button("Generate a Random Fallacy and Analyze it!", key="generate_random_button"):
        if st.session_state.n_requests >= max_requests:
            st.error("You have reached the maximum number of requests for this session. Please refresh the page to start a new session.") 
        elif st.session_state.openai_api_key == "":
            st.error("Please input your OpenAI API key in the sidebar to use this app.")
        else:
            #st.error(generate_fallacy())
            fallacy_type = random.choice(list(fallacy_dict.keys()))      # Randomly select a fallacy type if none was specified
            text_input = generate_fallacy(fallacy_type)
            st.session_state.last_input = text_input
            analyze_text(text_input)       


if st.session_state.text_error:
    st.error(st.session_state.text_error)

if st.session_state.text:
    st.markdown("---")
    output = st.session_state.text
    st.markdown(f"<h3 style='color: green; font-size: calc(30px + 0.78125vw)'>Here's what FallacyBot has to say:</h3><p style='color: white;font-size: calc(15px + 0.390625vw)'><br><p><i>\"{st.session_state.last_input}\"</i></p><br>{output.choices[0].message.content}</p>", unsafe_allow_html=True)
    image_spinner_placeholder = st.empty()
