import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import torch
import gradio as gr
from transformers import pipeline

# Load the summarization model
text_summary = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", torch_dtype=torch.bfloat16)

def summary(input_text):
    output = text_summary(input_text)
    return output[0]['summary_text']

def extract_video_id(url):
    regex = r"(?:youtube\.com\/(?:.*[?&]v=|embed\/|v\/|shorts\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

def get_youtube_transcript(video_url):
    """Fetches the transcript from a YouTube video and summarizes it."""
    video_id = extract_video_id(video_url)
    if not video_id:
        return "Error: Could not extract a valid video ID from the URL."

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        if not transcript:
            return "Error: No transcript available for this video."

        # Format transcript into plain text
        formatter = TextFormatter()
        text_transcript = formatter.format_transcript(transcript)

        # Summarize the transcript
        summary_text = summary(text_transcript)

        return summary_text
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Close any previous Gradio instances
gr.close_all()

# Gradio interface setup
demo = gr.Interface(
    fn=get_youtube_transcript,
    inputs=[gr.Textbox(label="Enter YouTube URL to summarize", lines=1)],
    outputs=[gr.Textbox(label="Summarized Transcript", lines=4)],
    title="YouTube Video Summarizer",
    description="Enter a YouTube video URL to get a summarized version of its transcript.",
)

# Launch the Gradio app
demo.launch()
