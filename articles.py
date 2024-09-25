import openai
import streamlit as st

# Set the OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Define the conversation history
conversation_history = [
    {"role": "system", "content": "You are a professional sports article writer."},
    {"role": "user", "content": "Write an article in the same format, style, and vibe as the following text:\n\n{article_template}. The article will be based on the following game notes:\n{game_notes}. The article should only be about and get information from the notes. Be creative and make sure you follow the format."},
    {"role": "user", "content": "Now, for Spurgeon College, write a new article based on the following game notes:\n{game_notes}. Make sure you focus more on Spurgeon and make it encouraging even if it's a loss, and hype it up if it's a win for Spurgeon."}
]

# Function to generate article using OpenAI API
def generate_article(conversation_history):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=conversation_history,
            max_tokens=1000,  # Adjust token limit as needed
            temperature=0.7
        )

        # Correct way to access the content
        article_text = response.choices[0].message['content'].strip()

        return article_text

    except Exception as e:
        st.error(f"An error occurred with the OpenAI API: {e}")
        return None

# Example call
article_text = generate_article(conversation_history)

if article_text:
    st.write(article_text)
