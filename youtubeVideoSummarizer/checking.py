## this file is used to check the url of the youtube video summarizer.
import re

def extract_video_id(url):
    regex = r"(?:youtube\.com\/(?:.*[?&]v=|embed\/|v\/|shorts\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None

# Test cases
urls = [
    "https://www.youtube.com/watch?v=FooC7gp4wk4",
    "https://youtu.be/FooC7gp4wk4",
    "https://www.youtube.com/embed/FooC7gp4wk4",
    "https://www.youtube.com/v/FooC7gp4wk4",
    "https://www.youtube.com/shorts/FooC7gp4wk4",
    "https://www.youtube.com/watch?v=Bar12345678&ab_channel=Example"
]

for url in urls:
    print(f"{url} -> {extract_video_id(url)}")  # Should print the 11-character video ID