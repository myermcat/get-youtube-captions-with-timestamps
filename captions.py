# pip install youtube-transcript-api
import sys
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

PREF_LANGS = ["en", "en-US", "en-GB", "en-CA", "en-AU", "en-*"]

def get_video_id(url_or_id: str) -> str:
    if url_or_id.startswith("http"):
        u = urlparse(url_or_id)
        if "youtube.com" in u.netloc:
            return parse_qs(u.query).get("v", [""])[0]
        if "youtu.be" in u.netloc:
            return u.path.lstrip("/")
    return url_or_id

def to_mmss(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"

def print_captions(url_or_id: str):
    vid = get_video_id(url_or_id)
    try:
        # Create API instance and get transcript list (ONLY 1 REQUEST)
        api = YouTubeTranscriptApi()
        transcript_list = api.list(vid)
        
        # Get all available transcripts in one go
        available_transcripts = list(transcript_list)
        
        if not available_transcripts:
            sys.exit("No transcripts available for this video.")
        
        # Show available options
        print("Available transcripts:")
        for t in available_transcripts:
            transcript_type = "Manual" if not t.is_generated else "Auto-generated"
            print(f"  - {t.language_code} ({t.language}) - {transcript_type}")
        print()
        
        # Find the best transcript with OPTIMIZED logic
        best_transcript = None
        
        # Priority 1: Manual transcripts in preferred languages
        for transcript in available_transcripts:
            if not transcript.is_generated:  # Manual transcript
                for lang in PREF_LANGS:
                    if lang == "en-*" and transcript.language_code.startswith("en"):
                        best_transcript = transcript
                        break
                    elif lang == transcript.language_code:
                        best_transcript = transcript
                        break
                if best_transcript:
                    break
        
        # Priority 2: Auto-generated transcripts in preferred languages
        if not best_transcript:
            for transcript in available_transcripts:
                for lang in PREF_LANGS:
                    if lang == "en-*" and transcript.language_code.startswith("en"):
                        best_transcript = transcript
                        break
                    elif lang == transcript.language_code:
                        best_transcript = transcript
                        break
                if best_transcript:
                    break
        
        # Priority 3: Any available transcript as fallback
        if not best_transcript:
            best_transcript = available_transcripts[0]
        
        # Show what we're using
        transcript_type = "Manual" if not best_transcript.is_generated else "Auto-generated"
        print(f"Selected: {transcript_type} transcript: {best_transcript.language_code} ({best_transcript.language})")
        print("-" * 50)
        
        # Fetch the transcript (ONLY 1 MORE REQUEST)
        segs = best_transcript.fetch()
        
    except TranscriptsDisabled:
        sys.exit("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        sys.exit("No transcript found in preferred languages (or at all).")
    except Exception as e:
        sys.exit(f"Error fetching transcript: {e}")
    
    for e in segs:
        # Handle both dict and object formats
        if hasattr(e, 'text'):
            text = e.text
            start = e.start
        else:
            text = e.get("text", "")
            start = e.get("start", 0)
        
        text = text.replace("\n", " ").strip()
        if text:
            print(f"[{to_mmss(start)}] {text}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # default demo; or show usage
        url = "https://www.youtube.com/watch?v=bZQun8Y4L2A"
    else:
        url = sys.argv[1]
    print_captions(url)

