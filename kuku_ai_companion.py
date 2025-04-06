import os
import streamlit as st
import requests
from gtts import gTTS
from dotenv import load_dotenv
import base64

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_story(mood):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "user",
                "content": f"Write a fictional story based on the mood: '{mood}'. Do not include any explanations, summaries, or analysis. Just give the story directly, ready for narration."
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content'].strip()

def generate_audio(text, filename="story.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    return filename

st.set_page_config(page_title="AI Story Companion", page_icon="📖")
st.title("AI Story Companion")
st.markdown("Get a mood-based AI-generated story with voice narration!")

if "story_count" not in st.session_state:
    st.session_state.story_count = 0

st.markdown(f"### Stories played: {st.session_state.story_count}")

mood = st.selectbox("Choose your mood:", ["Happy", "Sad", "Adventurous", "Romantic", "Calm", "Curious"])

if st.button("Generate Story"):
    with st.spinner("Crafting your story..."):
        story = generate_story(mood)
        st.session_state.story_count += 1

        audio_path = generate_audio(story)
        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            b64 = base64.b64encode(audio_bytes).decode()

        st.markdown(
            f"""
            <audio controls autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### 📖 Your Story")
        st.write(story)

        st.markdown("### Did you enjoy the story?")
        col1, col2 = st.columns(2)
        with col1:
            st.button("👍 Yes")
        with col2:
            st.button("👎 No")
