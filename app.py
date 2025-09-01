import os
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI

# Load API key locally if .env exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # If dotenv isn't installed, just skip (Streamlit Cloud won't need it)

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key not found! Please set it in .env or Streamlit Secrets.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

st.title("🎥 AI YouTube Summarizer")
st.write("Paste a YouTube link and get a summary, key insights, and quiz questions!")

video_url = st.text_input("Enter YouTube link:")

def extract_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        return None

if st.button("Summarize Video"):
    if not api_key:
        st.error("No API key found!")
    elif not video_url:
        st.error("Please paste a YouTube link.")
    else:
        try:
            video_id = extract_video_id(video_url)
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            full_text = " ".join([t['text'] for t in transcript])

            with st.spinner("Summarizing..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that summarizes YouTube videos."},
                        {"role": "user", "content": f"Summarize this transcript: {full_text}\n\nProvide:\n1. Bullet-point summary\n2. 5 key keywords\n3. 3 quiz questions"}
                    ]
                )
                st.success("Done!")
                st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(f"Error: {e}")
