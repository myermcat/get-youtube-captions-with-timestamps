# YouTube Transcript Tool

A Python tool to extract and display YouTube video captions/transcripts.

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation:**
   ```bash
   python test_captions.py
   ```

## Usage

### Basic usage:
```bash
python captions.py [youtube_url_or_id]
```

### Examples:
```bash
# Use default demo video
python captions.py

# Use specific video
python captions.py "https://www.youtube.com/watch?v=bZQun8Y4L2A"

# Use video ID directly
python captions.py bZQun8Y4L2A
```

### Output format:
```
[00:00] Video transcript text here
[00:05] More transcript text
[00:10] And so on...
```

## Features

- Supports both YouTube URLs and video IDs
- Handles various YouTube URL formats (youtube.com, youtu.be)
- Prefers English transcripts when available
- Graceful error handling for videos without transcripts
- Time-stamped output in MM:SS format

## Troubleshooting

If you get import errors:
1. Make sure you've installed requirements: `pip install -r requirements.txt`
2. Check that you're using Python 3.6+
3. Verify the `youtube-transcript-api` package is installed

## Note

This tool requires the video to have captions/transcripts enabled. Not all YouTube videos have transcripts available.

## Live Demo

**Testing URL:** https://get-youtube-captions-with-timestamps.onrender.com

**Note:** This is a demo instance that may go to sleep. For production use, please deploy your own instance.

**Health Check:** https://get-youtube-captions-with-timestamps.onrender.com/health

## API Usage

### Deploy to Render

1. Push your code to GitHub
2. Connect your repository to [Render](https://render.com)
3. Create a new Web Service
4. Render will automatically detect the Python environment and deploy

### API Endpoints

**Health Check:**
```bash
GET https://your-app-name.onrender.com/health
```

**Get Transcript:**
```bash
POST https://your-app-name.onrender.com/transcript
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
```json
{
  "success": true,
  "transcript": "[00:00] Video transcript here...",
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

### n8n Integration

Use the HTTP Request node in n8n to call your deployed API:

- **Method:** POST
- **URL:** `https://your-app-name.onrender.com/transcript`
- **Headers:** `Content-Type: application/json`
- **Body:** `{"url": "{{$json.youtube_url}}"}`

## Deployment Files

- `app.py` - Flask API wrapper
- `render.yaml` - Render deployment configuration
- `requirements.txt` - Python dependencies
