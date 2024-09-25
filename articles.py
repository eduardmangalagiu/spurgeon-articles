import subprocess
import sys
import streamlit as st

# Function to upgrade the OpenAI package
def upgrade_openai_package():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'openai'])
        st.success("OpenAI package upgraded successfully!")
    except PermissionError:
        st.error("Permission denied: Cannot upgrade the OpenAI package. Please upgrade manually.")
    except Exception as e:
        st.error(f"An error occurred while upgrading the OpenAI package: {e}")

# Run the upgrade command when the app starts
upgrade_openai_package()

# Import OpenAI after upgrade
import openai

# Set the OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Define the app colors
BG_COLOR = "#003b5d"  # Dark blue background
TEXT_COLOR = "#b78c2e"  # Golden text
FONT = 'Futura'  # Use Futura font for a professional look

# Set the custom styles
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {BG_COLOR};
        font-family: {FONT};
        color: {TEXT_COLOR};
    }}
    .stTextInput, .stTextArea {{
        border: 2px solid {TEXT_COLOR};
        background-color: white;
        color: black;
        border-radius: 8px;
        padding: 10px;
        font-size: 16px;
    }}
    .stButton > button {{
        background-color: {TEXT_COLOR};
        color: {BG_COLOR};
        border-radius: 8px;
        font-size: 16px;
    }}
    .stButton > button:hover {{
        background-color: {BG_COLOR};
        color: {TEXT_COLOR};
        border: 2px solid {TEXT_COLOR};
    }}
    </style>
""", unsafe_allow_html=True)

# Title for the app
st.title("Spurgeon Articles")

# Instructions
st.subheader("Enter the Game Notes Below:")
st.write("Write your game notes in the text box and click **Generate Article** to create a professional sports article in Spurgeon College style.")

# Input for the base article format (optional)
article_template = st.text_area("Article Template", value="Insert a base article format or leave blank for general style.", height=150)

# Input for game notes (required)
game_notes = st.text_area("Game Notes", "Insert your game notes here.", height=200)

# Generate Article button
if st.button('Generate Article'):
    if not game_notes.strip():
        st.warning("Please enter game notes to generate the article.")
    else:
        with st.spinner("Generating article..."):
            # OpenAI prompt
            conversation_history = [
                {"role": "system", "content": "You are a professional sports article writer."},
                {"role": "user", "content": f"Write an article in the same format, style, and vibe as the following text:\n\n{article_template}. The article will be based on the following game notes:\n{game_notes}. The article should only be about and get information from the notes. Be creative and make sure you follow the format."},
                {"role": "user", "content": f"Now, for Spurgeon College, write a new article based on the following game notes:\n{game_notes}. Make sure you focus more on Spurgeon and make it encouraging even if it's a loss, and hype it up if it's a win for Spurgeon."}
            ]

            # Generate the article using OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=conversation_history,
                max_tokens=800,
                temperature=0.7
            )

            # Extract the generated article
            article_text = response['choices'][0]['message']['content'].strip()

            # Display the generated article in the app
            st.subheader("Generated Article")
            st.write(article_text)

            # Option to download the article
            st.download_button(
                label="Download Article as Text File",
                data=article_text,
                file_name='spurgeon_article.txt',
                mime='text/plain'
            )
