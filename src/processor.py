import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def extract_video_id(url: str) -> str:
    """
    Extracts the unique video ID from a standard YouTube URL.
    """
    id_pattern = r"(?:v=|\/|be\/|embed\/)([0-9A-Za-z_-]{11})(?:[&?]|$)"
    match = re.search(id_pattern, url)
    if match:
        return match.group(1)
    return None

def get_video_transcript(video_id: str) -> str:
    """
    Fetches the transcript by trying all possible calling conventions 
    for the youtube-transcript-api library.
    """
    transcript_list = None
    
    # Try 1: Modern Static Method (list_transcripts)
    if transcript_list is None:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        except:
            pass

    # Try 2: Modern Instance Method (list_transcripts)
    if transcript_list is None:
        try:
            transcript_list = YouTubeTranscriptApi().list_transcripts(video_id)
        except:
            pass

    # Try 3: Alternative Static Method (list)
    if transcript_list is None:
        try:
            transcript_list = YouTubeTranscriptApi.list(video_id)
        except:
            pass

    # Try 4: Alternative Instance Method (list)
    if transcript_list is None:
        try:
            transcript_list = YouTubeTranscriptApi().list(video_id)
        except:
            pass

    if transcript_list is None:
        return "Error: Could not find a working method to list transcripts in your library version."

    try:
        # Now that we have the list, find the best transcript
        try:
            # Prefer English
            transcript = transcript_list.find_transcript(['en'])
        except:
            # Fallback: Grab the first available (e.g., Hindi) for the AI to translate
            available = list(transcript_list)
            if available:
                transcript = available[0]
            else:
                return "Error: No transcripts found for this video."

        # Fetch and format
        data = transcript.fetch()
        formatter = TextFormatter()
        return " ".join(formatter.format_transcript(data).split())

    except Exception as e:
        return f"Error: {str(e)}"

def clean_transcript_text(text: str) -> str:
    """
    Removes bracketed noise like [Music] or [Laughter].
    """
    text = re.sub(r"\[.*?\]", "", text)
    return " ".join(text.split())