from csv import Error
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound 
import yt_dlp
import re


def get_metadata(url: str) -> dict:
    ydl_opts = {'quiet': True, 'skip_download': True, 'extract_flat': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            'title': info.get('title', None),  # type: ignore
            'uploader': info.get('channel', None),  # type: ignore
            'description': info.get('description', None), # type: ignore
            'thumbnail': info.get('thumbnail', None)  # type: ignore
        }
    

def get_video_id(url: str):
    if 'list=' in url: return None
    pattern = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None


def get_transcript(video_id: str):
    # Retrieve the available transcripts
    ytt_api = YouTubeTranscriptApi()
    transcript_list = ytt_api.list(video_id)
    
    transcript = None
    try:
        # Manual transcript in English
        transcript = transcript_list.find_manually_created_transcript(['en']).fetch()
    except NoTranscriptFound:
        try:
            # Auto-generated transcript in English
            transcript = transcript_list.find_generated_transcript(['en']).fetch()
        except NoTranscriptFound:
            try:
                # Any manual transcript (regardless of language)
                transcript = transcript_list.find_manually_created_transcript(transcript_list._manually_created_transcripts.keys())
                transcript = transcript.translate('en').fetch()
            except NoTranscriptFound:
                try:
                    # Any auto-generated transcript (regardless of language)
                    transcript = transcript_list.find_generated_transcript(transcript_list._generated_transcripts.keys())
                    transcript = transcript.translate('en').fetch()
                except NoTranscriptFound:
                    transcript = None
                    print("No transcripts found (manual or auto-generated in any language).")

    # Combine the transcript into a single string
    transcript_combined = ""
    if transcript:
        for snippet in transcript:
            transcript_combined += snippet.text.replace('\n', ' ') + " "
    else:
        print("No transcript available")

    return transcript_combined if transcript_combined != "" else None
