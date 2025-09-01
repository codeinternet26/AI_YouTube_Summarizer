import os
import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.title("🎥 AI YouTube Summarizer")
st.write("Paste a YouTube link and get a summary, key insights, and quiz questions!")

# Input box for YouTube link
video_url = st.text_input("Enter YouTube link:")

# Function to extract video ID from URL
def extract_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        return None

# Button to generate summary
if st.button("Summarize Video"):
    if not api_key:
        st.error("No API key found. Please set it in your .env or Streamlit secrets.")
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
